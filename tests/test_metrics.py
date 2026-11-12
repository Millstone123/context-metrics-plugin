from context_metrics.metrics import SessionMetrics


def test_totals_and_slowest_phases():
    metrics = SessionMetrics()
    metrics.start()
    metrics.record_collection(5)
    metrics.record_outcome("passed")
    metrics.record_outcome("passed")
    metrics.record_outcome("failed")
    metrics.record_phase("a", 0.01)
    metrics.record_phase("b", 0.5)
    metrics.record_phase("c", 0.05)
    assert metrics.totals() == {"collected": 5, "passed": 2, "failed": 1, "skipped": 0}
    assert metrics.slowest(2)[0] == ("b", 0.5)


def test_negative_durations_are_clamped():
    metrics = SessionMetrics()
    metrics.record_phase("x", -1.0)
    assert metrics.slowest(1) == [("x", 0.0)]
