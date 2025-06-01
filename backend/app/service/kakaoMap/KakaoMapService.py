import requests
from typing import Optional, Tuple, List
from core.config import env
from loguru import logger


class KakaoMapService:

    BASE_URL = "https://dapi.kakao.com"
    CATEGORY_CODE_MAP = {
        "대형마트": "MT1",
        "편의점": "CS2",
        "어린이집_유치원": "PS3",
        "학교": "SC4",
        "학원": "AC5",
        "주차장": "PK6",
        "주유소_충전소": "OL7",
        "지하철역": "SW8",
        "은행": "BK9",
        "문화시설": "CT1",
        "중개업소": "AG2",
        "공공기관": "PO3",
        "관광명소": "AT4",
        "숙박": "AD5",
        "음식점": "FD6",
        "카페": "CE7",
        "병원": "HP8",
        "약국": "PM9",
    }

    def __init__(self):
        self.api_key = env.KAKAO_API_REST_KEY
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}",
            "Content-Type": "application/json",
        }

    def transform_address_to_axis(self, address: str):
        """
        실제 주소를 좌표로 변환하는 API 호출 함수
        """
        REQUEST_URL = f"{self.BASE_URL}/v2/local/search/address.json"
        params = {
            "query": address,
            "page": 1,
            "size": 1,
        }
        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response
        except Exception as e:
            logger.error(f"주소를 좌표로 변환하는 중 실패하였습니다.{e}")
            return None

    def transform_axis_to_administration_code(self, x: str, y: str):
        """
        좌표를 행정구역정보로 변환하는 API 호출 함수
        """
        REQUEST_URL = f"{self.BASE_URL}/v2/local/geo/coord2regioncode.json"
        params = {
            "x": x,
            "y": y,
        }
        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response
        except Exception as e:
            logger.error(f"좌표를 행정구역정보로 변환하는 중 실패하였습니다.{e}")
            return None

    def transform_axis_to_address(self, x: str, y: str):
        """
        좌표를 실제 주소로 변환하는 API 호출 함수
        """
        REQUEST_URL = f"{self.BASE_URL}/v2/local/geo/coord2address.json"
        params = {
            "x": x,
            "y": y,
        }
        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response
        except Exception as e:
            logger.error(f"좌표를 실제 주소로 변환하는 중 실패하였습니다.{e}")
            return None

    def find_place_by_keyword(
        self,
        keyword: str,
        category_group_code: Optional[str] = None,
        x: Optional[str] = None,
        y: Optional[str] = None,
        radius: Optional[int] = None,
    ):
        """
        키워드로 장소를 검색하는 API 호출 함수
        """
        REQUEST_URL = f"{self.BASE_URL}/v2/local/search/keyword.json"
        params = {
            "query": keyword,
            "category_group_code": self.CATEGORY_CODE_MAP[category_group_code],
            "x": x,
            "y": y,
            "radius": radius,
        }
        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response
        except Exception as e:
            logger.error(f"키워드로 장소를 검색하는 중 실패하였습니다.{e}")
            return None

    def find_place_by_category_group_code(
        self,
        category_group_code: str,
        x: Optional[str] = None,
        y: Optional[str] = None,
        radius: Optional[int] = None,
    ):
        """
        카테고리 그룹 코드로 장소를 검색하는 API 호출 함수
        """
        REQUEST_URL = f"{self.BASE_URL}/v2/local/search/category.json"
        params = {
            "category_group_code": self.CATEGORY_CODE_MAP[category_group_code],
            "x": x,
            "y": y,
            "radius": radius,
        }
        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response
        except Exception as e:
            logger.error(f"카테고리 그룹 코드로 장소를 검색하는 중 실패하였습니다.{e}")
            return None

    def get_how_many_times_to_visit(
        self,
        origin_axis: Tuple[float, float],
        destination_axis: Tuple[float, float],
        waypoints: List[Tuple[float, float]] = None,
    ):
        """
        출발지와 도착지의 거리를 계산하는 API 호출 함수
        """
        REQUEST_URL = "https://apis-navi.kakaomobility.com/v1/directions"

        params = {
            "origin": f"{origin_axis[0]},{origin_axis[1]}",
            "destination": f"{destination_axis[0]},{destination_axis[1]}",
        }

        if waypoints:
            params["waypoints"] = "|".join(
                [f"{waypoint[0]},{waypoint[1]}" for waypoint in waypoints]
            )

        try:
            response = requests.get(
                REQUEST_URL, params=params, headers=self.headers
            ).json()
            return response["routes"][0]["summary"]["duration"]
        except Exception as e:
            logger.error(f"소요시간을 요청하는 중 실패하였습니다.{e}")
            return None
