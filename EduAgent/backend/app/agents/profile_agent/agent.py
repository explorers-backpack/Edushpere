"""Profile Agent for generating learning profiles."""
from typing import Any, Dict, List

from app.agents.base import BaseAgent, AgentResponse
from app.core.config import settings


class ProfileAgent(BaseAgent):
    """Agent responsible for analyzing users and generating learning profiles."""

    def __init__(self):
        super().__init__("ProfileAgent")

    def _build_system_prompt(self) -> str:
        return """You are the Profile Agent, an expert at analyzing learners and creating comprehensive learning profiles.

Your task is to analyze user-provided information about their learning goals, background, and preferences,
then generate a structured learning profile that will be used by other agents in the EduAgent system.

Analyze the following aspects:
1. Current knowledge level in relevant topics
2. Learning goals and objectives
3. Preferred learning styles (visual, auditory, reading/writing, kinesthetic)
4. Available time commitment
5. Target completion dates
6. Interests and motivations
7. Any constraints (budget, equipment, prior experience, etc.)

Output a comprehensive profile that other agents can use to personalize the learning experience."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process user input and generate learning profile."""
        try:
            user_input = input_data.get("user_input", "")
            existing_profile = input_data.get("existing_profile")

            if not user_input:
                return AgentResponse(
                    success=False,
                    error="user_input is required",
                )

            # Build the analysis prompt
            prompt = f"""Analyze the following user information and generate a comprehensive learning profile:

User Input:
{user_input}

{f"Existing Profile Data: {existing_profile}" if existing_profile else ""}

Please provide:
1. Analyzed knowledge levels
2. Refined learning goals
3. Learning style preferences (with confidence scores)
4. Recommended time commitment
5. Suggested target dates
6. Key interests to leverage
7. Any constraints to consider

Format your response as a detailed analysis that can be used to create a structured profile."""

            messages = self._create_messages(self._build_system_prompt(), prompt)
            raw_output = await self._generate_response(messages)

            # Parse the output to create structured profile data
            profile_data = self._parse_profile_output(raw_output)

            return AgentResponse(
                success=True,
                data=profile_data,
                raw_output=raw_output,
                metadata={"agent": self.agent_name},
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e),
            )

    def _parse_profile_output(self, raw_output: str) -> Dict[str, Any]:
        """Parse LLM output into structured profile data."""
        # This is a simplified parser - in production, use structured outputs or JSON parsing
        return {
            "raw_analysis": raw_output,
            # Other structured fields would be extracted here
        }
