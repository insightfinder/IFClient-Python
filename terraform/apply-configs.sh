#!/bin/bash

# apply-configs.sh - Apply InsightFinder configurations using Terraform
# This script replaces the IFClient-Python CLI tool

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Usage function
usage() {
    cat << EOF
Usage: $0 <environment> [action] [options]

This script replaces IFClient-Python CLI with Terraform for managing InsightFinder configurations.

Environments:
  stg      - Staging environment
  staging  - Staging environment  
  prod     - Production environment

Actions:
  plan     - Show what will be configured (default)
  apply    - Apply the configurations to InsightFinder
  destroy  - Remove configurations (use with caution)
  validate - Validate Terraform configuration
  output   - Show applied configuration details

Options:
  --username <user>    - InsightFinder username (overrides tfvars)
  --password <pass>    - InsightFinder password (overrides env var)
  --base-url <url>     - InsightFinder base URL (overrides tfvars)
  --auto-approve       - Skip confirmation prompts

Examples:
  $0 stg plan
  $0 prod apply --username myuser
  $0 stg apply --auto-approve

Environment Variables:
  TF_VAR_insightfinder_password    - InsightFinder password
  TF_VAR_insightfinder_username    - InsightFinder username (optional)
  TF_VAR_insightfinder_base_url    - InsightFinder URL (optional)

EOF
}

# Parse command line arguments
parse_args() {
    ENVIRONMENT=""
    ACTION="plan"
    USERNAME=""
    PASSWORD=""
    BASE_URL=""
    AUTO_APPROVE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --username)
                USERNAME="$2"
                shift 2
                ;;
            --password)
                PASSWORD="$2"
                shift 2
                ;;
            --base-url)
                BASE_URL="$2"
                shift 2
                ;;
            --auto-approve)
                AUTO_APPROVE=true
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -z "$ENVIRONMENT" ]]; then
                    ENVIRONMENT="$1"
                elif [[ -z "$ACTION" || "$ACTION" == "plan" ]]; then
                    ACTION="$1"
                else
                    log_error "Too many positional arguments"
                    usage
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$ENVIRONMENT" ]]; then
        log_error "Environment is required"
        usage
        exit 1
    fi
}

# Validate environment
validate_environment() {
    local env=$1
    local tfvars_file="${env}.tfvars"
    
    if [[ ! -f "$tfvars_file" ]]; then
        log_error "Environment file not found: $tfvars_file"
        log_info "Available environments:"
        ls -1 *.tfvars 2>/dev/null | sed 's/\.tfvars$//' || log_warning "No environment files found"
        exit 1
    fi
    
    case "$env" in
        stg|prod)
            ;;
        *)
            log_warning "Unknown environment: $env (proceeding anyway)"
            ;;
    esac
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if terraform is installed
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform is not installed. Please install Terraform first."
        exit 1
    fi
    
    # Check terraform version
    local tf_version=$(terraform version -json | jq -r '.terraform_version' 2>/dev/null || terraform version | head -n1 | cut -d' ' -f2 | sed 's/v//')
    log_info "Terraform version: $tf_version"
    
    log_success "Prerequisites check completed"
}

# Setup environment variables
setup_env_vars() {
    if [[ -n "$USERNAME" ]]; then
        export TF_VAR_insightfinder_username="$USERNAME"
        log_info "Using provided username: $USERNAME"
    fi
    
    if [[ -n "$PASSWORD" ]]; then
        export TF_VAR_insightfinder_password="$PASSWORD"
        log_info "Using provided password"
    fi
    
    if [[ -n "$BASE_URL" ]]; then
        export TF_VAR_insightfinder_base_url="$BASE_URL"
        log_info "Using provided base URL: $BASE_URL"
    fi
    
    # Check if password is set
    if [[ -z "${TF_VAR_insightfinder_password:-}" ]]; then
        if [[ -t 0 ]]; then
            read -s -p "Enter InsightFinder password: " TF_VAR_insightfinder_password
            echo
            export TF_VAR_insightfinder_password
        else
            log_error "InsightFinder password not provided. Set TF_VAR_insightfinder_password or use --password"
            exit 1
        fi
    fi
}

# Initialize Terraform
init_terraform() {
    log_info "Initializing Terraform..."
    terraform init -upgrade
    log_success "Terraform initialized"
}

