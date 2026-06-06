"""Path Agent for generating learning paths."""
from typing import Any, Dict

from app.agents.base import BaseAgent, AgentResponse


class PathAgent(BaseAgent):
    """Agent responsible for designing personalized learning paths."""

    def __init__(self):
        super().__init__("PathAgent")

    def _build_system_prompt(self) -> str:
        return """You are the Path Agent, an expert curriculum designer for personalized learning journeys.

Your task is to design comprehensive, structured learning paths based on:
1. Target skill or subject
2. User's current knowledge level
3. Available time commitment
4. Learning goals and objectives
5. Any constraints or preferences

Design a learning path with:
- Clear stages/steps ordered logically
- Each stage with specific objectives
- Estimated time for each stage
- Prerequisites between stages
- Practical milestones and checkpoints

The path should be challenging but achievable, and should leverage the user's strengths while addressing weaknesses."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Generate a personalized learning path."""
        try:
            target_skill = input_data.get("target_skill", "")
            current_knowledge = input_data.get("current_knowledge", {})
            time_available = input_data.get("time_available", 10)
            goals = input_data.get("goals", [])
            constraints = input_data.get("constraints", {})

            if not target_skill:
                return AgentResponse(success=False, error="target_skill is required")

            prompt = f"""Design a personalized learning path with the following specifications:

Target Skill: {target_skill}

Current Knowledge Levels:
{current_knowledge}

Available Time: {time_available} hours per week

Learning Goals:
{goals}

Constraints:
{constraints}

Please provide a structured learning path with:
1. Title and description
2. List of stages (with order numbers)
3. Each stage should have:
   - Title and description
   - Key learning objectives
   - Estimated hours
   - Prerequisites (if any)
4. Total estimated duration
5. Key milestones

Format as a detailed plan that can be structured into a learning path."""

            messages = self._create_messages(self._build_system_prompt(), prompt)
            raw_output = await self._generate_response(messages)

            path_data = self._parse_path_output(raw_output)

            return AgentResponse(
                success=True,
                data=path_data,
                raw_output=raw_output,
                metadata={"agent": self.agent_name},
            )

        except Exception as e:
            return AgentResponse(success=False, error=str(e))

    def _parse_path_output(self, raw_output: str) -> Dict[str, Any]:
        """Parse LLM output into structured path data."""
        return {
            "raw_plan": raw_output,
            # Other structured fields would be extracted here
        }
