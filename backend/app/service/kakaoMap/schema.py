from pydantic import BaseModel
from enum import StrEnum, Enum


class Address2AxisResponse(BaseModel):
    address_name: str
    address_type: str
    x: str
    y: str
    address: dict
    road_address: dict

    class Config:
        from_attributes = True


class Axis2AdministraionResponse(BaseModel):
    region_type: str
    address_name: str
    region_1depth_name: str
    region_2depth_name: str
    region_3depth_name: str
    region_4depth_name: str
    code: str
    x: float
    y: float


class Axis2AddressAdressDetail(BaseModel):
    address_name: str
    region_1depth_name: str
    region_2depth_name: str
    region_3depth_name: str
    mountain_yn: str
    main_address_no: str
    sub_address_no: str


class Axis2AddressRoadAddressDetail(BaseModel):
    address_name: str
    region_1depth_name: str
    region_2depth_name: str
    region_3depth_name: str
    road_name: str
    underground_yn: str
    main_building_no: str
    sub_building_no: str
    zone_no: str
    building_name: str


class Axis2AddressResponse(BaseModel):
    address: Axis2AddressAdressDetail
    road_address: Axis2AddressRoadAddressDetail


class FindPlaceByKeywordResponseDocument(BaseModel):
    place_name: str
    address_name: str
    road_address_name: str
    x: str
    y: str
