
resource "datadog_monitor" "test_daemonset_readiness_in_fake_namespace" {
  # Required Arguments
  name = "[test] Daemonset readiness in fake-namespace"
  type = "query alert"

  message = <<EOF
  {{#is_alert}}
Daemonset pods are either out of date or not ready for {{daemonset.name}}
Check that `kubectl get ds` shows the same number for Desired/Current/Ready/Up-to-date/Available.
{{/is_alert}}
{{^is_alert}}
Daemonset pods are Up-to-Date and Ready for {{daemonset.name}}
{{/is_alert}}
@slack

  EOF
  query   = "min(last_30m):2 * max:kubernetes_state.daemonset.desired{cluster_tag:test_cluster_name,namespace:fake-namespace} by {daemonset} - max:kubernetes_state.daemonset.updated{cluster_tag:test_cluster_name,namespace:fake-namespace} by {daemonset} - max:kubernetes_state.daemonset.ready{cluster_tag:test_cluster_name,namespace:fake-namespace} by {daemonset} > 0"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 0
  }
  include_tags = true
  tags         = ["test"]
}
