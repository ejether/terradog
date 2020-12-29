
resource "datadog_monitor" "test_node_is_not_ready" {
  # Required Arguments
  name = "[test] Node is not Ready"
  type = "service check"

  message = <<EOF
  {{#is_warning}}
A Node is not ready!
Cluster: {{cluster_tag.name}}
Host: {{host.name}}
IP: {{host.ip}}
{{check_message}}
{{/is_warning}}
{{#is_alert}}
A Node is not ready!
Cluster: {{cluster_tag.name}}
Host: {{host.name}}
IP: {{host.ip}}
{{check_message}}
{{/is_alert}}
{{#is_recovery}}
Node is now ready.
Cluster: {{cluster_tag.name}}
Host: {{host.name}}
IP: {{host.ip}}
{{/is_recovery}}
@slack

  EOF
  query   = "\"kubernetes_state.node.ready\".over(\"cluster_tag:test_cluster_name\").by(\"node\").last(20).count_by_status()"

  # Optional Arguments
  no_data_timeframe = 2
  new_host_delay    = 900
  thresholds = {
    critical = 20
    warning  = 9
    ok       = 2
  }
  tags = ["test"]
}
