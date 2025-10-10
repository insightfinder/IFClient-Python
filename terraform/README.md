# InsightFinder Terraform Configuration

This Terraform configuration provides an Infrastructure as Code (IaC) approach to manage InsightFinder projects, instances, and metric configurations. It serves as an alternative to the IFClient-Python CLI tool for automated deployment and configuration management.

## Overview

The Terraform configuration automates the creation and management of:
- **InsightFinder Projects**: Complete project setup with display names and configuration parameters
- **Instance Grouping**: Configure instances with container names, app names, and grouping settings
- **Metric Settings**: Define metric thresholds, alerts, and monitoring parameters
- **Batch Operations**: Apply multiple configurations efficiently with proper timing

## Features

- 🚀 **Automated Configuration**: Deploy multiple projects and configurations in a single run
- 🔧 **Infrastructure as Code**: Version-controlled, repeatable deployments
- 🛡️ **Secure**: Sensitive information handled through environment variables
- 📊 **Comprehensive**: Support for projects, instances, and metric configurations
- 🔄 **Flexible**: Multiple environment support (staging, production, test)
- 📝 **Validated**: Built-in validation and planning capabilities

## Prerequisites

### Required Tools
- **Terraform** >= 1.0
- **Bash** shell (for scripts)
- **InsightFinder Account** with appropriate permissions

### Environment Setup
1. Install Terraform:
   ```bash
   # On Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform

   # On macOS
   brew install terraform

   # On Windows
   choco install terraform
   ```

2. Verify installation:
   ```bash
   terraform --version
   ```

## Quick Start

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

### 2. Set Environment Variables
```bash
# Required for authentication
export TF_VAR_insightfinder_password="your-password"

# Optional: Override defaults
export TF_VAR_insightfinder_username="your-username"
export TF_VAR_insightfinder_base_url="https://your-instance.insightfinder.com"
```

### 3. Choose Your Environment Configuration
Select one of the pre-configured environments:
- `test.tfvars` - Test/development environment with sample data
- `stg.tfvars` - Staging environment configuration
- `prod.tfvars` - Production environment configuration

### 4. Plan and Apply Configuration
```bash
# See what will be created
terraform plan -var-file="test.tfvars"

# Apply the configuration
terraform apply -var-file="test.tfvars"
```

## Configuration Structure

### Project Configuration

Each project is defined in the `projects` variable with the following structure:

```hcl
projects = {
  "project-name" = {
    project_display_name = "Human Readable Project Name"
    c_value              = 2                    # Confidence value (1-5)
    p_value              = 0.95                 # P-value threshold (0.0-1.0)
    show_instance_down   = true                 # Show instance down alerts
    retention_time       = 120                  # Data retention in days
    ubl_retention_time   = 60                   # UBL retention in days

    instances = [
      {
        instance_name         = "SERVER_1"
        instance_display_name = "Server 1"
        container_name        = "app-server-1"
        app_name              = "my-application"
        ignore_flag           = false
      }
    ]

    metrics = [
      {
        metric_name                            = "cpu-usage"
        escalate_incident_all                  = true
        threshold_alert_lower_bound            = 5
        threshold_alert_upper_bound            = 90
        threshold_alert_lower_bound_negative   = -10
        threshold_alert_upper_bound_negative   = -20
        threshold_no_alert_lower_bound         = 10
        threshold_no_alert_upper_bound         = 80
        threshold_no_alert_lower_bound_negative = 5
        threshold_no_alert_upper_bound_negative = 15
      }
    ]
  }
}
```

### Variable Reference

#### Global Variables
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `insightfinder_base_url` | string | `https://stg.insightfinder.com` | InsightFinder instance URL |
| `insightfinder_username` | string | (required) | Username for authentication |
| `insightfinder_password` | string | (required) | Password for authentication |