# Validate configuration
validate_terraform() {
    local environment=$1
    
    log_info "Validating Terraform configuration..."
    terraform validate
    
    log_info "Formatting Terraform files..."
    terraform fmt -check=true -diff=true || {
        log_warning "Terraform files are not properly formatted"
        terraform fmt
        log_info "Files have been formatted"
    }
    
    log_success "Configuration is valid"
}

# Plan changes
plan_terraform() {
    local environment=$1
    local tfvars_file="${environment}.tfvars"
    
    log_info "Planning InsightFinder configuration changes for environment: $environment"
    
    terraform plan \
        -var-file="$tfvars_file" \
        -out="terraform-${environment}.tfplan"
    
    log_success "Plan created: terraform-${environment}.tfplan"
    log_info "Review the plan above. Use 'apply' action to execute the changes."
}

# Apply configuration
apply_terraform() {
    local environment=$1
    local tfvars_file="${environment}.tfvars"
    
    log_info "Applying InsightFinder configurations for environment: $environment"
    
    # Check if plan file exists
    local plan_file="terraform-${environment}.tfplan"
    if [[ -f "$plan_file" ]]; then
        log_info "Using existing plan file: $plan_file"
        
        if [[ "$AUTO_APPROVE" != "true" ]]; then
            read -p "Do you want to apply this plan? (yes/no): " confirm
            if [[ "$confirm" != "yes" ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        fi
        
        terraform apply "$plan_file"
    else
        log_warning "No plan file found. Creating and applying in one step..."
        
        # Confirmation for production
        if [[ "$environment" == "prod" && "$AUTO_APPROVE" != "true" ]]; then
            log_warning "You are about to apply changes to PRODUCTION InsightFinder!"
            read -p "Are you sure you want to continue? (yes/no): " confirm
            if [[ "$confirm" != "yes" ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        fi
        
        local apply_args=("-var-file=$tfvars_file")
        if [[ "$AUTO_APPROVE" == "true" ]]; then
            apply_args+=("-auto-approve")
        fi
        
        terraform apply "${apply_args[@]}"
    fi
    
    log_success "InsightFinder configurations applied successfully for environment: $environment"
    
    # Clean up plan file
    if [[ -f "$plan_file" ]]; then
        rm "$plan_file"
        log_info "Cleaned up plan file: $plan_file"
    fi
    
    # Show outputs
    log_info "Configuration results:"
    terraform output
}

# Destroy configuration
destroy_terraform() {
    local environment=$1
    local tfvars_file="${environment}.tfvars"
    
    log_warning "You are about to REMOVE InsightFinder configurations for environment: $environment"
    
    # Double confirmation for production
    if [[ "$environment" == "prod" ]]; then
        log_error "WARNING: This will remove PRODUCTION InsightFinder configurations!"
        if [[ "$AUTO_APPROVE" != "true" ]]; then
            read -p "Type 'destroy-prod-configs' to confirm: " confirm
            if [[ "$confirm" != "destroy-prod-configs" ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        fi
    else
        if [[ "$AUTO_APPROVE" != "true" ]]; then
            read -p "Are you sure you want to remove the configurations? (yes/no): " confirm
            if [[ "$confirm" != "yes" ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        fi
    fi
    
    local destroy_args=("-var-file=$tfvars_file")
    if [[ "$AUTO_APPROVE" == "true" ]]; then
        destroy_args+=("-auto-approve")
    fi
    
    terraform destroy "${destroy_args[@]}"
    
    log_success "InsightFinder configurations removed for environment: $environment"
}

# Show outputs
show_outputs() {
    log_info "Current InsightFinder configuration status:"
    terraform output
}

# Main function
main() {
    # Change to script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$SCRIPT_DIR"
    
    parse_args "$@"
    
    validate_environment "$ENVIRONMENT"
    check_prerequisites
    setup_env_vars
    
    case "$ACTION" in
        validate)
            init_terraform
            validate_terraform "$ENVIRONMENT"
            ;;
        plan)
            init_terraform
            validate_terraform "$ENVIRONMENT"
            plan_terraform "$ENVIRONMENT"
            ;;
        apply)
            init_terraform
            validate_terraform "$ENVIRONMENT"
            apply_terraform "$ENVIRONMENT"
            ;;
        destroy)
            destroy_terraform "$ENVIRONMENT"
            ;;
        output)
            show_outputs
            ;;
        *)
            log_error "Invalid action: $ACTION"
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"