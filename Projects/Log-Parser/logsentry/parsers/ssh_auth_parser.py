"""
Parser for SSH authentication logs (Linux /var/log/auth.log or
/var/log/secure). Covers the most security-relevant lines:
failed password, accepted password, accepted publickey, invalid user.
"""

import re
from datetime import datetime

from logsentry.parsers.base import BaseParser
from logsentry.core.schema import NormalizedEvent, EventCategory
from logsentry.core.exceptions import ParseError
from logsentry.utils.time_utils import parse_timestamp
import hashlib


# Example lines this parser handles:
# Sep 21 09:14:02 myhost sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 51514 ssh2
# Sep 21 09:14:10 myhost sshd[1234]: Accepted password for root from 203.0.113.5 port 51520 ssh2
# Sep 21 09:14:15 myhost sshd[1234]: Accepted publickey for deploy from 10.0.0.5 port 40012 ssh2

_SSH_LINE_RE = re.compile(
    r"^(?P<ts>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+"
    r"sshd\[\d+\]:\s+"
    r"(?P<result>Failed password|Accepted password|Accepted publickey|Invalid user|Failed publickey)"
    r"(?:\s+for)?"
    r"(?:\s+(?P<invalid>invalid user))?"
    r"\s+(?P<user>\S+)\s+"
    r"from\s+(?P<src_ip>[\d.:a-fA-F]+)\s+"
    r"port\s+(?P<port>\d+)"
)


class SSHAuthParser(BaseParser):
    name = "ssh_auth"

    def can_parse(self, raw_line: str) -> bool:
        return "sshd[" in raw_line and (
            "Failed password" in raw_line
            or "Accepted password" in raw_line
            or "Accepted publickey" in raw_line
            or "Invalid user" in raw_line
        )

    def parse(self, raw_line: str) -> NormalizedEvent:
        match = _SSH_LINE_RE.search(raw_line)
        if not match:
            raise ParseError("SSH auth line did not match expected pattern",
                              raw_line=raw_line, parser_name=self.name)

        gd = match.groupdict()

        try:
            # syslog timestamps have no year — assume current year
            ts = parse_timestamp(f"{gd['ts']} {datetime.now().year}", assume_utc=False)
        except ValueError as e:
            raise ParseError(str(e), raw_line=raw_line, parser_name=self.name) from e

        result = gd["result"]
        is_failure = result in ("Failed password", "Invalid user", "Failed publickey")

        event_id = hashlib.sha256(raw_line.encode()).hexdigest()[:16]

        return NormalizedEvent(
            event_id=event_id,
            log_source=self.name,
            raw_message=raw_line,
            timestamp=ts,
            user=gd["user"],
            source_ip=gd["src_ip"],
            source_port=int(gd["port"]),
            hostname=gd["host"],
            category=EventCategory.AUTHENTICATION,
            action="login_attempt",
            status="failure" if is_failure else "success",
            extra={"auth_method": "publickey" if "publickey" in result else "password",
                   "invalid_user": bool(gd["invalid"])},
        )