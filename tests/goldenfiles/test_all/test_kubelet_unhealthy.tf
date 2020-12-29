
resource "datadog_monitor" "test_kubelet_unhealthy" {
  # Required Arguments
  name = "[test] Kubelet unhealthy"
  type = "service check"

  message = <<EOF
  {{#is_alert}}
Kubelet is in an unhealthy state.  Either the Kubelet's api is unavailable or Kubelet's sync loop that updates containers isn't working.
{{/is_alert}}
{{^is_alert}}
Kubelets are healthy again
{{/is_alert}}
@slack

  EOF
  query   = "\"kubernetes.kubelet.check\".over(\"cluster_tag:test_cluster_name\").by(\"host\").last(40).count_by_status()"

  # Optional Arguments
  no_data_timeframe = 2
  new_host_delay    = 300
  thresholds = {
    critical = 40
  }
  tags = ["test"]
}
