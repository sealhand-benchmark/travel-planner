from pydantic import BaseModel
from typing import Optional, List


class AddressToAxisRequest(BaseModel):
    address: str


class AxisToAdministrationRequest(BaseModel):
    x: str
    y: str


class AxisToAddressRequest(BaseModel):
    x: str
    y: str


class FindPlaceByKeywordRequest(BaseModel):
    keyword: str
    category_group_code: Optional[str] = None
    x: Optional[str] = None
    y: Optional[str] = None
    radius: Optional[int] = None


class FindPlaceByCategoryRequest(BaseModel):
    category_group_code: str
    x: Optional[str] = None
    y: Optional[str] = None
    radius: Optional[int] = None


class KakaoMapResponse(BaseModel):
    documents: List[dict]
    meta: dict


class AxisPoint(BaseModel):
    x: float
    y: float


class RouteRequest(BaseModel):
    origin: AxisPoint
    destination: AxisPoint
    waypoints: Optional[List[AxisPoint]] = None


class RouteResponse(BaseModel):
    trans_id: str
    routes: List[dict]
