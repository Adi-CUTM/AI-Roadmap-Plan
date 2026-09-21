"""
Core data models for LogSentry.
Every parser normalizes raw log lines into a NormalizedEvent.
Every detection rule that fires produces an Alert.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, IPvAnyAddress


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    AUTHENTICATION = "authentication"
    NETWORK = "network"
    WEB = "web"
    SYSTEM = "system"
    FIREWALL = "firewall"
    CLOUD = "cloud"
    UNKNOWN = "unknown"


class NormalizedEvent(BaseModel):
    """
    Common schema every log source gets mapped into.
    Parsers ONLY produce this. Nothing downstream should
    know about the original log format.
    """

    # Identity / traceability
    event_id: str                              # hash or uuid, set by pipeline
    log_source: str                             # e.g. "ssh_auth", "nginx_access"
    raw_message: str                            # original untouched line

    # When
    timestamp: datetime

    # Who / where
    user: Optional[str] = None
    source_ip: Optional[IPvAnyAddress] = None
    dest_ip: Optional[IPvAnyAddress] = None
    source_port: Optional[int] = None
    dest_port: Optional[int] = None
    hostname: Optional[str] = None

    # What happened
    category: EventCategory = EventCategory.UNKNOWN
    action: Optional[str] = None                # e.g. "login_failed", "GET"
    status: Optional[str] = None                # e.g. "failure", "200", "denied"

    # Enrichment slots (filled later in pipeline, not by parser)
    geo_country: Optional[str] = None
    geo_city: Optional[str] = None
    asn: Optional[str] = None
    reverse_dns: Optional[str] = None
    threat_score: Optional[float] = None
    is_known_bad: bool = False

    # Escape hatch for parser-specific fields that don't fit the schema
    extra: dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = False  # pipeline mutates to add enrichment


class Alert(BaseModel):
    """Produced by the detection engine when a rule fires."""

    alert_id: str
    rule_name: str
    severity: Severity
    title: str
    description: str
    triggered_at: datetime
    matched_events: list[NormalizedEvent] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)