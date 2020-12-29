# terradog
Practical and Simple datadog resource generation with some sane defaults for dashboards and monitoring of Kubernetes infrastructure with Datadog.

## Requirements
- `>= python3.7`
or
- Docker

## Installation
### pip



## Usage

### Setup

The top of the configuration yaml contains environment variables that are used throughout the monitors. It is important to note that `cluster` and `cluster_tag` in this configuration yaml must match the value of the `DD_CLUSTER_CHECKS_EXTRA_TAGS` variable set in the `datadog` hel in `course.yml`. We have also added a namespace definition that will be used by all monitors unless you specifically overwrite those values ([documented below](#definitions)). 

### Adding Resources 

The configuration yaml file above should be populated with all the resource we want to use. Currently supported are `monitors`, `timeboards`, `downtimes`.

Finally, when ready run:

`terradog create -f <source_file> -o <output_directory>`

which creates a uniquw terraform file in the output directory for each `monitor`, `timeboard`, or `downtime` according to the configuration of definitions and namespaces.

#### Native Monitors and Monitor Families

### [Monitors](/monitors.md)
There are several monitors included in this module and those are broken up into families such as `kubernetes-stable`, `kubernetes-optional`, `rds`, etc.(see below for a comprehensive list). If you wish to deploy all monitors in a family, you can simply call out the family name in the yaml file. The following snippet will create a terraform file for each of the monitors in the `kubernetes-stable` family. This should be done in the `monitors` section. You can see the current monitors (yaml files) under [monitors](/docs/rodd/monitors.md). See [Custom Monitors](#custom-monitors) to create new monitors.

```yaml
monitors:
  - source: kubernetes-stable
```

You can override individual values in the monitor as necessary. A complete list of fields is declared in [Custom Monitors](#custom-monitors).

This example will use all the defaults from the `kubernetes-stable.pod_crashes` monitor but override the `thresholds` field.

```yaml
monitors:
  - source: kubernetes-stable.pod_crashes
    pod_crashes_critical_threshold: 5
```
#### Custom Monitors
If the monitor you want doesn't exist as a native monitor in a monitor family you can define any monitor you want inline in the yaml file. This will create

```yaml
definitions:
  environment: "production"
  cluster: "production.cluster"
  notifications: "@pagerduty"
  cluster_tag: "kubernetescluster"
monitors:
  - notify_audit: false
    locked: false
    name: '[${environment}] Increase in network errors'
    tags: [network, '${environment}', fairwinds]
    include_tags: false
    no_data_timeframe: null
    silenced: {}
    new_host_delay: 300
    require_full_window: true
    notify_no_data: false
    renotify_interval: 0
    escalation_message: ''
    query: avg(last_15m):avg:kubernetes.network.rx_errors{kubernetescluster:${cluster}} + avg:kubernetes.network.tx_errors{kubernetescluster:${cluster}} > 10
    message: |
      {{#is_alert}}
      We are getting increasing network errors
      {{/is_alert}}
      ${notifications}
    type: metric alert
    thresholds: {critical: 10, warning: 5}
    timeout_h: 0
```

#### Definitions
Alluded to above, in each monitor and dashboard there are certain fields that need to be defined; `environment`, `cluster` are two examples.

They are denoted by `${<name>}` in the template and are referred to as "definitions". You can define definitions at a global level.

```yaml
definitions:
  cluster: working.cluster
  environment: production
  cluster_tag: kubernetescluster
monitors:
  - source: kubernetes-stable
```
or at an individual monitor level to override the global value.

```yaml
definitions:
  cluster: working.cluster
  environment: production
  cluster_tag: kubernetescluster
monitors:
  - source: kubernetes-stable
    definitions:
      environment: staging # this will override the global value
```

#### Namespaced Monitors

Datadog does not support multiple namespaces in monitor query filters. As a workaround, `terradog` monitors that include a namespace filter can generate multiple namespace specific monitors from a single monitor definition.

The underlying `terradog` monitor must have `vary_by_namespace: true` set. The monitor's namespaces definition must ba list. Each namespace definition value will produce a separate monitor and Terraform file.

Namespaces can be defined in 3 places: 

- There is a `definition_defaults` section create at the bottom of each monitor's yaml file. This is used if you do not specify a namespace at the top of your config file or within the `source`. 

```
definition_defaults:
  daemonset_readiness_critical_threshold: 0
  namespaces:
    - kube-system
```

- As mentioned in the [Native Monitors and Monitor Families](#Native-Monitors-and-Monitor-Families) section above, you can specify some settings within the `monitors` definition in the config file. This includes namespaces.

```
monitors:
  - source: kubernetes-optional.daemonset_readiness
    definitions:
      namespaces: 
      - cert-manager
```

- Lastly you can also add overall definitions to the top of config file`, including namespaces.
```
namespaces:
  - cert-manager
  - datadog
  - external-dns
  - kube-system
  - cluster-autoscaler
```

- Namespaces defined at the top of config file or within the `monitor` override whatever is in the `definition_defaults` in the ${monitor}.yaml.
- Namespaces defined within the `monitor` section of an individual monitor (`kubernetes-optional.daemonset_readiness` for example) are merged with the top-level definitions



#### Exclusions
Sometimes you'll want to apply all the monitors or dashboards in a family of except one or two. In this case, you can can use a list of `exclude` in family call. All the monitors or dashboards in that family will be templated except the ones listed in `exclude`. Just the path of the resource is required:

```yaml
monitors:
  - source: kubernetes-stable
    exclude:
    - cluster_iops
```


## Dashboard Fields
 Complete list of fields as taken from datadog tf [provider](https://www.terraform.io/docs/providers/datadog/r/timeboard.html)
- read_only
- description
- title
- graphs
- template_variables

## Downtime Fields
 Complete list of fields are taken from datadog tf [provider](https://www.terraform.io/docs/providers/datadog/r/downtime.html)
 - name - descriptive name for the downtime (not part of the downtime definition)
 - scope
 - active
 - start
 - end
 - start_date
 - end_date
 - recurrence_type
 - recurrence_period
 - recurrence_week_days
 - recurrence_until
 - message
 - monitor_id
 - monitor_tags

## References:
- https://www.terraform.io/docs/providers/datadog/index.html
- https://docs.datadoghq.com/monitors/
