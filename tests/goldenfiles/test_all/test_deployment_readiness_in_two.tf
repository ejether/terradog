
resource "datadog_monitor" "test_deployment_readiness_in_two" {
  # Required Arguments
  name = "[test] Deployment readiness in two"
  type = "query alert"

  message = <<EOF
  {{#is_alert}}
Unavailable replicas has been above 0 for {{deployment.name}}
{{/is_alert}}
{{^is_alert}}
Unavailable replicas is back to 0 for {{deployment.name}}
{{/is_alert}}
@slack

  EOF
  query   = "min(last_30m):max:kubernetes_state.deployment.replicas_unavailable{cluster_tag:test_cluster_name,namespace:two} by {deployment} > 0"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 0
  }
  include_tags = true
  tags         = ["test"]
}
