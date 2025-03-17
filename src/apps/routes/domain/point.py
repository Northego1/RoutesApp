from dataclasses import dataclass
from enum import Enum
from typing import Self

from apps.routes.domain.edge import Edges
from apps.routes.domain.route import Route


class PointType(str, Enum):
    REST = "rest"
    INITIAL = "initial"


@dataclass
class Point:
    coord: tuple[float, float]
    type: PointType


@dataclass
class Points:
    points: list[Point]

    def __add__(self: Self, other: "Edges") -> "Route":
        if isinstance(other, Edges) and len(other.edges) == len(self.points) - 1:
            return Route(
                points=self,
                edges=other,
                transport_type=other.transport_type,
                distance=sum(edge.distance for edge in other.edges),
                way_time=sum(edge.way_time for edge in other.edges),
            )
        raise ValueError("Invalid combination of points and edges")


    def __radd__(self: Self, other: "Edges") -> "Route":
        return self.__add__(other)


    def __len__(self: Self) -> int:
        return len(self.points)
