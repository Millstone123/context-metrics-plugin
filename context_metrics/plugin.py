"""Pytest lifecycle integration for session context reports."""

import time

from .bridge import start_bridge
from .metrics import SessionMetrics


class ContextMetricsPlugin:
    def __init__(self) -> None:
        self.metrics = SessionMetrics()
        self._phase_started = 0.0

    def pytest_configure(self, config) -> None:
        config._context_metrics = self.metrics
        self.metrics.start()

    def pytest_sessionstart(self, session) -> None:
        self._phase_started = time.monotonic()
        start_bridge()

    def pytest_collection_finish(self, session) -> None:
        self.metrics.record_collection(len(session.items))

    def pytest_runtest_logreport(self, report) -> None:
        if report.when == "call":
            self.metrics.record_phase(report.nodeid, report.duration)
            self.metrics.record_outcome(report.outcome)

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config) -> None:
        totals = self.metrics.totals()
        terminalreporter.write_sep("=", "context metrics")
        terminalreporter.write_line(
            "collected={collected} passed={passed} failed={failed} skipped={skipped}".format(**totals)
        )
        for phase, elapsed in self.metrics.slowest():
            terminalreporter.write_line("{elapsed:8.3f}s  {phase}".format(elapsed=elapsed, phase=phase))


def pytest_configure(config) -> None:
    plugin = ContextMetricsPlugin()
    config.pluginmanager.register(plugin, "context-metrics")
    plugin.pytest_configure(config)
