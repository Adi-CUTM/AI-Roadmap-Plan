"""
Prints alerts to the console with color-coded severity — useful for
local dev/debugging and for running LogSentry interactively.
"""

from rich.console import Console
from rich.panel import Panel

from logsentry.output.base import BaseOutput
from logsentry.core.schema import Alert, Severity

_SEVERITY_COLORS = {
    Severity.INFO: "cyan",
    Severity.LOW: "green",
    Severity.MEDIUM: "yellow",
    Severity.HIGH: "bold red",
    Severity.CRITICAL: "bold white on red",
}


class ConsoleOutput(BaseOutput):
    name = "console"

    def __init__(self):
        self.console = Console()

    def send_alert(self, alert: Alert) -> None:
        color = _SEVERITY_COLORS.get(alert.severity, "white")
        body = (
            f"[bold]{alert.description}[/bold]\n\n"
            f"Rule: {alert.rule_name}\n"
            f"Triggered: {alert.triggered_at}\n"
            f"Tags: {', '.join(alert.tags)}"
        )
        self.console.print(
            Panel(body, title=f"[{color}]{alert.title}[/{color}]", border_style=color)
        )