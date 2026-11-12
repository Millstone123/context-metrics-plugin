from context_metrics.plugin import ContextMetricsPlugin


class _Config:
    pass


def test_plugin_starts_only_when_configured():
    plugin = ContextMetricsPlugin()
    assert plugin.metrics.started is False
    plugin.pytest_configure(_Config())
    assert plugin.metrics.started is True
