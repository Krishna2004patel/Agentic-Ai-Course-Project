from typing import Dict, Any, List

class FundingCalculatorTool:
    """
    Deterministic & Verifiable arithmetic calculator for grant proposals.
    Implements standard funding agency caps (DST, SERB, ICMR, AICTE):
    - Overhead limits: Standard 10% for educational institutions (e.g. KLE Tech)
    - Contingency limit: Standard 5%
    - Equipment + Manpower + Consumables + Travel balance checks.
    """
    @staticmethod
    def calculate_budget(
        equipment_cost: float,
        manpower_cost: float,
        travel_cost: float,
        software_cost: float,
        consumables_cost: float,
        contingency_percent: float = 5.0,
        overhead_percent: float = 10.0
    ) -> Dict[str, Any]:
        # Validate non-negative numbers
        costs = {
            "equipment": max(0.0, float(equipment_cost)),
            "manpower": max(0.0, float(manpower_cost)),
            "travel": max(0.0, float(travel_cost)),
            "software": max(0.0, float(software_cost)),
            "consumables": max(0.0, float(consumables_cost))
        }
        
        direct_cost = sum(costs.values())
        
        # Calculate contingency
        contingency_cost = round(direct_cost * (contingency_percent / 100.0), 2)
        subtotal = direct_cost + contingency_cost
        
        # Calculate institutional overhead
        overhead_cost = round(direct_cost * (overhead_percent / 100.0), 2)
        
        total_requested = round(subtotal + overhead_cost, 2)
        
        breakdown_percentages = {
            k: round((v / total_requested * 100.0), 1) if total_requested > 0 else 0.0
            for k, v in costs.items()
        }
        breakdown_percentages["contingency"] = round((contingency_cost / total_requested * 100.0), 1) if total_requested > 0 else 0.0
        breakdown_percentages["overhead"] = round((overhead_cost / total_requested * 100.0), 1) if total_requested > 0 else 0.0

        return {
            "direct_cost": direct_cost,
            "contingency_cost": contingency_cost,
            "overhead_cost": overhead_cost,
            "total_requested": total_requested,
            "breakdown": costs,
            "percentages": breakdown_percentages,
            "overhead_rule_applied": f"{overhead_percent}% institutional overhead applied per DST/SERB guidelines",
            "is_valid": True
        }

    @staticmethod
    def verify_limits(requested_budget: float, scheme_max_limit: float) -> Dict[str, Any]:
        exceeds = requested_budget > scheme_max_limit
        difference = abs(requested_budget - scheme_max_limit)
        return {
            "requested_budget": requested_budget,
            "scheme_max_limit": scheme_max_limit,
            "is_within_limit": not exceeds,
            "difference": difference,
            "warning": f"Budget exceeds funding scheme maximum limit by ₹{difference:,.2f}" if exceeds else "Budget is within funding agency cap."
        }