#### Project Variables
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `project_display_name` | string | (required) | Human-readable project name |
| `c_value` | number | 1 | Confidence value (1-5) |
| `p_value` | number | 0.95 | P-value threshold (0.0-1.0) |
| `show_instance_down` | bool | false | Enable instance down alerts |
| `retention_time` | number | 11 | Data retention period (days) |
| `ubl_retention_time` | number | 11 | UBL retention period (days) |

#### Instance Variables
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `instance_name` | string | (required) | Unique instance identifier |
| `instance_display_name` | string | instance_name | Human-readable instance name |
| `container_name` | string | null | Container identifier |
| `app_name` | string | null | Application identifier |
| `metric_instance_name` | string | null | Metric instance identifier |
| `ignore_flag` | bool | false | Whether to ignore this instance |

#### Metric Variables
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `metric_name` | string | (required) | Metric identifier |
| `escalate_incident_all` | bool | true | Escalate all incidents |
| `threshold_alert_lower_bound` | number | 15 | Lower alert threshold |
| `threshold_alert_upper_bound` | number | 105 | Upper alert threshold |
| `threshold_alert_*_negative` | number | varies | Negative threshold values |
| `threshold_no_alert_*` | number | varies | No-alert threshold values |

## Usage Examples

### Simple Single Project
```hcl
# terraform/my-project.tfvars
insightfinder_base_url = "https://your-instance.insightfinder.com"
insightfinder_username = "your-username"

projects = {
  "web-app-monitoring" = {
    project_display_name = "Web Application Monitoring"
    c_value              = 2
    p_value              = 0.95
    
    instances = [
      {
        instance_name         = "WEB_SERVER_1"
        instance_display_name = "Web Server 1"
        container_name        = "nginx-web-1"
        app_name              = "web-frontend"
      }
    ]
    
    metrics = [
      {
        metric_name                    = "response-time"
        threshold_alert_upper_bound    = 5000  # 5 seconds
        threshold_no_alert_upper_bound = 2000  # 2 seconds
      }
    ]
  }
}
```

### Multiple Environment Projects
```hcl
# terraform/multi-env.tfvars
projects = {
  "prod-web-app" = {
    project_display_name = "Production Web App"
    retention_time       = 365
    c_value              = 3
    
    instances = [
      { instance_name = "PROD_WEB_1", app_name = "web-prod" },
      { instance_name = "PROD_WEB_2", app_name = "web-prod" }
    ]
    
    metrics = [
      { metric_name = "cpu-usage", threshold_alert_upper_bound = 80 },
      { metric_name = "memory-usage", threshold_alert_upper_bound = 90 }
    ]
  }
  
  "staging-web-app" = {
    project_display_name = "Staging Web App"
    retention_time       = 30
    c_value              = 2
    
    instances = [
      { instance_name = "STG_WEB_1", app_name = "web-staging" }
    ]
    
    metrics = [
      { metric_name = "cpu-usage", threshold_alert_upper_bound = 90 }
    ]
  }
}
```

## Advanced Usage

### Using the Management Script
The included `apply-configs.sh` script provides a convenient wrapper around Terraform:

```bash
# Plan configuration for staging
./apply-configs.sh stg plan

# Apply configuration to production
./apply-configs.sh prod apply

# Validate configuration files
./apply-configs.sh test validate

# Show outputs from applied configuration
./apply-configs.sh prod output
```

### Environment-Specific Commands
```bash
# Staging environment
terraform plan -var-file="stg.tfvars"
terraform apply -var-file="stg.tfvars"

# Production environment
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"

# Test environment
terraform plan -var-file="test.tfvars"
terraform apply -var-file="test.tfvars"
```

### Using Environment Variables
```bash
# Set all required variables
export TF_VAR_insightfinder_username="myuser"
export TF_VAR_insightfinder_password="mypassword"
export TF_VAR_insightfinder_base_url="https://prod.insightfinder.com"

# Run terraform without variable files
terraform plan
terraform apply
```

## File Structure

