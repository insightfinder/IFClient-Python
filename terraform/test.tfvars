# Test configuration for sample project
# This is a test file to validate the Terraform configuration
# Replace with your actual values when using

insightfinder_base_url = "https://stg.insightfinder.com"
insightfinder_username = "your-username"
# insightfinder_password is set via environment variable: TF_VAR_insightfinder_password

projects = {
  "sample-project" = {
    project_display_name = "Sample Project Monitoring"
    c_value              = 2
    p_value              = 0.95
    show_instance_down   = true
    retention_time       = 120
    ubl_retention_time   = 60

    instances = [
      {
        instance_name         = "SAMPLE_NODE_1"
        instance_display_name = "Sample Node 1"
        container_name        = "sample-node-1"
        app_name              = "sample-app"
        ignore_flag           = false
      },
      {
        instance_name         = "SAMPLE_NODE_2"
        instance_display_name = "Sample Node 2"
        container_name        = "sample-node-2"
        app_name              = "sample-app"
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
      },
      {
        metric_name                            = "memory-usage"
        escalate_incident_all                  = true
        threshold_alert_lower_bound            = 10
        threshold_alert_upper_bound            = 95
        threshold_alert_lower_bound_negative   = -5
        threshold_alert_upper_bound_negative   = -15
        threshold_no_alert_lower_bound         = 20
        threshold_no_alert_upper_bound         = 85
        threshold_no_alert_lower_bound_negative = 10
        threshold_no_alert_upper_bound_negative = 20
      },
      {
        metric_name                            = "network-throughput"
        escalate_incident_all                  = true
        threshold_alert_lower_bound            = 10
        threshold_alert_upper_bound            = 1000
        threshold_alert_lower_bound_negative   = -5
        threshold_alert_upper_bound_negative   = -25
        threshold_no_alert_lower_bound         = 50
        threshold_no_alert_upper_bound         = 800
        threshold_no_alert_lower_bound_negative = 10
        threshold_no_alert_upper_bound_negative = 20
      }
    ]
  }
}
