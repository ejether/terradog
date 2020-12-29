
resource "datadog_downtime" "test_maintenance_window" {
  scope = ["*", ]
  start = 1614285704
  end   = 1645821704
  recurrence {
    type   = "days"
    period = 1
  }



  # Datadog API will reject dates in the past so let's ignore `start` and `end`
  # arguments during lifecycle. To update or extend an existing downtime, temporarily
  # remove the `ignore` section, apply timestamp changes, and re-apply the `ignore`
  # section.
  lifecycle {
    ignore_changes = ["start", "end"]
  }
}
