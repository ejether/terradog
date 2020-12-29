
resource "datadog_monitor" "test_external_dns_reporting_errors_with_sources_kubernetes" {
  # Required Arguments
  name = "[test] external-dns reporting errors with sources (kubernetes)."
  type = "metric alert"

  message = <<EOF
  {{#is_warning}}
The external-dns controller is reporting source errors.
Most likely a kubernetes object was deployed with a misconfiguration regarding external-dns.

Check the logs of external-dns for more information.
@slack
{{/is_warning}}
{{#is_recovery}}
@slack
{{/is_recovery}}

  EOF
  query   = "sum(last_15m):max:external_dns.source_errors_total{cluster_tag:test_cluster_name}.as_count() > 10"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 10
    warning  = 1
  }
  tags = ["network", "test"]
}
