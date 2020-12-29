
resource "datadog_monitor" "test_clock_in_sync_with_ntp" {
  # Required Arguments
  name = "[test] Clock in sync with NTP"
  type = "service check"

  message = <<EOF
  Triggers if any host's clock goes out of sync with the time given by NTP.
@slack

  EOF
  query   = "\"ntp.in_sync\".over(\"cluster_tag:test_cluster_name\").by(\"host\").last(6).count_by_status()"

  # Optional Arguments
  no_data_timeframe = 2
  new_host_delay    = 300
  thresholds = {
    warning  = 3
    ok       = 1
    critical = 5
  }
  tags = ["test"]
}
