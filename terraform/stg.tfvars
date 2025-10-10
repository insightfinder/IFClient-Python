# Staging environment configuration
# This replaces the YAML configuration files from IFClient-Python

insightfinder_base_url = "https://stg.insightfinder.com"
insightfinder_username = "mustafa"
# insightfinder_password is set via environment variable: TF_VAR_insightfinder_password

projects = {
  "staging-log-project" = {
    project_display_name = "Staging Log Project"
    c_value              = 1
    p_value              = 0.95
    show_instance_down   = true
    retention_time       = 90
    ubl_retention_time   = 45

    instances = [
      {
        instance_name         = "STAGING_WEB"
        instance_display_name = "Staging Web Server"
        container_name        = "staging-web"
        app_name              = "web-frontend"
        ignore_flag           = false
      },
      {
        instance_name         = "STAGING_API"
        instance_display_name = "Staging API Server"
        container_name        = "staging-api"
        app_name              = "backend-api"
        ignore_flag           = false
      }
    ]

    metrics = [
      {
        metric_name                             = "cpu_usage"
        escalate_incident_all                   = true
        threshold_alert_lower_bound             = 10
        threshold_alert_upper_bound             = 85
        threshold_alert_upper_bound_negative    = -15
        threshold_alert_lower_bound_negative    = -5
        threshold_no_alert_lower_bound          = 40
        threshold_no_alert_upper_bound          = 70
        threshold_no_alert_lower_bound_negative = 15
        threshold_no_alert_upper_bound_negative = 35
      },
      {
        metric_name                             = "memory_usage"
        escalate_incident_all                   = true
        threshold_alert_lower_bound             = 15
        threshold_alert_upper_bound             = 80
        threshold_alert_upper_bound_negative    = -10
        threshold_alert_lower_bound_negative    = -8
        threshold_no_alert_lower_bound          = 35
        threshold_no_alert_upper_bound          = 65
        threshold_no_alert_lower_bound_negative = 20
        threshold_no_alert_upper_bound_negative = 30
      }
    ]
  }

  "staging-metric-project" = {
    project_display_name = "Staging Metric Project"
    c_value              = 2
    p_value              = 0.92
    show_instance_down   = false
    retention_time       = 120
    ubl_retention_time   = 60

    instances = [
      {
        instance_name         = "STAGING_DB"
        instance_display_name = "Staging Database"
        container_name        = "staging-postgres"
        app_name              = "database"
        ignore_flag           = false
      },
      {
        instance_name         = "STAGING_CACHE"
        instance_display_name = "Staging Cache"
        container_name        = "staging-redis"
        app_name              = "cache"
        ignore_flag           = false
      }
    ]

    metrics = [
      {
        metric_name                             = "response_time"
        escalate_incident_all                   = true
        threshold_alert_lower_bound             = 50
        threshold_alert_upper_bound             = 1000
        threshold_alert_upper_bound_negative    = -25
        threshold_alert_lower_bound_negative    = -10
        threshold_no_alert_lower_bound          = 100
        threshold_no_alert_upper_bound          = 500
        threshold_no_alert_lower_bound_negative = 5
        threshold_no_alert_upper_bound_negative = 15
      },
      {
        metric_name                    = "error_rate"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 1
        threshold_alert_upper_bound    = 10
        threshold_no_alert_lower_bound = 0
        threshold_no_alert_upper_bound = 5
      }
    ]
  }
}