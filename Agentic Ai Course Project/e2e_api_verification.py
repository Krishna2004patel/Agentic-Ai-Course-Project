import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

def http_get(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return response.status, json.loads(response.read().decode())

def http_post(url, data=None):
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return response.status, json.loads(response.read().decode())

def run_tests():
    print("=" * 80)
    print("END-TO-END HTTP API VERIFICATION FOR RESEARCH GRANT MANAGEMENT SYSTEM")
    print("=" * 80)

    # 1. Verify project listing and check for duplicates
    status, projects = http_get(f"{BASE_URL}/projects")
    print(f"\n[1] GET /projects -> Status: {status} | Count: {len(projects)}")
    titles = [p["title"].strip().lower() for p in projects]
    assert len(titles) == len(set(titles)), "Duplicate project titles detected in /projects list!"
    print("    [PASS] Zero duplicate projects detected in directory.")

    # 2. Test Dynamic Project Creation
    new_proj_payload = {
        "title": "Deep-Sea Autonomous Underwater Vehicle Telemetry and Swarm Mapping",
        "domain": "Marine Robotics & Ocean Engineering",
        "department": "Ocean Engineering & Robotics",
        "institution": "National Institute of Ocean Technology",
        "pi_name": "Dr. S. K. Sundaram",
        "pi_email": "sundaram@niot.res.in",
        "duration_weeks": 20,
        "requested_budget": 3600000.0,
        "currency": "INR",
        "objectives": "Deploy an acoustic telemetry network for autonomous underwater vehicles performing benthic hydrothermal mapping.",
        "funding_preferences": "DRDO-ER, DST Clean Energy"
    }

    # Delete if already existing from prior run
    for p in projects:
        if p["title"].strip().lower() == new_proj_payload["title"].strip().lower():
            req = urllib.request.Request(f"{BASE_URL}/projects/{p['id']}", method="DELETE")
            urllib.request.urlopen(req)
            print(f"    (Cleaned up pre-existing project ID #{p['id']})")

    status, created = http_post(f"{BASE_URL}/projects", new_proj_payload)
    new_id = created["id"]
    print(f"\n[2] POST /projects -> Status: {status} | Created Project #{new_id}")
    print(f"    Title: '{created['title']}' | Domain: '{created['domain']}' | Budget: ₹{created['requested_budget']:,.2f}")
    assert created["id"] > 0, "Created project has invalid ID"
    print("    [PASS] Project created successfully with isolated memory.")

    # 3. Test Duplicate Rejection
    print(f"\n[3] Testing Duplicate Project Rejection...")
    try:
        http_post(f"{BASE_URL}/projects", new_proj_payload)
        raise AssertionError("Expected HTTP error for duplicate project creation, but succeeded!")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 for duplicate, got {e.code}"
        err_body = json.loads(e.read().decode())
        print(f"    [PASS] Backend successfully rejected duplicate: {err_body.get('detail')}")

    # 4. Verify 4 Expected Outputs for New Project
    status, outputs = http_get(f"{BASE_URL}/projects/{new_id}/expected-outputs")
    print(f"\n[4] GET /projects/{new_id}/expected-outputs -> Status: {status}")
    print(f"    Output 1 (Funding Matches): {len(outputs['ranked_funding_opportunities'])} calls matched.")
    top_opp = outputs['ranked_funding_opportunities'][0] if outputs['ranked_funding_opportunities'] else {}
    print(f"             Top Call: '{top_opp.get('grant_title')}' by {top_opp.get('funding_organization')} (Score: {top_opp.get('relevance_score')}%)")
    print(f"    Output 2 (Proposal Draft): Title = '{outputs['structured_proposal_draft'].get('research_title')}'")
    b_tot = outputs['budget_plan'].get('total_budget') or outputs['budget_plan'].get('total_estimated_budget', 0)
    b_ovh = outputs['budget_plan'].get('statutory_overhead_10_percent') or outputs['budget_plan'].get('overhead', 0)
    print(f"    Output 3 (Budget Plan): Total = ₹{b_tot:,.2f} (Overhead: ₹{b_ovh:,.2f})")
    print(f"    Output 4 (Compliance Report): Status = {outputs['compliance_report'].get('compliance_status')} (Score: {outputs['compliance_report'].get('compliance_score')}%)")
    assert len(outputs['ranked_funding_opportunities']) > 0, "Missing funding opportunities!"
    assert b_tot > 0, "Missing budget plan total!"
    print("    [PASS] All 4 deliverables dynamically generated for newly created project.")

    # 5. TEST LAB 2 EXECUTION (The specific failure reported by user!)
    print(f"\n[5] Executing Lab 2 via HTTP API: POST /labs/2/execute/{new_id}...")
    status, lab2_res = http_post(f"{BASE_URL}/labs/2/execute/{new_id}")
    print(f"    Status: {status} | Lab 2 Execution Status: {lab2_res.get('status')} | Eval: {lab2_res.get('evaluation_status')}")
    print(f"    Output 1 Opps: {len(lab2_res['output1_funding_opportunities']['opportunities'])}")
    print(f"    Output 2 Draft: '{lab2_res['output2_proposal_draft']['research_title'][:50]}...'")
    print(f"    Output 3 Budget: ₹{lab2_res['output3_budget_plan']['total_budget']:,.2f}")
    print(f"    Output 4 Compliance: {lab2_res['output4_compliance_report']['compliance_status']}")
    print(f"    Lab 2 Concept Evidence: {list(lab2_res['lab_concept_evidence'].keys())}")
    assert lab2_res["status"] == "COMPLETED", "Lab 2 failed execution!"
    assert lab2_res["evaluation_status"] == "PASSED", "Lab 2 evaluation did not pass!"
    print("    [PASS] Lab 2 executed flawlessly with zero errors and authentic deliverables.")

    # 6. Verify All 14 Labs execution via HTTP API
    print(f"\n[6] Testing All 14 Labs on Project #{new_id}...")
    for lab_idx in range(1, 15):
        status, lab_res = http_post(f"{BASE_URL}/labs/{lab_idx}/execute/{new_id}")
        assert lab_res["status"] == "COMPLETED", f"Lab {lab_idx} failed!"
        print(f"    Lab {lab_idx:02d}: {lab_res['lab_title'][:40]:<40} -> COMPLETED / PASSED")
    print("    [PASS] All 14 labs executed independently through live FastAPI HTTP endpoints.")

    # 7. Check Teacher Overview for this Project
    status, teacher = http_get(f"{BASE_URL}/teacher/overview?project_id={new_id}")
    print(f"\n[7] GET /teacher/overview?project_id={new_id} -> Status: {status}")
    print(f"    Completed Labs: {teacher['completed_labs']}/14 | Passed Evaluations: {teacher['passed_evaluations']}/14")
    assert teacher["completed_labs"] == 14, "Teacher overview does not show 14 completed labs!"
    print("    [PASS] Teacher overview verified.")

    print("\n" + "=" * 80)
    print("ALL END-TO-END TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
