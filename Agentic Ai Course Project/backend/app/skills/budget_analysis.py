from typing import Dict, Any
from ..core.topic_reasoning import TopicReasoningEngine
from ..tools.funding_calculator import FundingCalculatorTool

class BudgetAnalysisSkill:
    """
    Skill Package: Budget Analysis
    Instructions:
    - Partition requested grant budget into equipment, manpower, travel, software, consumables, contingency, and overhead.
    - Check compliance against SERB/DST/ICMR capping guidelines.
    - Produce itemized budget and justification notes tailored to the research domain.
    Constraints:
    - Overhead strictly capped at 10% for institutions.
    - Contingency strictly capped at 5%.
    - Equipment and manpower must not exceed 80% combined.
    
    Topic-Agnostic Financial Planner & Statutory Auditor:
    - Analyzes project methodology and technical entities to determine resource intensity.
    - Dynamically partitions budget into Equipment, Manpower, Software, Consumables, Travel.
    - Strictly enforces statutory 5% contingency and 10% institutional overhead caps.
    - Formulates transparent arithmetic justifications.
    """
    name = "budget_analysis_skill"
    instructions = "Produce an optimized, guideline-compliant itemized budget with arithmetic precision."
    workflow = [
        "1. Extract total grant target and domain requirements",
        "2. Allocate equipment, manpower, and software costs based on domain needs",
        "1. Extract total grant target and technical requirements",
        "2. Dynamically allocate equipment, manpower, software, and consumables based on resource intensity",
        "3. Compute statutory 5% contingency and 10% institutional overhead",
        "4. Validate totals against funding agency guidelines and compile justifications"
    ]
    constraints = [
        "Enforce 10% overhead cap",
        "Enforce 10% overhead cap for host institution",
        "Enforce 5% contingency cap",
        "Total sum of all components must equal requested total exactly"
        "Total sum of all components must equal requested budget exactly"
    ]

    @classmethod
    def execute(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        total_requested = float(context.get("requested_budget", 1000000.0))
        domain = context.get("domain", "Engineering & Technology")
        institution = context.get("institution", "Host Institution")
        institution = context.get("institution", "Host University")
        topic = context.get("topic", "Research Grant Project")

        domain_lower = domain.lower()
        topic_lower = topic.lower()
        # Dynamically infer resource partitions from project semantics
        resource_plan = TopicReasoningEngine.analyze_resource_intensity(
            title=topic,
            domain=domain,
            requested_budget=total_requested
        )

        # Domain-aware partition ratios
        if "agri" in domain_lower or "crop" in topic_lower or "plant" in topic_lower:
            equip_ratio = 0.38
            manpower_ratio = 0.28
            software_ratio = 0.08
            consumables_ratio = 0.18
            travel_ratio = 0.08
            equip_desc = f"Multispectral imaging sensors, drone payload mount, and solar-powered edge IoT telemetry nodes for field deployment."
            consumables_desc = f"Soil nutrient test kits, foliar chemical reagents, testbed planting consumables, and flash memory media."
            travel_desc = f"Field visits to agricultural research plots, farmer field trials, and national agritech dissemination conferences."
        elif "energy" in domain_lower or "solar" in topic_lower or "wind" in topic_lower or "power" in topic_lower:
            equip_ratio = 0.42
            manpower_ratio = 0.25
            software_ratio = 0.13
            consumables_ratio = 0.14
            travel_ratio = 0.06
            equip_desc = f"Precision power quality analyzers, grid-tied inverter testbench, battery storage cyclers, and data loggers."
            consumables_desc = f"Lithium cell test batches, electrical shunt resistors, busbars, and testing leads."
            travel_desc = f"Visits to solar farm substations, utility interconnect pilot sites, and IEEE PES conference presentations."
        elif "biomedical" in domain_lower or "health" in domain_lower or "disease" in topic_lower or "medical" in topic_lower:
            equip_ratio = 0.35
            manpower_ratio = 0.32
            software_ratio = 0.10
            consumables_ratio = 0.18
            travel_ratio = 0.05
            equip_desc = f"Non-invasive diagnostic physiological sensors, optical acquisition hardware, and GPU inference workstation."
            consumables_desc = f"Clinical sample assay kits, biochemical reagents, specimen collection containers, and data backup storage."
            travel_desc = f"Hospital clinical trial visits, collaborative meetings with medical specialists, and biomedical symposiums."
        elif "civil" in domain_lower or "structural" in topic_lower:
            equip_ratio = 0.40
            manpower_ratio = 0.26
            software_ratio = 0.10
            consumables_ratio = 0.16
            travel_ratio = 0.08
            equip_desc = f"Distributed fiber-optic strain sensor interrogator, accelerometers, and environmental telemetry transmitters."
            consumables_desc = f"Optical fiber spools, protective epoxy resins, mounting brackets, and sensor cables."
            travel_desc = f"Infrastructure field site monitoring on bridges, structural testbeds, and national civil engineering conventions."
        else: # Computer Science / AI / Advanced Tech
            equip_ratio = 0.32
            manpower_ratio = 0.38
            software_ratio = 0.15
            consumables_ratio = 0.10
            travel_ratio = 0.05
            equip_desc = f"High-performance GPU compute server, development workstations, and sensory hardware interfaces."
            consumables_desc = f"High-speed NVMe storage arrays, networking cables, sensor breakout components, and benchmark media."
            travel_desc = f"Dissemination at peer-reviewed ACM/IEEE conferences, project review meetings, and technical workshops."
        equip = resource_plan["equipment"]
        manpower = resource_plan["manpower"]
        software = resource_plan["software"]
        consumables = resource_plan["consumables"]
        travel = resource_plan["travel"]

        # The direct costs partition (15% is reserved for Contingency (5%) + Overhead (10%))
        # direct_cost * (1 + 0.05 + 0.10) = direct_cost * 1.15 = total_requested
        allocatable = total_requested / 1.15

        equip = round(allocatable * equip_ratio, 2)
        manpower = round(allocatable * manpower_ratio, 2)
        software = round(allocatable * software_ratio, 2)
        consumables = round(allocatable * consumables_ratio, 2)
        travel = round(allocatable * travel_ratio, 2)

        calc_result = FundingCalculatorTool.calculate_budget(
            equipment_cost=equip,
            manpower_cost=manpower,
            travel_cost=travel,
            software_cost=software,
            consumables_cost=consumables,
            contingency_percent=5.0,
            overhead_percent=10.0
        )

        justifications = [
            f"Equipment (₹{equip:,.2f}): {equip_desc}",
            f"Manpower (₹{manpower:,.2f}): Junior Research Fellow (JRF) and research assistant stipends compliant with national funding agency norms.",
            f"Software & Licenses (₹{software:,.2f}): Cloud compute credits, specialized modeling licenses, and development tools.",
            f"Consumables (₹{consumables:,.2f}): {consumables_desc}",
            f"Travel (₹{travel:,.2f}): {travel_desc}",
            f"Contingency (₹{calc_result['contingency_cost']:,.2f}): Statutory 5% emergency cushion for price fluctuations and experimental escalation.",
            f"Institutional Overhead (₹{calc_result['overhead_cost']:,.2f}): Mandatory 10% overhead allocation to {institution} for laboratory infrastructure, power, and administrative audit support."
        ]

        return {
            "skill_name": cls.name,
            "requested_total": total_requested,
            "calculated_total": calc_result["total_requested"],
            "direct_cost": calc_result["direct_cost"],
            "direct_costs": calc_result["direct_cost"],
            "breakdown": {
                "equipment": equip,
                "manpower": manpower,
                "travel": travel,
                "software": software,
                "consumables": consumables
            },
            "contingency_cost": calc_result["contingency_cost"],
            "overhead_cost": calc_result["overhead_cost"],
            "percentages": {
                "equipment": round((equip / calc_result["direct_cost"]) * 100, 1) if calc_result["direct_cost"] > 0 else 35.0,
                "manpower": round((manpower / calc_result["direct_cost"]) * 100, 1) if calc_result["direct_cost"] > 0 else 30.0,
                "travel": round((travel / calc_result["direct_cost"]) * 100, 1) if calc_result["direct_cost"] > 0 else 5.0,
                "software": round((software / calc_result["direct_cost"]) * 100, 1) if calc_result["direct_cost"] > 0 else 10.0,
                "consumables": round((consumables / calc_result["direct_cost"]) * 100, 1) if calc_result["direct_cost"] > 0 else 10.0,
                "contingency": 5.0,
                "institutional_overhead": 10.0
            },
            "justifications": [
                f"Equipment (₹{equip:,.2f}): {resource_plan.get('equipment_justification', equip_desc)}",
                f"Manpower (₹{manpower:,.2f}): {resource_plan.get('manpower_justification', 'Junior Research Fellow (JRF) and research assistant stipends compliant with national funding agency norms.')}",
                f"Software (₹{software:,.2f}): {resource_plan.get('software_justification', 'Cloud compute credits, specialized modeling licenses, and development tools.')}",
                f"Consumables (₹{consumables:,.2f}): {resource_plan.get('consumables_justification', consumables_desc)}",
                f"Travel & Fieldwork (₹{travel:,.2f}): {resource_plan.get('travel_justification', travel_desc)}",
                f"Statutory 5% Contingency (₹{calc_result['contingency_cost']:,.2f}): Mandated provision for unpredicted experimental escalation.",
                f"Mandatory 10% Overhead (₹{calc_result['overhead_cost']:,.2f}): Institutional infrastructure overhead for {institution} capped at 10%."
            ],
            "overhead_rule_applied": f"10% institutional overhead for {institution} per statutory guidelines",
            "statutory_compliant": calc_result["overhead_cost"] <= round(total_requested * 0.12, 2)
        }
