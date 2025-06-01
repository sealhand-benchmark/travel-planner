# import requests
# from core.config import env
# from requests_oauthlib import OAuth2Session


# class KakaoCalendarService:

#     BASE_URL = "https://kapi.kakao.com"

#     def __init__(self):
#         self.api_key = env.KAKAO_API_REST_KEY
#         self.client_secret = env.KAKAO_CLIENT_SECRET

#     def get_kakao_calendar_access_token(self):
#         AUTHORIZE_REQUEST_URL = "https://kauth.kakao.com/oauth/authorize"
#         TOKEN_REQUEST_URL = "https://kauth.kakao.com/oauth/token"
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded"
#         }
#         authorize_params = {
#             "response_type": "code",
#             "client_id": self.api_key,
#             "redirect_uri": "https://example.com/oauth",
#         }
#         authorize_response = requests.(AUTHORIZE_REQUEST_URL, headers=headers, params=authorize_params)
#         # authorize_code = authorize_response.json()["code"]

#         oauth_session = OAuth2Session(
#             client_id=self.api_key, redirect_uri="https://example.com/oauth"
#         )
#         url, state = oauth_session.authorization_url(AUTHORIZE_REQUEST_URL)

#         print("ur", url, "state", state)

#         token_response = oauth_session.fetch_token(
#             token_url=TOKEN_REQUEST_URL,
#             client_id=self.api_key,
#             client_secret=self.client_secret,
#             include_client_id=True,
#             code="A",
#         )

#         token_params = {
#             "grant_type": "authorization_code",
#             "client_id": self.api_key,
#             "redirect_uri": "https://example.com/oauth",
#             "code": authorize_code,
#         }
#         token_response = requests.post(
#             TOKEN_REQUEST_URL, headers=headers, params=token_params
#         )
#         token_response.json()["access_token"]
#         return token_response.json()

#     def get_kakao_calendar_api_key(self):
#         return self.api_key
