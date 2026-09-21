"""
Parser registry — auto-discovers and routes log lines to the right parser.
Add a new parser file in parsers/ and register it here (or via decorator).
"""

from logsentry.parsers.base import BaseParser
from logsentry.core.exceptions import NoMatchingParserError
from logsentry.utils.logger import get_logger

logger = get_logger("parsers.registry")


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: list[BaseParser] = []

    def register(self, parser: BaseParser) -> None:
        logger.info(f"Registering parser: {parser.name}")
        self._parsers.append(parser)

    def get_parser_for_line(self, raw_line: str) -> BaseParser:
        for parser in self._parsers:
            if parser.can_parse(raw_line):
                return parser
        raise NoMatchingParserError(f"No parser matched line: {raw_line!r}")

    def get_by_name(self, name: str) -> BaseParser:
        for parser in self._parsers:
            if parser.name == name:
                return parser
        raise NoMatchingParserError(f"No parser registered with name: {name}")

    @property
    def registered_names(self) -> list[str]:
        return [p.name for p in self._parsers]


# Shared registry instance
registry = ParserRegistry()


def bootstrap_parsers() -> ParserRegistry:
    """
    Explicit registration (safer & more debuggable than magic auto-import).
    Called once at startup from cli.py.
    """
    from logsentry.parsers.ssh_auth_parser import SSHAuthParser
    from logsentry.parsers.nginx_parser import NginxParser
    from logsentry.parsers.apache_parsers import ApacheParser

    registry.register(SSHAuthParser())
    registry.register(NginxParser())
    registry.register(ApacheParser())

    return registry