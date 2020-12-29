
resource "datadog_monitor" "test_nginx_config_reload_failure" {
  # Required Arguments
  name = "[test] Nginx Config Reload Failure"
  type = "metric alert"

  message = <<EOF
  {{#is_alert}}
The last nginx config reload for {{kube_deployment.name}} failed!  Are there any bad ingress configs?  Does the nginx config have a syntax error?
{{/is_alert}}
{{#is_recovery}}
Nginx config reloaded successfully!
{{/is_recovery}}
@slack

  EOF
  query   = "max(last_5m):max:ingress.nginx_ingress_controller_config_last_reload_successful{cluster_tag:test_cluster_name} by {kube_deployment} <= 0"

  # Optional Arguments
  notify_no_data = true
  new_host_delay = 300
  thresholds = {
    critical = 0
  }
  require_full_window = true
  tags                = ["test"]
}
