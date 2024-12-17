# Configurations
base_url = "https://stg.insightfinder.com"
username = "maoyuwang"
password = ""
projectName = "maoyu-test-api-1"
user_agent = "Mozilla/5.0 (compatible; InsightFinderClient/1.0;)"

# Metric Project Settings:
metric_project_settings = {
    "cValue": 1,
    "pValue": 0.95,
    "showInstanceDown": False,
    "retentionTime": 11,
    "UBLRetentionTime": 11,
    "projectDisplayName": "Project-Display-Name",
    "instanceGroupingData": [
        {
            "instanceName": "instance1",
            "appName": "new-component1"
        },
        {
            "instanceName": "instance3",
            "ignoreFlag": True
        }
    ],
    "componentMetricSettingOverallModelList": [
        {
            "metricName": "metric1",
            "escalateIncidentAll": True,
            # The following thresholds can be null or empty, if empty just skip them or set to None
            "thresholdAlertLowerBound": None,
            "thresholdAlertUpperBound": 105,
            "thresholdAlertUpperBoundNegative": None,
            "thresholdAlertLowerBoundNegative": None,
            "thresholdNoAlertLowerBound": None,
            "thresholdNoAlertUpperBound": 75,
            "thresholdNoAlertLowerBoundNegative": None,
            "thresholdNoAlertUpperBoundNegative": None
        },
        {
            "metricName": "metric3",
            "escalateIncidentAll": True,
            "thresholdAlertLowerBound": 1,
            "thresholdAlertUpperBound": None,
            "thresholdAlertUpperBoundNegative": None,
            "thresholdAlertLowerBoundNegative": None,
            "thresholdNoAlertLowerBound": None,
            "thresholdNoAlertUpperBound": None,
            "thresholdNoAlertLowerBoundNegative": None,
            "thresholdNoAlertUpperBoundNegative": None
        }
    ]
}