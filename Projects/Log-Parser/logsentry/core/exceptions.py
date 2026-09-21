"""Central exception hierarchy for LogSentry.
Keeping all exceptions in one place makes it easy for any layer
to catch broad or narrow failures consistently.
"""


class LogSentryError(Exception):
    """Base exception for all LogSentry errors."""


# --- Ingestion ---
class IngestionError(LogSentryError):
    """Raised when a log source can't be read/tailed/connected to."""


class SourceNotFoundError(IngestionError):
    """Raised when a configured log file/path doesn't exist."""


# --- Parsing ---
class ParseError(LogSentryError):
    """Raised when a parser fails to parse a line it claims to handle."""

    def __init__(self, message: str, raw_line: str = "", parser_name: str = ""):
        self.raw_line = raw_line
        self.parser_name = parser_name
        super().__init__(message)


class NoMatchingParserError(LogSentryError):
    """Raised when no registered parser can handle a given log line."""


# --- Enrichment ---
class EnrichmentError(LogSentryError):
    """Raised when an enrichment step fails (e.g. GeoIP DB missing)."""


# --- Detection ---
class RuleLoadError(LogSentryError):
    """Raised when a detection rule YAML/Sigma file is malformed."""


class RuleEvaluationError(LogSentryError):
    """Raised when a rule fails during evaluation against an event."""


# --- Output ---
class OutputError(LogSentryError):
    """Raised when an output sink fails to deliver (Slack, ES, file, etc.)."""


# --- Config ---
class ConfigError(LogSentryError):
    """Raised when config.yaml / sources.yaml is invalid or missing keys."""