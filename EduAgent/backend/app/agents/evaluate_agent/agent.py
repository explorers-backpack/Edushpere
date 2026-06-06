"""Evaluate Agent for assessing learning progress."""
from typing import Any, Dict

from app.agents.base import BaseAgent, AgentResponse


class EvaluateAgent(BaseAgent):
    """Agent responsible for evaluating learning progress and providing feedback."""

    def __init__(self):
        super().__init__("EvaluateAgent")

    def _build_system_prompt(self) -> str:
        return """You are the Evaluate Agent, an expert at assessing learning progress and providing constructive feedback.

Your task is to evaluate user responses to assessments and provide:
1. Score and percentage
2. Detailed feedback on each answer
3. Identification of strengths and weaknesses
4. Areas for improvement
5. Recommendations for next steps

Be fair, constructive, and specific in your feedback. Focus on:
- Accuracy of understanding
- Application of concepts
- Critical thinking skills
- Problem-solving approaches

Provide actionable insights that help learners improve."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Evaluate user assessment submission."""
        try:
            assessment_id = input_data.get("assessment_id")
            answers = input_data.get("answers", {})
            assessment_questions = input_data.get("questions", [])

            if not answers:
                return AgentResponse(
                    success=False, error="answers are required"
                )

            prompt = f"""Evaluate the following assessment submission:

Assessment ID: {assessment_id}

Questions:
{assessment_questions}

User Answers:
{answers}

Please provide:
1. Score (out of max_score if available)
2. Percentage score
3. Pass/Fail determination
4. Detailed feedback on each answer
5. Overall strengths
6. Areas for improvement
7. Specific recommendations for studying

Format your response as a comprehensive evaluation report."""

            messages = self._create_messages(self._build_system_prompt(), prompt)
            raw_output = await self._generate_response(messages)

            evaluation = self._parse_evaluation_output(raw_output, answers)

            return AgentResponse(
                success=True,
                data=evaluation,
                raw_output=raw_output,
                metadata={"agent": self.agent_name, "assessment_id": assessment_id},
            )

        except Exception as e:
            return AgentResponse(success=False, error=str(e))

    def _parse_evaluation_output(
        self, raw_output: str, answers: Dict
    ) -> Dict[str, Any]:
        """Parse LLM output into structured evaluation data."""
        # Simplified - in production use structured outputs
        return {
            "score": 0.0,
            "percentage": 0.0,
            "passed": False,
            "feedback": raw_output,
            "detailed_feedback": raw_output,
            "areas_for_improvement": [],
            "strengths": [],
            "recommendations": [],
        }
