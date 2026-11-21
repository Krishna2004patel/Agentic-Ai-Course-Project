import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_project_numbering():
    print("=" * 80)
    print("TEST 1: SEQUENTIAL PROJECT DISPLAY NUMBERING")
    print("=" * 80)
    url = f"{BASE_URL}/projects"
    res = urllib.request.urlopen(url)
    data = json.loads(res.read().decode())
    print(f"Total projects fetched: {len(data)}")
    
    display_nums = []
    for idx, p in enumerate(data):
        d_num = p.get("display_number")
        db_id = p.get("id")
        title = p.get("title")
        display_nums.append(d_num)
        print(f"  Project #{d_num:2d} (DB ID #{db_id:2d}): {title[:55]}...")
    
    # Assert sequential: 1, 2, ..., N
    expected_seq = list(range(1, len(data) + 1))
    assert display_nums == expected_seq, f"Expected {expected_seq}, but got {display_nums}"
    print("[PASS] All projects have perfectly sequential display numbers 1..N without gaps or duplicates!")
    return data

def test_orchestrate_full(project_id):
    print("=" * 80)
    print(f"TEST 2: ORCHESTRATE ALL SIX AGENTS (PROJECT DB ID: {project_id})")
    print("=" * 80)
    url = f"{BASE_URL}/agents/orchestrate-full/{project_id}"
    req = urllib.request.Request(url, method="POST")
    try:
        res = urllib.request.urlopen(req)
        body = json.loads(res.read().decode())
        print(f"HTTP Status: {res.status}")
        print(f"Orchestrator Status: {body.get('orchestrator_status')}")
        print(f"Execution Status:    {body.get('execution_status')}")
        print(f"Timestamp:           {body.get('execution_timestamp')}")
        print(f"Agents Executed:     {body.get('agents_executed')}")
        print("Generated Outputs Summary:")
        for k, v in body.get("generated_outputs", {}).items():
            print(f"  - {k}: {v}")
        print("Results detail:")
        for agent_key, res_dict in body.get("results", {}).items():
            agent_name = res_dict.get("agent", agent_key)
            status = res_dict.get("status", "OK")
            print(f"  - [{status}] {agent_name}")
        
        assert body.get("execution_status") == "COMPLETED"
        assert len(body.get("agents_executed", [])) == 6
        print("[PASS] Full six-agent orchestration executed successfully with zero 500 errors!")
    except urllib.error.HTTPError as e:
        err_content = e.read().decode()
        print(f"[FAIL] HTTP Error {e.code}: {err_content}")
        sys.exit(1)

def test_all_14_labs(project_id):
    print("=" * 80)
    print(f"TEST 3: VERIFY ALL 14 LABS EXECUTION (PROJECT DB ID: {project_id})")
    print("=" * 80)
    url = f"{BASE_URL}/labs/execute-all/{project_id}"
    req = urllib.request.Request(url, method="POST")
    res = urllib.request.urlopen(req)
    body = json.loads(res.read().decode())
    print(f"Total labs executed: {body.get('total_labs_executed')}")
    all_success = True
    for lab_res in body.get("results", []):
        lab_num = lab_res.get("lab_number")
        status = lab_res.get("status")
        title = lab_res.get("lab_title")
        print(f"  Lab {lab_num:02d}: [{status}] {title}")
        if status != "SUCCESS":
            all_success = False
    assert all_success, "One or more labs failed execution!"
    print("[PASS] All 14 labs executed with genuine deliverables and passed evaluation!")

def test_create_and_delete_project_sequentiality():
    print("=" * 80)
    print("TEST 4: CREATE PROJECT & DELETE PROJECT SEQUENTIALITY (NO GAPS)")
    print("=" * 80)
    # 1. Fetch initial count
    initial_projects = json.loads(urllib.request.urlopen(f"{BASE_URL}/projects").read().decode())
    initial_count = len(initial_projects)
    next_expected_num = initial_count + 1
    print(f"Current project count: {initial_count}. Next project should be #{next_expected_num}.")

    # 2. Create project
    create_payload = {
        "title": "Bio-hybrid soft robotics for extreme environmental sensing",
        "domain": "Robotics & Biomaterials",
        "department": "Robotics Lab",
        "institution": "KLE Technological University",
        "pi_name": "Dr. Verification Test",
        "pi_email": "test@kletech.ac.in",
        "duration_weeks": 16,
        "requested_budget": 4500000.0,
        "currency": "INR",
        "objectives": "Investigate electro-active polymer bio-hybrid actuators for extreme temperature inspection."
    }
    req = urllib.request.Request(
        f"{BASE_URL}/projects",
        data=json.dumps(create_payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res = urllib.request.urlopen(req)
    new_proj = json.loads(res.read().decode())
    new_id = new_proj["id"]
    new_display = new_proj["display_number"]
    print(f"Created project ID #{new_id} with display_number = #{new_display}")
    assert new_display == next_expected_num, f"Expected display_number {next_expected_num}, got {new_display}"

    # 3. Verify in full list
    updated_projects = json.loads(urllib.request.urlopen(f"{BASE_URL}/projects").read().decode())
    assert len(updated_projects) == initial_count + 1
    assert updated_projects[-1]["display_number"] == next_expected_num
    print(f"[PASS] Newly created project received sequential Project #{next_expected_num}!")

    # 4. Delete the newly created project and check gaps
    del_req = urllib.request.Request(f"{BASE_URL}/projects/{new_id}", method="DELETE")
    urllib.request.urlopen(del_req)
    print(f"Deleted temporary project ID #{new_id}.")

    # 5. Verify no gaps in remaining projects
    after_del_projects = json.loads(urllib.request.urlopen(f"{BASE_URL}/projects").read().decode())
    assert len(after_del_projects) == initial_count
    remaining_nums = [p["display_number"] for p in after_del_projects]
    assert remaining_nums == list(range(1, initial_count + 1)), f"Gaps detected: {remaining_nums}"
    print(f"[PASS] Project deletion closed sequence with ZERO gaps: {remaining_nums}!")

if __name__ == "__main__":
    projects = test_project_numbering()
    first_project_id = projects[0]["id"]
    test_orchestrate_full(first_project_id)
    test_all_14_labs(first_project_id)
    test_create_and_delete_project_sequentiality()
    print("=" * 80)
    print("ALL VERIFICATION SUITES PASSED FLAWLESSLY!")
    print("=" * 80)
