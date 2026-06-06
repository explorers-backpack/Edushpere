"""Base class for all AI agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import hashlib
import hmac
import base64
import json
import time
from urllib.parse import urlparse, urlencode
from datetime import datetime
import asyncio

import websockets

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from app.core.config import settings


@dataclass
class AgentResponse:
    """Standardized response from agents."""

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    raw_output: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.provider = settings.LLM_PROVIDER

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process input and return agent response."""
        pass

    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build the system prompt for this agent."""
        pass

    def _create_messages(
        self, system_prompt: str, user_message: str, history: Optional[List[Dict]] = None
    ) -> List[Dict[str, str]]:
        """Create message list for LLM (provider-agnostic format)."""
        messages = []
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    async def _generate_response(
        self, messages: List[Dict[str, str]], system_prompt: str = ""
    ) -> str:
        """Generate response from LLM."""
        if self.provider == "spark":
            return await self._spark_chat(messages, system_prompt)
        else:
            return await self._deepseek_chat(messages, system_prompt)

    async def _deepseek_chat(self, messages: List[Dict[str, str]], system_prompt: str) -> str:
        """Call DeepSeek API via LangChain."""
        try:
            from langchain.chat_models import init_chat_model
            llm = init_chat_model(
                model=settings.DEEPSEEK_MODEL,
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL,
            )
            langchain_messages = []
            if system_prompt:
                langchain_messages.append(SystemMessage(content=system_prompt))
            for msg in messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                else:
                    langchain_messages.append(AIMessage(content=msg["content"]))
            response = await llm.ainvoke(langchain_messages)
            return response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            raise Exception(f"DeepSeek API call failed: {str(e)}")

    async def _spark_chat(self, messages: List[Dict[str, str]], system_prompt: str) -> str:
        """Call 讯飞星火 API via WebSocket."""
        try:
            # 构建完整消息列表（包含系统提示）
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)

            # 获取 WebSocket URL 和鉴权参数
            ws_url = await self._get_spark_ws_url()
            domain = settings.SPARK_DOMAIN

            all_content = []

            async with websockets.connect(ws_url) as ws:
                # 构造请求
                request = {
                    "header": {
                        "app_id": settings.SPARK_APP_ID,
                        "uid": "user_" + str(int(time.time())),
                    },
                    "parameter": {
                        "chat": {
                            "domain": domain,
                            "temperature": 0.5,
                            "max_tokens": 2048,
                            "top_k": 4,
                        }
                    },
                    "payload": {
                        "message": {
                            "text": full_messages
                        }
                    }
                }
                await ws.send(json.dumps(request))

                # 接收响应
                while True:
                    response = await ws.recv()
                    data = json.loads(response)
                    code = data.get("header", {}).get("code", 0)
                    if code != 0:
                        raise Exception(f"Spark API error: {data}")

                    choices = data.get("payload", {}).get("choices", {})
                    status = choices.get("status", 0)
                    content_parts = choices.get("text", [])

                    for part in content_parts:
                        if part.get("role") == "assistant":
                            content = part.get("content", "")
                            all_content.append(content)

                    if status == 2:  # 完成
                        break

            return "".join(all_content)

        except Exception as e:
            raise Exception(f"Spark API call failed: {str(e)}")

    async def _get_spark_ws_url(self) -> str:
        """生成讯飞星火 WebSocket 鉴权 URL。"""
        # 讯飞星火 WebSocket 地址
        host_url = "wss://spark-api.xf-yun.com"
        if settings.SPARK_VERSION == "v3.5":
            path = "/v3.5/chat"
            host_url = "wss://spark-api.xf-yun.com/v3.5/chat"
        elif settings.SPARK_VERSION == "v3.0":
            path = "/v3.1/chat"
            host_url = "wss://spark-api.xf-yun.com/v3.1/chat"
        elif settings.SPARK_VERSION == "v2.0":
            path = "/v2.1/chat"
            host_url = "wss://spark-api.xf-yun.com/v2.1/chat"
        else:  # v1.5
            path = "/v1.1/chat"
            host_url = "wss://spark-api.xf-yun.com/v1.1/chat"

        # 生成鉴权参数
        now = datetime.now()
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 签名
        signature_origin = f"host: {urlparse(host_url).netloc}\ndate: {date}\nGET {path} HTTP/1.1"
        signature_sha = hmac.new(
            settings.SPARK_API_SECRET.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode("utf-8")

        authorization_origin = (
            f'api_key="{settings.SPARK_API_KEY}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature_sha_base64}"'
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

        # 构建最终 URL
        params = {
            "authorization": authorization,
            "date": date,
            "host": urlparse(host_url).netloc,
        }
        return f"{host_url}?{urlencode(params)}"
