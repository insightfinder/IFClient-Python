terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.9"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

# Variables for InsightFinder configuration
variable "insightfinder_base_url" {
  description = "Base URL for InsightFinder deployment"
  type        = string
  default     = "https://stg.insightfinder.com"
}

variable "insightfinder_username" {
  description = "InsightFinder username"
  type        = string
  sensitive   = true
}

variable "insightfinder_password" {
  description = "InsightFinder password"
  type        = string
  sensitive   = true
}

variable "projects" {
  description = "Map of InsightFinder projects to configure"
  type = map(object({
    project_display_name = string
    c_value              = optional(number, 1)
    p_value              = optional(number, 0.95)
    show_instance_down   = optional(bool, false)
    retention_time       = optional(number, 11)
    ubl_retention_time   = optional(number, 11)

    # Instance grouping settings
    instances = optional(list(object({
      instance_name         = string
      instance_display_name = optional(string)
      container_name        = optional(string)
      app_name              = optional(string)
      metric_instance_name  = optional(string)
      ignore_flag           = optional(bool, false)
    })), [])

    # Metric settings
    metrics = optional(list(object({
      metric_name                             = string
      escalate_incident_all                   = optional(bool, true)
      threshold_alert_lower_bound             = optional(number, 15)
      threshold_alert_upper_bound             = optional(number, 105)
      threshold_alert_upper_bound_negative    = optional(number, -20)
      threshold_alert_lower_bound_negative    = optional(number, -5)
      threshold_no_alert_lower_bound          = optional(number, 50)
      threshold_no_alert_upper_bound          = optional(number, 75)
      threshold_no_alert_lower_bound_negative = optional(number, 20)
      threshold_no_alert_upper_bound_negative = optional(number, 40)
    })), [])
  }))
}

# Local values for processing
locals {
  # Flatten projects for iteration
  project_configs = {
    for project_name, config in var.projects : project_name => {
      name                 = project_name
      project_display_name = config.project_display_name
      c_value              = config.c_value
      p_value              = config.p_value
      show_instance_down   = config.show_instance_down
      retention_time       = config.retention_time
      ubl_retention_time   = config.ubl_retention_time
      instances            = config.instances
      metrics              = config.metrics
    }
  }
}

# Create configuration files for each project
resource "local_file" "project_configs" {
  for_each = local.project_configs

  filename = "${path.module}/.terraform/configs/${each.key}-config.json"
  content = jsonencode({
    projectName        = each.value.name
    projectDisplayName = each.value.project_display_name
    cValue             = each.value.c_value
    pValue             = each.value.p_value
    showInstanceDown   = each.value.show_instance_down
    retentionTime      = each.value.retention_time
    UBLRetentionTime   = each.value.ubl_retention_time

    instanceDataList = [
      for instance in each.value.instances : {
        instanceName        = instance.instance_name
        instanceDisplayName = coalesce(instance.instance_display_name, instance.instance_name)
        containerName       = instance.container_name
        appName             = instance.app_name
        metricInstanceName  = instance.metric_instance_name
        ignoreFlag          = instance.ignore_flag
      }
    ]

    metricSettings = [
      for metric in each.value.metrics : {
        metricName                         = metric.metric_name
        escalateIncidentAll                = metric.escalate_incident_all
        thresholdAlertLowerBound           = metric.threshold_alert_lower_bound
        thresholdAlertUpperBound           = metric.threshold_alert_upper_bound
        thresholdAlertUpperBoundNegative   = metric.threshold_alert_upper_bound_negative
        thresholdAlertLowerBoundNegative   = metric.threshold_alert_lower_bound_negative
        thresholdNoAlertLowerBound         = metric.threshold_no_alert_lower_bound
        thresholdNoAlertUpperBound         = metric.threshold_no_alert_upper_bound
        thresholdNoAlertLowerBoundNegative = metric.threshold_no_alert_lower_bound_negative
        thresholdNoAlertUpperBoundNegative = metric.threshold_no_alert_upper_bound_negative
      }
    ]
  })
}

# Apply configurations using null_resource
resource "null_resource" "apply_project_config" {
  for_each = local.project_configs

  triggers = {
    config_file = local_file.project_configs[each.key].content_md5
    base_url    = var.insightfinder_base_url
    username    = var.insightfinder_username
  }

  provisioner "local-exec" {
    command = "${path.module}/scripts/apply-single-config.sh"
    environment = {
      CONFIG_FILE  = local_file.project_configs[each.key].filename
      PROJECT_NAME = each.key
      BASE_URL     = var.insightfinder_base_url
      USERNAME     = var.insightfinder_username
      PASSWORD     = var.insightfinder_password
    }
  }

  depends_on = [local_file.project_configs]
}

# Add delay between requests
resource "time_sleep" "request_delay" {
  create_duration = "1s"
  depends_on      = [null_resource.apply_project_config]
}

# Output the results
output "project_configurations" {
  description = "Status of project configurations"
  value = {
    for project_name, config in local.project_configs : project_name => {
      project_name    = project_name
      configured_at   = timestamp()
      instances_count = length(config.instances)
      metrics_count   = length(config.metrics)
    }
  }
  depends_on = [null_resource.apply_project_config]
}

output "authentication_status" {
  description = "Configuration summary"
  sensitive   = true
  value = {
    base_url        = var.insightfinder_base_url
    username        = var.insightfinder_username
    projects_count  = length(local.project_configs)
    total_instances = sum([for config in local.project_configs : length(config.instances)])
    total_metrics   = sum([for config in local.project_configs : length(config.metrics)])
  }
}