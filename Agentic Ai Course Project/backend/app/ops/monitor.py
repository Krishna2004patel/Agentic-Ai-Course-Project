from typing import Dict, Any, List
from datetime import datetime

class OperationsMonitorEngine:
    """
    Lab 10: Operations Monitoring Agent
    Monitors runtime health, agent timeouts, document extraction errors,
    and classifies incident severity with safe, non-destructive recovery actions.
    """
    @staticmethod
    def audit_system_operations(simulated_telemetry: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        telemetry = simulated_telemetry or [
            {
                "incident_id": "INC-801",
                "subsystem": "OpenAlex Funding API Connector",
                "event_type": "HTTP 504 Gateway Timeout",
                "latency_ms": 10500,
                "timestamp": "2026-11-18T21:40:12Z"
            },
            {
                "incident_id": "INC-802",
                "subsystem": "PDF Extractor (pypdf)",
                "event_type": "Malformed Font Dictionary Warning in scanned annexure",
                "latency_ms": 420,
                "timestamp": "2026-11-18T21:42:05Z"
            },
            {
                "incident_id": "INC-803",
                "subsystem": "Budget Planner Agent",
                "event_type": "Overhead discrepancy attempt: 15% requested vs 10% statutory cap",
                "latency_ms": 110,
                "timestamp": "2026-11-18T21:45:33Z"
            }
        ]

        diagnoses = []
        requires_human_approval = []

        for item in telemetry:
            if "Timeout" in item["event_type"]:
                severity = "HIGH"
                root_cause = "External API rate limiting or temporary upstream connectivity issue."
                recovery_action = "Switch to cached local funding schemes database; retry with exponential backoff."
                is_destructive = False
            elif "Malformed" in item["event_type"]:
                severity = "LOW"
                root_cause = "Non-standard embedded font in scanned annexure PDF."
                recovery_action = "Fallback to OCR or text stream sanitization."
                is_destructive = False
            elif "Overhead" in item["event_type"]:
                severity = "CRITICAL"
                root_cause = "Regulatory guideline violation; exceeds 10% statutory institutional overhead limit."
                recovery_action = "Hold proposal dispatch; require Human Approval from Dean R&D before budget recalculation."
                is_destructive = True
                requires_human_approval.append({
                    "incident_id": item["incident_id"],
                    "action_required": "Authorize manual budget override or force clamp to 10% statutory overhead."
                })
            else:
                severity = "INFO"
                root_cause = "Normal telemetry operation."
                recovery_action = "Log and continue."
                is_destructive = False

            diagnoses.append({
                "incident_id": item["incident_id"],
                "subsystem": item["subsystem"],
                "event": item["event_type"],
                "severity": severity,
                "root_cause_analysis": root_cause,
                "recommended_recovery": recovery_action,
                "destructive_action_blocked": is_destructive
            })

        return {
            "monitor_status": "OPERATIONAL",
            "telemetry_items_analyzed": len(telemetry),
            "diagnoses": diagnoses,
            "high_risk_actions_requiring_human_approval": requires_human_approval,
            "automated_destructive_action_executed": False,
            "system_health": "DEGRADED_RECOVERING" if any(d["severity"] == "CRITICAL" for d in diagnoses) else "HEALTHY"
        }
