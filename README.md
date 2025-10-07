# IFClient-Python

A command-line tool to validate, merge, plan, and apply configuration files for InsightFinder projects.

## Installation

### From PyPI
Run the following command to install the tool:
```shell
pip install insightfinder-client
ifclient --help
```

### From Source
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ifclient.git
   cd ifclient
   ```

2. **Install Dependencies:**

   Using [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

   Or install in editable mode with pip:

   ```bash
   pip install -e .
   ```

## Usage
1. Create configurations files

Copy the folder under `docs/examples` to your current folder and edit the files.


3. Setup the InsightFinder credentials as environment variables.
```shell
export insightfinderusername_PASSWORD=insightfinderpassword
```

3. Valide the configuration files.

```shell
ifclient validate
```

4. Apply the configuration files in InsightFinder.
```shell
ifclient apply
```

## Recommended Configuration File Structure

Your configuration files are organized hierarchically. A typical structure is like this:

```
/config
|-- tool_config.yaml                # Base tool configuration
|-- /projects
|    |-- base1.yaml                 # Project base configuration
|    |-- base2.yaml
|-- /instance-grouping-settings
|    |-- grouping-data-1.yaml
|    |-- grouping-data-2.yaml
|-- /component-metric-settings
     |-- metric-setting-1.yaml
     |-- metric-setting-2.yaml

```

You can find examples for all of these in the docs/examples folder in the repository. These files can be used as a starting point.
The files are organised in the same way as show above. As mentiond before this is a recommonded but not a mandatory structure of organizing

## Configuration File Types
### toolConfig
toolConfig is the base configuration file. It contains the base URL for the deployment and the paths to the project base configurations.
```yaml
apiVersion: v1       # Configuration version 
type: toolConfig     # Schema validation type 
baseUrl: "stg.insightfinder.com"   # Base URL for deployment

projectBaseConfigs:
  - /path/to/project-config.yaml # Can be absolute or relative paths
  - /path/to/base/*.yaml # Wildcards are allowed
```

### projectBase
projectBase is the base configuration for a project. It contains the project name, display name,project level settings, and the paths to the grouping and metric settings.

```yaml
apiVersion: v1
type: projectBase
user: "user1"
project: "project_name"
projectDisplayName: "Project-Display-Name"
cValue: 1
pValue: 0.95
showInstanceDown: false
retentionTime: 11
UBLRetentionTime: 11
instanceGroupingData:
  files:
    - "../instance-grouping-data/grouping-data-1.yaml" # All file paths must be relative to the current file
    - "../instance-grouping-data/grouping-data-2.yaml"
consumerMetricSettingOverallModelList:
  files:
    - "../consumer-metric-setting/metric-setting-*.yaml"
```

### consumerMetricSetting
consumerMetricSetting stores the configuration for a metric project. It contains the metric name, incident escalation, and other threshold settings.
```yaml
apiVersion: v1
type: consumerMetricSetting
metricSettings:
  - metricName: "metric1"
    escalateIncidentAll: true
    thresholdAlertLowerBound: 15
    thresholdAlertUpperBound: 105
    thresholdAlertUpperBoundNegative: -20
    thresholdAlertLowerBoundNegative: -5
    thresholdNoAlertLowerBound: 50
    thresholdNoAlertUpperBound: 75
    thresholdNoAlertLowerBoundNegative: 20
    thresholdNoAlertUpperBoundNegative: 40

  - metricName: "metric2"
    escalateIncidentAll: true
    thresholdAlertLowerBound: 15
    thresholdAlertUpperBound: 105
    thresholdAlertUpperBoundNegative: -20
    thresholdAlertLowerBoundNegative: -5
    thresholdNoAlertLowerBound: 50
    thresholdNoAlertUpperBound: 75
    thresholdNoAlertLowerBoundNegative: 20
    thresholdNoAlertUpperBoundNegative: 40
```

### instanceGroupingSetting
instanceGroupingSetting contains the configuration for instance grouping. It contains the instance name, display name, component name, and other metadata for instances.
```yaml
apiVersion: v1
type: instanceGroupingSetting
instanceDataList:
  - instanceName: "CONFIRMED"
    instanceDisplayName: "Confirmed"
    containerName: "container"
    component: "component1"
    ignoreFlag: true
    
  - instanceName: "NEW"
    instanceDisplayName: "New"
    ignoreFlag: false

```
## Commands

The tool provides several commands:

- **validate:** Validate all provided configuration files.
- **generate:** Merge configurations into one output file.
- **apply:** Apply the merged configuration via API calls.

### Examples

```bash
# Validate configuration files in a directory
ifclient validate # Searches for all toolConfigs in current directory and recursively validates them
ifclient validate /path/to/configs # Validation with directory to search for all toolConfigs and apply validation recursively
ifclient validate /path/to/configs/config.yaml # Validation of any file and its subconfigs recursively(Need not be of type tool config)

# Generate a merged configuration file
ifclient generate /path/to/configs/config.yaml /path/to/outputs/output.yaml # Generate a yaml file as output with input of a toolConfig file

# Apply the merged configuration via API call
ifclient apply # Searches for all toolConfig files in current directory and recursively applies them
ifclient apply /path/to/configs # Searches for all toolConfig files in the specified directory and applies them recursively
ifclient apply /path/to/configs/config.yaml # Appies file and its subconfigs recursively
```

## Environment Variables

Before running the tool, ensure that sensitive passwords are available as environment variables. The naming convention should be:

```
ifusername_PASSWORD
```

For example, if your InsightFinder username is `jdoe`, set the environment variable:

```bash
export jdoe_PASSWORD=your_password_here
```
