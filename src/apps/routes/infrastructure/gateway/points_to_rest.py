import asyncio
from collections import deque
from typing import Annotated, Optional, Protocol, Self

import aiohttp
from fastapi import Depends, HTTPException

from api.v1.main_app.schemas.schemeMap import PlaceAddress, Point, PointType, RestPlace, RestPlaceInfo
from logger import get_logger
from config import settings


logger = get_logger(__name__)



class OverpassApiGatewayImpl:
    def __init__(self: Self):
        self.rest_places: list[RestPlace] = []


    async def _find_hotel_by_coords(
            self: Self,
            index:int,
            coord: tuple[int, list[float]],
            radius: int,
    ) -> Optional[RestPlace]: 
        request_data = f"""
                    [out:json];
                    (
                        node["tourism"~"hotel|motel|guest_house"](
                            around:{radius},{coord[0]},{coord[1]}
                        );
                        way["tourism"~"hotel|motel|guest_house"](
                            around:{radius},{coord[0]},{coord[1]}
                        );
                        relation["tourism"~"hotel|motel|guest_house"](
                            around:{radius},{coord[0]},{coord[1]}
                        );
                    );
                    out center;
                """      
        logger.debug(f'Обращение к API overpass по радусу {radius}')
        async with self.session.get(
            url=settings.gateway.overpass_request_url,
            params={'data': request_data}
        ) as response:
            if response.status >= 300:
                logger.error(f'Ошибка ответа overpass')
                raise HTTPException(408, detail='overpass error')
            response_data = await response.json()
            if response_data['elements']:
                for elem in response_data['elements']:
                    try:
                        place = RestPlace(
                            point=Point(
                                coord=(elem['lat'], elem['lon']),
                                type=PointType.REST,
                                index=index
                            ),
                            place=RestPlaceInfo(
                                type=elem['tags'].get('tourism', 'motel'),
                                name=elem['tags'].get('name:be') or elem['tags'].get('name', ''),
                                address=PlaceAddress(
                                    city=elem['tags'].get('addr:city', ''),
                                    street=elem['tags'].get('addr:street', ''),
                                    house_num=elem['tags'].get('addr:housenumber', '')
                                ),
                                phone=elem['tags'].get('phone', ''),
                                reservation=elem['tags'].get('reservation', '')
                            )
                        )
                    except KeyError:
                        logger.debug(f'Отсутствуют координаты отеля')
                        continue
                    logger.debug(f'Найден отель по координатам {place.point.coord}') 
                    return place
            logger.debug(f'Данные не найдены')
            return None       


    async def overpass_request(
            self: Self,
            rest_coords: dict[int, list[list]],
            rest_times: int,
            *,
            radius_increment: int = 2000,
    ) -> list[RestPlace]:
        async with aiohttp.ClientSession() as self.session:
            crds = list((
                (key, tuple(coords)) for key, value in rest_coords.items() 
                    if rest_coords[key]
                        for coords in value
            ))
            while radius_increment > 30000 or rest_times:
                tasks = []
                for pair in crds:
                    tasks.append(   
                        asyncio.create_task(
                            self._find_hotel_by_coords(
                                pair[0], pair[1], radius_increment
                            )
                        )
                    )
                options: list[Optional[RestPlace]] = await asyncio.gather(*tasks)
                for res in options: 
                    if res:
                        logger.debug(f'Найден отель по координатам: \n{res.point.coord}')
                        rest_times -= 1
                        to_remove = next((x for x in crds if x[0] == res.point.index), None)
                        if to_remove:
                            crds.remove(to_remove)
                        self.rest_places.append(res)
                else:
                    radius_increment += 2000  
            return self.rest_places                  


async def get_overpass_gateway():
    return OverpassApiGatewayImpl()


OverpassApiGateway = Annotated[
    OverpassApiGatewayImpl,
    Depends(get_overpass_gateway)
]