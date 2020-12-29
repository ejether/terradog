
resource "datadog_monitor" "test_i_o_wait_times_are_high" {
  # Required Arguments
  name = "[test] I/O wait times are high"
  type = "metric alert"

  message = <<EOF
  {{#is_alert}}
The I/O wait time for {host.ip} is very high
- Is the EBS volume out of burst capacity for iops?
- Is something writing lots of errors to the journal?
- Is there a pod doing something unexpected (crash looping, etc)?
{{/is_alert}}
{{^is_alert}}
The IO wait time is returning to normal.
{{/is_alert}}
@slack

  EOF
  query   = "avg(last_10m):avg:system.cpu.iowait{cluster_tag:test_cluster_name} by {host} > 50"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 50
    warning  = 30
  }
  require_full_window = true
  tags                = ["test"]
}