```
terraform/
├── main.tf                     # Main Terraform configuration
├── README.md                   # This file
├── apply-configs.sh           # Management script
├── test.tfvars                # Test environment configuration
├── stg.tfvars                 # Staging environment configuration
├── prod.tfvars                # Production environment configuration
├── .terraform.lock.hcl        # Provider version locks
└── scripts/
    └── apply-single-config.sh  # Single configuration application script
```

## Outputs

After successful application, Terraform provides the following outputs:

### `project_configurations`
Details about each configured project:
```json
{
  "my-project": {
    "project_name": "my-project",
    "configured_at": "2024-10-10T14:30:00Z",
    "instances_count": 2,
    "metrics_count": 3
  }
}
```

### `authentication_status`
Summary of the configuration process:
```json
{
  "base_url": "https://your-instance.insightfinder.com",
  "username": "your-username",
  "projects_count": 1,
  "total_instances": 2,
  "total_metrics": 3
}
```

## Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Verify credentials
export TF_VAR_insightfinder_username="correct-username"
export TF_VAR_insightfinder_password="correct-password"

# Test connection manually
curl -u "$TF_VAR_insightfinder_username:$TF_VAR_insightfinder_password" \
     "$TF_VAR_insightfinder_base_url/api/health"
```

#### Configuration Validation Errors
```bash
# Validate syntax
terraform validate

# Check formatting
terraform fmt -check

# Detailed plan output
terraform plan -var-file="test.tfvars" -detailed-exitcode
```

#### State Management Issues
```bash
# Refresh state
terraform refresh -var-file="your-env.tfvars"

# Import existing resources
terraform import 'resource.name' resource-id

# Force unlock if needed
terraform force-unlock LOCK_ID
```

### Debugging

#### Enable Detailed Logging
```bash
export TF_LOG=DEBUG
terraform apply -var-file="test.tfvars"
```

#### Validate Individual Components
```bash
# Test script functionality
bash -x scripts/apply-single-config.sh

# Check configuration files
cat .terraform/configs/*-config.json | jq .
```

## Security Best Practices

### 1. Environment Variables
Never commit passwords or sensitive information to version control:
```bash
# Use environment variables
export TF_VAR_insightfinder_password="secure-password"

# Or use external secret management
export TF_VAR_insightfinder_password="$(aws secretsmanager get-secret-value --secret-id prod/insightfinder --query SecretString --output text)"
```

### 2. State File Security
- Store Terraform state securely (use remote backends)
- Never commit `.tfstate` files to version control
- Use state locking to prevent concurrent modifications

### 3. Access Control
- Use principle of least privilege for InsightFinder accounts
- Regularly rotate credentials
- Monitor configuration changes

## Migration from IFClient-Python

If migrating from the IFClient-Python CLI tool:

### 1. Export Existing Configuration
```bash
# Export current configuration using IFClient-Python
ifclient generate --output-dir ./configs

# Convert to Terraform format
# (Manual conversion required - see examples above)
```

### 2. Import Existing Resources
```bash
# Import existing projects if needed
terraform import 'local_file.project_configs["project-name"]' ./path/to/existing/config.json
```

### 3. Validate Migration
```bash
# Plan to see what changes would be made
terraform plan -var-file="your-env.tfvars"

# Apply only if plan shows expected changes
terraform apply -var-file="your-env.tfvars"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

### Development Setup
```bash
git clone https://github.com/insightfinder/IFClient-Python.git
cd IFClient-Python/terraform
terraform init
terraform validate
```

## Support

- **Documentation**: [InsightFinder Documentation](https://docs.insightfinder.com)
- **Issues**: [GitHub Issues](https://github.com/insightfinder/IFClient-Python/issues)
- **Community**: [InsightFinder Community](https://community.insightfinder.com)

## License

This project is licensed under the same license as the parent IFClient-Python project.

---

**Note**: This Terraform configuration is designed to work alongside or replace the IFClient-Python CLI tool for automated deployments. Choose the approach that best fits your infrastructure automation strategy.
