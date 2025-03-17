from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.routes.domain.route import TransportType


@dataclass
class Edge:
    distance: float
    way_time: float


@dataclass
class Edges:
    transport_type: "TransportType"
    edges: list[Edge]
