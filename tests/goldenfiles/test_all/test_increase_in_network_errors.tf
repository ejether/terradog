
resource "datadog_monitor" "test_increase_in_network_errors" {
  # Required Arguments
  name = "[test] Increase in network errors"
  type = "metric alert"

  message = <<EOF
  {{#is_alert}}
We are getting increasing network errors
{{/is_alert}}
@slack

  EOF
  query   = "avg(last_15m):avg:kubernetes.network.rx_errors{cluster_tag:test_cluster_name} + avg:kubernetes.network.tx_errors{cluster_tag:test_cluster_name} > 10"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 10
    warning  = 5
  }
  require_full_window = true
  tags                = ["network", "test"]
}
