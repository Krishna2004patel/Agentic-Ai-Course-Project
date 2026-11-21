from typing import Dict, Any, List, Optional
from ..core.topic_reasoning import TopicReasoningEngine

class ProposalWritingSkill:
    """
    Skill Package: Proposal Writing
    
    Topic-Agnostic Research Proposal Synthesizer:
    - Receives project title, domain, duration, objectives, and research gaps.
    - Dynamically generates SMART specific aims, four-phase technical methodology,
      time-bound milestones, and deliverables without relying on fixed domain branches.
    """
    name = "proposal_writing_skill"
    instructions = "Generate a formal academic and grant-ready research proposal adhering to agency templates."
    workflow = [
        "1. Map project objectives and lexical semantics to agency priority areas",
        "2. Formulate technical problem statement and SMART specific aims",
        "3. Detail four-stage methodology and experimental architecture",
        "4. Construct time-bound milestone breakdown mapped to project duration"
    ]
    constraints = [
        "Align milestone schedule exactly with project duration in weeks",
        "Format output into structured sections",
        "Include measurable success indicators"
    ]

    @classmethod
    def execute(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        topic = context.get("topic", "Advanced Scientific Research")
        domain = context.get("domain", "Applied Science & Engineering")
        duration_weeks = int(context.get("duration_weeks", 12))
        institution = context.get("institution", "Host University")
        pi_name = context.get("pi_name", "Principal Investigator")
        objectives_raw = context.get("objectives", "")
        research_gaps = context.get("research_gaps", [])

        # Synthesize proposal architecture dynamically via TopicReasoningEngine
        arch = TopicReasoningEngine.synthesize_proposal_architecture(
            title=topic,
            domain=domain,
            objectives=objectives_raw,
            duration_weeks=duration_weeks,
            institution=institution,
            pi_name=pi_name,
            research_gaps=research_gaps
        )

        return {
            "title": arch["title"],
            "executive_summary": arch["executive_summary"],
            "specific_aims": arch["specific_aims"],
            "methodology": arch["methodology"],
            "expected_deliverables": arch["expected_deliverables"],
            "milestones": arch["milestones"],
            "duration_weeks": duration_weeks,
            "skill_executed": cls.name,
            "reasoning_model": "topic_agnostic_semantic_synthesis"
        }
