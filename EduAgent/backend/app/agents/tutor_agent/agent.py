"""Tutor Agent for conversational learning assistance."""
from typing import Any, Dict, List

from app.agents.base import BaseAgent, AgentResponse


class TutorAgent(BaseAgent):
    """Agent responsible for conversational tutoring and Q&A."""

    def __init__(self):
        super().__init__("TutorAgent")

    def _build_system_prompt(self) -> str:
        return """You are the Tutor Agent, a patient and knowledgeable learning companion.

Your role is to:
1. Answer questions about learning topics
2. Explain concepts in multiple ways
3. Guide users through problems
4. Provide examples and analogies
5. Encourage critical thinking
6. Adapt to the user's level of understanding

Guidelines:
- Be clear and concise
- Use examples and analogies
- Check for understanding
- Encourage questions
- Provide positive reinforcement
- When unsure, admit it and suggest resources

Keep responses focused and helpful. Use the conversation history to maintain context."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process a tutoring conversation turn."""
        try:
            message = input_data.get("message", "")
            session_id = input_data.get("session_id", "default")
            context = input_data.get("context", {})
            history = input_data.get("history", [])

            if not message:
                return AgentResponse(success=False, error="message is required")

            # Build context information
            context_prompt = ""
            if context:
                context_prompt = f"""
Current Learning Context:
- Current topic: {context.get('current_topic', 'N/A')}
- Learning path: {context.get('learning_path_title', 'N/A')}
- Current stage: {context.get('current_stage', 'N/A')}
- User's knowledge level: {context.get('knowledge_level', 'N/A')}
"""

            prompt = f"""{context_prompt}

User Question: {message}

Please respond to the user's question in a helpful, educational manner.
Consider the context provided above when formulating your response.

After your response, you may suggest:
- Follow-up questions the user might ask
- Related topics to explore
- Next steps in their learning journey"""

            messages = self._create_messages(self._build_system_prompt(), prompt, history)
            raw_output = await self._generate_response(messages)

            response_data = self._parse_tutor_output(raw_output)

            return AgentResponse(
                success=True,
                data=response_data,
                raw_output=raw_output,
                metadata={
                    "agent": self.agent_name,
                    "session_id": session_id,
                },
            )

        except Exception as e:
            return AgentResponse(success=False, error=str(e))

    def _parse_tutor_output(self, raw_output: str) -> Dict[str, Any]:
        """Parse LLM output into structured response data."""
        # Simplified - in production use structured outputs
        return {
            "response": raw_output,
            "suggestions": [],
        }
