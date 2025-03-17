from http.client import OK
from typing import Self

import aiohttp

from apps.routes.domain.point import Points
from apps.routes.domain.route import TransportType
from core.config import settings
from core.exceptions import BaseError


class ValhallaApiGatewayImpl:
    async def _request(self: Self, json_request: dict) -> str:
        async with aiohttp.request(
            "post",
            url=settings.gateway.valhalla_request_url,
            json=json_request,
        ) as response:
            if response.status == OK:
                return await response.json()
            raise BaseError(
                status_code=response.status,
                detail="Маршрут не найден"
            )


    async def valhalla_request(
            self: Self,
            points: Points,
            transport_type: TransportType = TransportType.AUTO,
            *,
            units: str = "kilometres",
            language: str = "ru",
            directions_type: str = "maneuvers",
    ):
        json_request = {
            "locations": [0] * len(points),
            "costing": transport_type,
            "directions_options": {
                "units": units,
                "language": language,
                "directions_type": directions_type,
            },
        }
        for ind, _ in enumerate(json_request["locations"]):
            json_request["locations"][ind] = {
                "lat": points.points[ind].coord[0],
                "lon": points.points[ind].coord[1],
                "type": "break",
            }
        return await self._request(json_request=json_request)




