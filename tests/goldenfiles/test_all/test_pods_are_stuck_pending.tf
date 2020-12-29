
resource "datadog_monitor" "test_pods_are_stuck_pending" {
  # Required Arguments
  name = "[test] Pods are stuck Pending"
  type = "metric alert"

  message = <<EOF
  {{#is_alert}}
There has been at least 1 pod Pending for 30 minutes.
There are currently {{value}} pods Pending.
  - Is something crash-looping?
  - Is autoscaling adding node capacity where needed?
  - Is a secret or a configmap missing?
{{/is_alert}}
{{^is_alert}}
Pods are no longer pending.
{{/is_alert}}
@slack

  EOF
  query   = "min(last_30m):sum:kubernetes_state.pod.status_phase{cluster_tag:test_cluster_name,phase:running} - sum:kubernetes_state.pod.status_phase{cluster_tag:test_cluster_name,phase:running} + sum:kubernetes_state.pod.status_phase{cluster_tag:test_cluster_name,phase:pending}.fill(zero) >= 1"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 1
  }
  require_full_window = true
  tags                = ["test"]
}
