"""Base class for all AI agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from langchain.chat_models import init_chat_model
from langchain.graph import StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

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
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the language model."""
        return init_chat_model(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process input and return agent response."""
        pass

    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build the system prompt for this agent."""
        pass

    async def _generate_response(
        self, messages: List[BaseMessage], tools: Optional[List] = None
    ) -> str:
        """Generate response from LLM."""
        if tools:
            # For agents with tool calling capability
            response = await self.llm.bind_tools(tools).ainvoke(messages)
        else:
            response = await self.llm.ainvoke(messages)
        return response.content if hasattr(response, "content") else str(response)

    def _create_messages(
        self, system_prompt: str, user_message: str, history: Optional[List[Dict]] = None
    ) -> List[BaseMessage]:
        """Create message list for LLM."""
        messages = [SystemMessage(content=system_prompt)]
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_message))
        return messages
