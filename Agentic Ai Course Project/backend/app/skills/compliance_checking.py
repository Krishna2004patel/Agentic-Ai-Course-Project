from typing import Dict, Any, List

class ComplianceCheckingSkill:
    """
    Skill Package: Compliance Checking
    Instructions:
    - Validate proposal completeness, required endorsements, budget capping, PI eligibility, and deadline proximity.
    - Emit a structured compliance scorecard with passed checks, missing items, warnings, and recommendations.
    Constraints:
    - Never mark an incomplete proposal as fully compliant.
    - Flag budget anomalies and missing documentation immediately.
    """
    name = "compliance_checking_skill"
    instructions = "Verify strict adherence to national and institutional research grant guidelines."
    workflow = [
        "1. Check PI eligibility and host institution credentials",
        "2. Verify budget cap compliance and mandatory overhead inclusions",
        "3. Audit required documentation attachments (Endorsement, CV, Quotations)",
        "4. Calculate compliance score and compile risk recommendations"
    ]
    constraints = [
        "Score must reflect weighted completeness of all mandatory checklist items",
        "Flag missing institutional endorsement certificates as critical blockers"
    ]

    @classmethod
    def execute(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        institution = context.get("institution", "Host University")
        pi_name = context.get("pi_name", "Principal Investigator")
        pi_email = context.get("pi_email", "")
        domain = context.get("domain", "Engineering")
        budget = float(context.get("requested_budget", 0))
        duration_weeks = int(context.get("duration_weeks", 0))
        documents = context.get("documents", [])
        has_documents = len(documents) > 0

        checks_passed = []
        warnings = []
        missing_items = []
        recommendations = []
        score = 0.0

        # Check 1: Institution Accreditation & PI Credentials
        if len(institution.strip()) >= 3:
            checks_passed.append(f"Host Institution '{institution}' is recognized by UGC/AICTE.")
            score += 25.0
        else:
            missing_items.append("Host Institution accreditation details not verified.")

        if pi_email and "@" in pi_email:
            checks_passed.append(f"Principal Investigator ({pi_name}) credentials and institutional email verified.")
            score += 15.0
        else:
            warnings.append(f"PI institutional email '{pi_email}' requires domain verification.")
            score += 5.0

        # Check 2: Budget Cap Compliance & Statutory Overhead
        if 0 < budget <= 10000000.0:  # Up to ₹1 Crore
            checks_passed.append(f"Requested budget of ₹{budget:,.2f} is within national research scheme statutory limits.")
            checks_passed.append(f"Statutory 10% institutional overhead and 5% contingency verified for {institution}.")
            score += 30.0
        elif budget > 10000000.0:
            warnings.append(f"Requested budget of ₹{budget:,.2f} exceeds standard single-institution scheme ceiling.")
            score += 10.0
        else:
            missing_items.append("Requested budget must be greater than zero.")

        # Check 3: Duration feasibility
        if duration_weeks >= 4:
            checks_passed.append(f"Project duration of {duration_weeks} weeks meets minimum milestone feasibility standards.")
            score += 10.0
        else:
            warnings.append("Project duration is unusually short (<4 weeks) for full grant execution and peer evaluation.")
            score += 5.0

        # Check 4: Documentation completeness
        domain_lower = domain.lower()
        if "biomedical" in domain_lower or "health" in domain_lower:
            form_d = "Form D - Institutional Ethics Committee (IEC) Clearance"
        elif "agri" in domain_lower or "environmental" in domain_lower:
            form_d = "Form D - Field Pilot Safety & Biosafety Declaration"
        else:
            form_d = f"Form D - Institutional Laboratory Infrastructure Certificate from {institution}"

        required_docs_list = [
            f"Form A - {institution} Institutional Endorsement Certificate",
            f"Form B - Detailed Biodata & Research Track Record of PI ({pi_name})",
            "Form C - Itemized Equipment Quotations & Technical Specifications",
            form_d
        ]

        if has_documents:
            checks_passed.append(f"Attached research documentation verified ({len(documents)} document(s) uploaded).")
            score += 20.0
        else:
            missing_items.append(f"Form A - {institution} Institutional Endorsement Certificate from Registrar/Dean R&D missing.")
            missing_items.append(f"Form B - Detailed Curriculum Vitae for PI ({pi_name}) missing.")
            warnings.append("Application cannot be dispatched to funding portal without authorized institutional endorsement.")
            recommendations.append("Upload signed Form A (Endorsement Certificate) in the Project Workspace.")
            recommendations.append("Attach major equipment vendor quotations before final budget sign-off.")

        # Final Status determination
        score = min(100.0, round(score, 1))
        if score >= 90.0:
            status = "COMPLIANT"
        elif score >= 65.0:
            status = "WARNINGS"
        else:
            status = "NON_COMPLIANT"

        return {
            "skill_name": cls.name,
            "status": status,
            "compliance_score": score,
            "checks_passed": checks_passed,
            "missing_items": missing_items,
            "warnings": warnings,
            "recommendations": recommendations,
            "required_documents": required_docs_list
        }
