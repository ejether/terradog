
resource "datadog_monitor" "test_host_disk_usage_high" {
  # Required Arguments
  name = "[test] Host Disk Usage High"
  type = "query alert"

  message = <<EOF
  {{#is_alert}}
Disk Usage has been above threshold over 30 minutes on {{host.name}}
{{/is_alert}}
{{#is_warning}}
Disk Usage has been above threshold over 30 minutes on {{host.name}}
{{/is_warning}}
{{^is_alert}}
Disk Usage has recovered on {{host.name}}
{{/is_alert}}
{{^is_warning}}
Disk Usage has recovered on {{host.name}}
{{/is_warning}}
@slack

  EOF
  query   = "avg(last_30m):( avg:system.disk.total{cluster_tag:test_cluster_name} by {host} - avg:system.disk.free{cluster_tag:test_cluster_name} by {host} ) / avg:system.disk.total{cluster_tag:test_cluster_name} by {host} * 100 > 95"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical          = 95
    warning           = 92
    warning_recovery  = 91
    critical_recovery = 94
  }
  require_full_window = true
  tags                = ["test", "hardware"]
}
