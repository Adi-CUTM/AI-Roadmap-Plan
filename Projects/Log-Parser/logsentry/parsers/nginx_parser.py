"""
Parser for Nginx access logs in the standard "combined" log format:
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
"""

import re
import hashlib
from logsentry.parsers.base import BaseParser
from logsentry.core.schema import NormalizedEvent, EventCategory
from logsentry.core.exceptions import ParseError
from logsentry.utils.time_utils import parse_timestamp

# Example:
# 203.0.113.7 - - [21/Sep/2026:09:15:32 +0000] "GET /wp-login.php HTTP/1.1" 404 162 "-" "curl/7.68.0"

_NGINX_RE = re.compile(
    r'^(?P<ip>[\d.:a-fA-F]+)\s+-\s+(?P<user>\S+)\s+'
    r'\[(?P<ts>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+HTTP/[\d.]+"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\d+)\s+'
    r'"(?P<referer>[^"]*)"\s+"(?P<agent>[^"]*)"'
)


class NginxParser(BaseParser):
    name = "nginx_access"

    def can_parse(self, raw_line: str) -> bool:
        return bool(_NGINX_RE.search(raw_line))

    def parse(self, raw_line: str) -> NormalizedEvent:
        match = _NGINX_RE.search(raw_line)
        if not match:
            raise ParseError("Nginx line did not match combined log format",
                              raw_line=raw_line, parser_name=self.name)

        gd = match.groupdict()
        try:
            ts = parse_timestamp(gd["ts"].replace(":", " ", 1))
        except ValueError as e:
            raise ParseError(str(e), raw_line=raw_line, parser_name=self.name) from e

        event_id = hashlib.sha256(raw_line.encode()).hexdigest()[:16]
        status_code = int(gd["status"])

        return NormalizedEvent(
            event_id=event_id,
            log_source=self.name,
            raw_message=raw_line,
            timestamp=ts,
            source_ip=gd["ip"],
            user=None if gd["user"] == "-" else gd["user"],
            category=EventCategory.WEB,
            action=f"{gd['method']} {gd['path']}",
            status=str(status_code),
            extra={
                "method": gd["method"],
                "path": gd["path"],
                "status_code": status_code,
                "referer": gd["referer"],
                "user_agent": gd["agent"],
            },
        )