import random
import asyncio
import json
import uuid
import time
from datetime import timedelta, datetime, timezone
from typing import Annotated, Any, Optional, Dict
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
    Body,
)
import uuid
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from api.schema.chat import ResponsePostChatInitConfig
from app.service.agent.TravelPlanner import SESSION_MEMORIES
from langchain.memory import ConversationBufferMemory
from core.config import env
from app.service.kakaoMap.KakaoMapService import KakaoMapService
from api.schema.map import (
    AddressToAxisRequest,
    AxisToAdministrationRequest,
    AxisToAddressRequest,
    FindPlaceByKeywordRequest,
    FindPlaceByCategoryRequest,
    KakaoMapResponse,
    RouteRequest,
    RouteResponse,
)

map_router = APIRouter()


@map_router.post(
    path="/address-to-axis",
    summary="주소를 좌표로 변환",
    response_model=KakaoMapResponse,
)
async def transform_address_to_axis(request: AddressToAxisRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.transform_address_to_axis(request.address)


@map_router.post(
    path="/axis-to-administration",
    summary="좌표를 행정구역정보로 변환",
    response_model=KakaoMapResponse,
)
async def transform_axis_to_administration(request: AxisToAdministrationRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.transform_axis_to_administration_code(request.x, request.y)


@map_router.post(
    path="/axis-to-address",
    summary="좌표를 주소로 변환",
    response_model=KakaoMapResponse,
)
async def transform_axis_to_address(request: AxisToAddressRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.transform_axis_to_address(request.x, request.y)


@map_router.post(
    path="/place/keyword",
    summary="키워드로 장소 검색",
    response_model=KakaoMapResponse,
)
async def find_place_by_keyword(request: FindPlaceByKeywordRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.find_place_by_keyword(
        keyword=request.keyword,
        category_group_code=request.category_group_code,
        x=request.x,
        y=request.y,
        radius=request.radius,
    )


@map_router.post(
    path="/place/category",
    summary="카테고리로 장소 검색",
    response_model=KakaoMapResponse,
)
async def find_place_by_category(request: FindPlaceByCategoryRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.find_place_by_category_group_code(
        category_group_code=request.category_group_code,
        x=request.x,
        y=request.y,
        radius=request.radius,
    )


@map_router.post(
    path="/route",
    summary="경로 소요시간 계산",
    response_model=RouteResponse,
)
async def calculate_route(request: RouteRequest):
    kakao_map_service = KakaoMapService()
    return kakao_map_service.get_how_many_times_to_visit(
        origin_axis=(request.origin.x, request.origin.y),
        destination_axis=(request.destination.x, request.destination.y),
        waypoints=(
            [(point.x, point.y) for point in request.waypoints]
            if request.waypoints
            else None
        ),
    )
