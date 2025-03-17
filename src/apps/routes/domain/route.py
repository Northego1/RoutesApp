from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Self, Sequence

if TYPE_CHECKING:
    from apps.routes.domain.edge import Edges
    from apps.routes.domain.point import Points


class TransportType(str, Enum):
    AUTO = "auto"
    BICYCLE = "bicycle"
    PEDESTRIAN = "pedestrian"



@dataclass
class Route:
    points: "Points"
    edges: "Edges"
    transport_type: TransportType
    distance: float
    way_time: float




    def __len__(self: Self) -> int:
        return len(self.points)















class PointsMaker:
    def execute(self, coords: Sequence[float]) -> Sequence[Point]:
        ...


class EdgeMaker:
    def execure(self, points: Sequence[Point]) -> Sequence[Edge]:
        ...


class RouteMaker:
    def execute(self, points: Sequence[Point], edges: Sequence[Edge]) -> Route:
        ...


class RestSearcher:
    def execute(self, route: Route) -> list[Point]:
        ...
