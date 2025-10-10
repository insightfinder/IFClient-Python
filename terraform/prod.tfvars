# Production configuration
insightfinder_base_url = "https://app.insightfinder.com"
insightfinder_username = "produser1"

projects = {
  "production-web-logs" = {
    project_display_name = "Production Web Application Logs"
    c_value              = 1
    p_value              = 0.98
    show_instance_down   = true
    retention_time       = 365
    ubl_retention_time   = 180

    instances = [
      {
        instance_name         = "WEB_01"
        instance_display_name = "Web Server 01"
        container_name        = "web-app"
        app_name              = "web-frontend"
        ignore_flag           = false
      },
      {
        instance_name         = "WEB_02"
        instance_display_name = "Web Server 02"
        container_name        = "web-app"
        app_name              = "web-frontend"
        ignore_flag           = false
      },
      {
        instance_name         = "API_01"
        instance_display_name = "API Server 01"
        container_name        = "api-service"
        app_name              = "backend-api"
        ignore_flag           = false
      }
    ]

    metrics = [
      {
        metric_name                    = "error_rate"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 1
        threshold_alert_upper_bound    = 5
        threshold_no_alert_lower_bound = 0
        threshold_no_alert_upper_bound = 2
      },
      {
        metric_name                    = "response_time_p95"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 500
        threshold_alert_upper_bound    = 2000
        threshold_no_alert_lower_bound = 100
        threshold_no_alert_upper_bound = 800
      }
    ]
  }

  "production-infrastructure-metrics" = {
    project_display_name = "Production Infrastructure Metrics"
    c_value              = 2
    p_value              = 0.95
    show_instance_down   = true
    retention_time       = 730
    ubl_retention_time   = 365

    instances = [
      {
        instance_name         = "DB_PRIMARY"
        instance_display_name = "Database Primary"
        container_name        = "postgresql"
        app_name              = "database"
        ignore_flag           = false
      },
      {
        instance_name         = "DB_REPLICA"
        instance_display_name = "Database Replica"
        container_name        = "postgresql"
        app_name              = "database"
        ignore_flag           = false
      },
      {
        instance_name         = "CACHE_01"
        instance_display_name = "Redis Cache 01"
        container_name        = "redis"
        app_name              = "cache"
        ignore_flag           = false
      }
    ]

    metrics = [
      {
        metric_name                    = "cpu_utilization"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 10
        threshold_alert_upper_bound    = 85
        threshold_no_alert_lower_bound = 20
        threshold_no_alert_upper_bound = 70
      },
      {
        metric_name                    = "memory_utilization"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 15
        threshold_alert_upper_bound    = 90
        threshold_no_alert_lower_bound = 25
        threshold_no_alert_upper_bound = 75
      },
      {
        metric_name                    = "disk_utilization"
        escalate_incident_all          = true
        threshold_alert_lower_bound    = 20
        threshold_alert_upper_bound    = 85
        threshold_no_alert_lower_bound = 30
        threshold_no_alert_upper_bound = 70
      }
    ]
  }
}