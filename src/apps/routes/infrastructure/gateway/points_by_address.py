import asyncio
from http.client import OK
from typing import Iterable, Self

import aiohttp

from apps.routes.domain.point import Point, Points, PointType
from core.config import settings
from core.exceptions import BaseError


class NominatimApiGatewayImpl:
    async def _request(self: Self, address: str) -> Point:
        url = settings.gateway.nominatim_request_url(address)
        async with self.session.get(url=url) as response:
            if response.status == OK:
                data = await response.json()
                if data:
                    lat = data[0]["lat"]
                    lon = data[0]["lon"]
                    return Point(
                        coord=(float(lat), float(lon)),
                        type=PointType.INITIAL,
                    )
                raise BaseError(status_code=404, detail=f"Address {address!r} not found")
            error_text = await response.text()
            raise BaseError(
                status_code=response.status,
                detail=f"{error_text}",
            )


    async def get_points(self: Self, addresses: Iterable[str]) -> Points:
        async with aiohttp.ClientSession() as self.session:
            tasks = [
                asyncio.create_task(self._request(address=address))
                for address in addresses
            ]
            point_list = await asyncio.gather(*tasks)
            return Points(point_list)



