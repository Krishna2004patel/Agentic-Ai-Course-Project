from typing import Dict, Any, List
from .research_summary import ResearchSummarizationSkill
from .proposal_writing import ProposalWritingSkill
from .budget_analysis import BudgetAnalysisSkill
from .compliance_checking import ComplianceCheckingSkill

class GlobalSkillRegistry:
    """Central registry of all reusable grant management skills."""
    
    _skills = {
        ResearchSummarizationSkill.name: ResearchSummarizationSkill,
        ProposalWritingSkill.name: ProposalWritingSkill,
        BudgetAnalysisSkill.name: BudgetAnalysisSkill,
        ComplianceCheckingSkill.name: ComplianceCheckingSkill
    }

    @classmethod
    def list_skills(cls) -> List[Dict[str, Any]]:
        return [
            {
                "name": skill.name,
                "instructions": skill.instructions,
                "workflow": skill.workflow,
                "constraints": skill.constraints
            }
            for skill in cls._skills.values()
        ]

    @classmethod
    def execute_skill(cls, name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if name not in cls._skills:
            return {"error": f"Skill '{name}' not found in registry."}
        skill_cls = cls._skills[name]
        return skill_cls.execute(context)
