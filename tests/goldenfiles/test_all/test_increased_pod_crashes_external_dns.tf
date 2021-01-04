
resource "datadog_monitor" "test_increased_pod_crashes_external_dns" {
  # Required Arguments
  name = "[test] Increased pod crashes external-dns"
  type = "metric alert"

  message = <<EOF
  {{#is_alert}}
{{pod.name}} has crashed repeatedly over the last hour
{{/is_alert}}
{{^is_alert}}
{{pod.name}} appears to have stopped crashing
{{/is_alert}}
@slack

  EOF
  query   = "change(avg(last_5m),last_1h):max:kubernetes_state.container.restarts{cluster_tag:test_cluster_name,namespace:external-dns,!container:metadata-agent,!container:prometheus-to-sd,!container:fluentd-gcp} by {pod} >= 1"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 1
  }
  include_tags = true
  tags         = ["test"]
}
