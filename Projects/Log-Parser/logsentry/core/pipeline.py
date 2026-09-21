"""
The pipeline is the single place where ingestion -> parsing -> detection
-> output are wired together. Keeping this orchestration in one file
(rather than scattered) means the whole data flow is readable top to bottom.
"""

from logsentry.ingestion.base import BaseIngestor
from logsentry.parsers.registry import ParserRegistry
from logsentry.detection.rule_engine import RuleEngine
from logsentry.output.base import BaseOutput
from logsentry.core.exceptions import NoMatchingParserError
from logsentry.utils.logger import get_logger
from logsentry.utils.metrics import metrics

logger = get_logger("core.pipeline")


class Pipeline:
    def __init__(
        self,
        ingestor: BaseIngestor,
        parser_registry: ParserRegistry,
        rule_engine: RuleEngine,
        outputs: list[BaseOutput],
        enrichers: list | None = None,
    ):
        self.ingestor = ingestor
        self.parser_registry = parser_registry
        self.rule_engine = rule_engine
        self.outputs = outputs
        self.enrichers = enrichers or []

    def run(self) -> None:
        logger.info("Pipeline starting")
        try:
            for raw_line in self.ingestor.stream():
                self._process_line(raw_line)
        except KeyboardInterrupt:
            logger.info("Pipeline stopped by user (Ctrl+C)")
        finally:
            self.ingestor.close()
            for output in self.outputs:
                output.close()
            logger.info("Pipeline shut down cleanly")

    def _process_line(self, raw_line: str) -> None:
        metrics.incr("events_ingested")

        try:
            parser = self.parser_registry.get_parser_for_line(raw_line)
        except NoMatchingParserError:
            logger.debug(f"No parser matched line, skipping: {raw_line!r}")
            metrics.incr("parse_failures")
            return

        event = parser.parse_safe(raw_line)
        if event is None:
            metrics.incr("parse_failures")
            return

        metrics.incr("events_parsed")

        # Enrichment (GeoIP, threat intel, etc.)
        for enricher in self.enrichers:
            try:
                event = enricher.enrich(event)
            except Exception as e:  # noqa: BLE001
                logger.warning(f"Enrichment '{enricher.name}' failed for event {event.event_id}: {e}")
        metrics.incr("events_enriched")

        # Detection
        alerts = self.rule_engine.evaluate(event)

        # Output
        for alert in alerts:
            for output in self.outputs:
                try:
                    output.send_alert(alert)
                except Exception as e:  # noqa: BLE001
                    metrics.incr("output_failures")
                    logger.error(f"Output '{output.name}' failed to send alert {alert.alert_id}: {e}")