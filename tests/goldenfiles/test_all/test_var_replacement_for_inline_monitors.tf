
resource "datadog_monitor" "test_var_replacement_for_inline_monitors" {
  # Required Arguments
  name = "test var replacement for inline monitors"
  type = "metric alert"

  message = <<EOF
  in-line-notifications

  EOF
  query   = "test_cluster_name foo test"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 10
    warning  = 5
  }
  require_full_window = true
  tags                = ["network", "test"]
}
