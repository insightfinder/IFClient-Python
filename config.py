# Configurations
base_url = "https://stg.insightfinder.com"
username = "maoyuwang"
password = ""
systemID = "e802b01d8339176d8dcfc58493813e28e520d615"
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

project_keywords_settings = [{"type":"fieldName",
                              "keyword":"name=^(?!.*(High ICMP ping response time|Link down)).*$ AND value=1 AND severity=4|5",
                              "countThreshold":0,
                              "order":1,
                              "patternNameLabels":[{"type":"fieldName","order":1,"patternNameKey":"name"}]}]