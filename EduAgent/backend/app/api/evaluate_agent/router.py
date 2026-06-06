"""Evaluate Agent API router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.assessment import (
    EvaluationRequest,
    EvaluationResponse,
    AssessmentResultResponse,
)
from app.services.assessment_service import AssessmentService
from app.agents.evaluate_agent.agent import EvaluateAgent

router = APIRouter(prefix="/api/evaluate", tags=["evaluate_agent"])
agent = EvaluateAgent()


@router.post("/submit", response_model=EvaluationResponse)
async def submit_evaluation(
    request: EvaluationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit assessment answers for evaluation."""
    assessment_service = AssessmentService(db)

    # Get the assessment
    assessment = await assessment_service.get_assessment_by_id(request.assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Process through Evaluate Agent
    result = await agent.process({
        "assessment_id": request.assessment_id,
        "answers": request.answers,
        "questions": assessment.questions,
    })

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    # Save result to database
    evaluation_data = result.data
    assessment_result = await assessment_service.create_result(
        user_id=current_user.id,
        assessment_id=request.assessment_id,
        result_data={
            "answers": request.answers,
            "score": evaluation_data.get("score"),
            "percentage": evaluation_data.get("percentage"),
            "passed": evaluation_data.get("passed"),
            "feedback": evaluation_data.get("feedback"),
        },
    )

    return EvaluationResponse(
        result=AssessmentResultResponse.model_validate(assessment_result),
        detailed_feedback=evaluation_data.get("detailed_feedback", ""),
        areas_for_improvement=evaluation_data.get("areas_for_improvement", []),
        strengths=evaluation_data.get("strengths", []),
        recommendations=evaluation_data.get("recommendations", []),
    )


@router.get("/result/{result_id}", response_model=AssessmentResultResponse)
async def get_evaluation_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific evaluation result."""
    service = AssessmentService(db)
    result = await service.get_result_by_id(result_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.get("/history", response_model=list[AssessmentResultResponse])
async def get_evaluation_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get evaluation history for current user."""
    service = AssessmentService(db)
    results = await service.get_user_results(current_user.id)
    return results
