# -*- coding:utf-8 -*-
import aiohttp
import requests
from fake_useragent import UserAgent

from util import utils
from util.config import PROXY, CLERK_JS_VERSION
from util.logger import logger

ua = UserAgent(browsers=["edge"])

get_session_url = f"https://clerk.suno.com/v1/client?_clerk_js_version={CLERK_JS_VERSION}"

exchange_token_url = (
    "https://clerk.suno.com/v1/client/sessions/{sid}/tokens?_clerk_js_version={CLERK_JS_VERSION}"
)

base_url = "https://studio-api.suno.ai"

browser_version = "edge101"

MUSIC_GENRE_LIST = [
    "African",
    "Asian",
    "South and southeast Asian",
    "Avant-garde",
    "Blues",
    "Caribbean and Caribbean-influenced",
    "Comedy",
    "Country",
    "Easy listening",
    "Electronic",
    "Folk",
    "Hip hop",
    "Jazz",
    "Latin",
    "Pop",
    "R&B and soul",
    "Rock",
]


class SongsGen:
    # 初始化
    def __init__(self, cookie: str) -> None:
        try:
            self.token_headers = {
                "User-Agent": ua.edge,
                "Content-Type": "application/x-www-form-urlencoded",
                # "Impersonate": browser_version,
                "accept-encoding": "gzip, deflate, br, zstd",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Affiliate-Id": "undefined",
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "X-Priority": "u=1, i"
            }
            self.request_headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) \
                    Gecko/20100101 Firefox/117.0",
                "Impersonate": browser_version,
            }
            self.proxy = PROXY
            self.cookie_string = utils.parse_cookie_string(cookie)
        except Exception as e:
            raise Exception(f"初始化失败,请检查cookie是否有效: {e}")

    # 获取token
    async def _get_session_id(self):
        try:
            async with aiohttp.ClientSession(cookies=self.cookie_string) as request_session:
                try:
                    async with request_session.get(get_session_url, headers=self.token_headers,
                                                   proxy=self.proxy) as response:
                        response.raise_for_status()
                        data = await response.json()
                        sessions = data.get("response", {}).get("sessions")
                        if not sessions:
                            raise ValueError("No session data in response")
                        session_id = sessions[0].get('id')
                        if not session_id:
                            raise ValueError("Failed to get session id")
                        return session_id
                except (aiohttp.ClientError, ValueError) as e:
                    raise Exception(f"Failed to get session id: {e}")
        except Exception as outer_e:
            # 记录会话创建过程中的异常
            logger.error(f"无法建立会话: {outer_e}")
            return -1

    async def _get_jwt_token(self, session_id):
        try:
            async with aiohttp.ClientSession(cookies=self.cookie_string) as request_session:
                try:
                    async with request_session.post(
                            exchange_token_url.format(sid=session_id, CLERK_JS_VERSION=CLERK_JS_VERSION),
                            headers=self.token_headers, proxy=self.proxy) as response:
                        response.raise_for_status()
                        data = await response.json()
                        jwt_token = data.get('jwt')
                        if not jwt_token:
                            raise ValueError("Failed to get JWT token")
                        return jwt_token
                except (aiohttp.ClientError, ValueError) as e:
                    raise Exception(f"Failed to get JWT token: {e}")
        except Exception as outer_e:
            # 记录会话创建过程中的异常
            logger.error(f"无法建立会话: {outer_e}")
            return -1

    async def get_auth_token(self, w=None):
        try:
            session_id = await self._get_session_id()
            jwt_token = await self._get_jwt_token(session_id)
            if w is not None:
                return jwt_token, session_id
            logger.info(f"获取get_auth_token成功: {jwt_token}")
            return jwt_token
        except Exception as e:
            logger.error(f"获取get_auth_token失败: {e}")
            raise Exception(f"获取get_auth_token失败: {e}")

    # 获取剩余次数
    async def get_limit_left(self) -> int:
        try:
            # 获取认证令牌
            auth_token = await self.get_auth_token()
            # 更新请求头信息
            request_headers = {
                "Authorization": f"Bearer {auth_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Origin": "https://suno.com",
                "Referer": "https://suno.com/",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Affiliate-Id": "undefined",
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "X-Priority": "u=1, i"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get("https://studio-api.suno.ai/api/billing/info/",
                                       headers=request_headers, proxy=self.proxy) as response:
                    response_text = await response.text()
                    logger.info(response_text)
                    response.raise_for_status()
                    data = await response.json()
                    return int(data["total_credits_left"] / 10)

        except Exception as e:
            logger.error(f"获取get_limit_left失败: {e}")
            return -1
    
    async def get_limit_finally(self) -> int:
        try:
            # 使用上下文管理器创建客户端会话
            async with aiohttp.ClientSession(cookies=self.cookie_string) as request_session:
                try:
                    # 获取认证令牌
                    auth_token = await self.get_auth_token()
                    # 更新请求头信息
                    self.request_headers["Authorization"] = f"Bearer {auth_token}"
                    self.request_headers["user-agent"] = ua.edge
                    request_session.headers.update(self.request_headers)

                    # 发送请求获取剩余次数信息
                    async with request_session.get(
                            "https://studio-api.suno.ai/api/billing/info/", proxy=self.proxy
                    ) as response:
                        # 检查响应状态码
                        response.raise_for_status()
                        # 解析响应数据
                        data = await response.json()
                        # 计算并返回剩余次数
                        return int(data["total_credits_left"] / 10)
                except Exception as e:
                    # 记录获取剩余次数过程中的异常
                    logger.error(f"获取get_limit_left失败: {e}")
                    return -1
        except Exception as outer_e:
            # 记录会话创建过程中的异常
            logger.error(f"无法建立会话: {outer_e}")
            return -1
