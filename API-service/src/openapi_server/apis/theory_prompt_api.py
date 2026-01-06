from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="", tags=["BehaviorChangeTheories"])


# ----------------------------
# 1) Theory registry (easy to extend)
# ----------------------------
THEORY_REGISTRY: Dict[str, Dict[str, str]] = {
    "DEFAULT": {
        "display_name": "No theory selected (fallback)",
        "prompt": """
You are a behavior change assistant for a Habit Recommendation System.

The user DID NOT select a behavior change theory.
Your job is to:
1) Briefly explain that multiple evidence-based behavior change theories exist and choosing one affects the recommendation logic.
2) Present the available options and what each is best for:
   - COM-B: Diagnose Capability/Opportunity/Motivation gaps and recommend habits targeting the weakest component.
   - TTM: Stage-matched recommendations based on readiness (Preparation/Action/Maintenance etc.).
   - SCT: Focus on self-efficacy, self-regulation, environment support, and reinforcement.
3) Ask for a minimal clarification IF needed (one question max):
   - Example: "Do you want a readiness-based approach (TTM), a diagnosis-based approach (COM-B), or a confidence/support-based approach (SCT)?"
4) Until the user chooses, proceed with a safe general strategy:
   - Prefer small, low-risk, easy-to-start habits
   - Provide context design (time/place/trigger)
   - Provide a tiny starter version + progression path
   - Provide 1–2 barrier-handling if-then plans
   - Avoid overconfident assumptions; label uncertainties.

Output requirements:
- A short explanation that no theory was selected
- A recommended next step (how to choose)
- A generic recommendation strategy that can still work as a temporary default
""".strip(),
    },
    "COM-B": {
        "display_name": "COM-B (Capability, Opportunity, Motivation → Behavior)",
        "prompt": """
You are a behavior change assistant grounded in the COM-B model.

Explain COM-B briefly:
- Behavior (B) is driven by Capability (C), Opportunity (O), and Motivation (M).
- Capability: physical/psychological skills and knowledge.
- Opportunity: physical/social environment that enables or blocks behavior.
- Motivation: reflective (goals, plans) and automatic (habits, emotions).


""".strip(),
    },
    "TTM": {
        "display_name": "TTM (Transtheoretical Model / Stages of Change)",
        "prompt": """
You are a behavior change assistant grounded in the Transtheoretical Model (TTM / Stages of Change).

Explain TTM briefly:
- Change progresses through stages: Precontemplation, Contemplation, Preparation, Action, Maintenance (relapse possible).
- Recommendations should match the user's stage (readiness and past attempts).

""".strip(),
    },
    "SCT": {
        "display_name": "SCT (Social Cognitive Theory)",
        "prompt": """
You are a behavior change assistant grounded in Social Cognitive Theory (SCT).

Explain SCT briefly:
- Behavior, personal factors, and environment interact (reciprocal determinism).
- Key constructs: self-efficacy, outcome expectations, observational learning, self-regulation, reinforcement.


""".strip(),
    },
}


# ----------------------------
# 2) Input restriction (Enum) + Optional fallback
# ----------------------------
class TheoryName(str, Enum):
    COMB = "COM-B"
    TTM = "TTM"
    SCT = "SCT"


# ----------------------------
# 3) Models
# ----------------------------
class TheoryPromptIn(BaseModel):
    request_uuid: str
    theory_name: Optional[TheoryName] = None  # <- key change: allow missing selection


class TheoryPromptOut(BaseModel):
    request_uuid: str
    theory_name: str
    display_name: str
    prompt: str
    allowed_theories: List[str] = Field(default_factory=list)


# ----------------------------
# 4) Route
# ----------------------------
@router.post(
    "/theories/prompt",
    response_model=TheoryPromptOut,
    summary="Return a pre-built prompt for a behavior change theory (3 built-ins + DEFAULT fallback)",
)
async def get_theory_prompt(body: TheoryPromptIn):
    # if not selected -> fallback
    theory = body.theory_name.value if body.theory_name is not None else "DEFAULT"

    entry = THEORY_REGISTRY.get(theory)
    if not entry:
        # 双保险：正常不会发生
        raise HTTPException(status_code=400, detail=f"Unsupported theory_name: {theory}")

    return TheoryPromptOut(
        request_uuid=body.request_uuid,
        theory_name=theory,
        display_name=entry["display_name"],
        prompt=entry["prompt"],
        allowed_theories=["COM-B", "TTM", "SCT"],
    )
