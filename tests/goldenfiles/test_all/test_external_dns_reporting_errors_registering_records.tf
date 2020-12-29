
resource "datadog_monitor" "test_external_dns_reporting_errors_registering_records" {
  # Required Arguments
  name = "[test] external-dns reporting errors registering records"
  type = "metric alert"

  message = <<EOF
  {{#is_warning}}
The external-dns controller is reporting registry errors.
- Is there a conflicting record in the registry (e.g. an existing CNAME)?
- Does external-dns have proper permissions to access the registry?

Check the logs of external-dns for more information.
@slack
{{/is_warning}}
{{#is_recovery}}
@slack
{{/is_recovery}}

  EOF
  query   = "sum(last_15m):max:external_dns.registry_errors_total{cluster_tag:test_cluster_name}.as_count() > 1000"

  # Optional Arguments
  new_host_delay = 300
  thresholds = {
    critical = 1000
    warning  = 1
  }
  tags = ["network", "test"]
}
