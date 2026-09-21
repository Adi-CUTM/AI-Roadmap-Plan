"""
CLI entry point for LogSentry.
Run with: python -m logsentry.cli run --source /var/log/auth.log
"""

import typer
import yaml
from pathlib import Path

from logsentry.utils.logger import setup_logger, get_logger
from logsentry.core.checkpoint import CheckpointStore
from logsentry.core.pipeline import Pipeline
from logsentry.parsers.registry import bootstrap_parsers
from logsentry.detection.rule_engine import bootstrap_rules
from logsentry.ingestion.file_tailer import FileTailer
from logsentry.ingestion.batch_reader import BatchReader
from logsentry.output.console_output import ConsoleOutput
from logsentry.output.json_file_output import JsonFileOutput

app = typer.Typer(help="LogSentry — production log parsing & threat detection")


def _load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


@app.command()
def run(
    source: str = typer.Option(..., help="Path to the log file to monitor"),
    mode: str = typer.Option("tail", help="'tail' for real-time, 'batch' for one-time read"),
    config: str = typer.Option("config/config.yaml", help="Path to main config file"),
    log_level: str = typer.Option("INFO", help="Logging level"),
    alerts_file: str = typer.Option("data/alerts.ndjson", help="Where to write JSON alerts"),
):
    """Start the log parsing and detection pipeline on a single source."""
    setup_logger(level=log_level)
    logger = get_logger("cli")

    cfg = _load_config(config)
    logger.info(f"Starting LogSentry | source={source} | mode={mode}")

    parser_registry = bootstrap_parsers()
    logger.info(f"Loaded parsers: {parser_registry.registered_names}")

    rule_engine = bootstrap_rules(cfg.get("detection", {}))
    logger.info(f"Loaded rules: {rule_engine.registered_names}")

    if mode == "tail":
        checkpoint_store = CheckpointStore()
        ingestor = FileTailer(source, checkpoint_store=checkpoint_store)
    elif mode == "batch":
        ingestor = BatchReader(source)
    else:
        typer.echo(f"Unknown mode: {mode}. Use 'tail' or 'batch'.")
        raise typer.Exit(code=1)

    outputs = [
        ConsoleOutput(),
        JsonFileOutput(output_path=alerts_file),
    ]

    pipeline = Pipeline(
        ingestor=ingestor,
        parser_registry=parser_registry,
        rule_engine=rule_engine,
        outputs=outputs,
    )
    pipeline.run()


@app.command()
def list_parsers():
    """Show all registered parsers."""
    registry = bootstrap_parsers()
    for name in registry.registered_names:
        typer.echo(f"- {name}")


@app.command()
def list_rules(config: str = typer.Option("config/config.yaml")):
    """Show all registered detection rules."""
    cfg = _load_config(config)
    engine = bootstrap_rules(cfg.get("detection", {}))
    for name in engine.registered_names:
        typer.echo(f"- {name}")


if __name__ == "__main__":
    app()