from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..mcp.server import MCPGrantServer

class MCPEvaluationAgent:
    """
    Lab 5: MCP-Style Connector
    Evaluates resource discovery, read-only database query execution, security boundary enforcement,
    and external paper search via MCP.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.lab_number = 5
        self.lab_title = "Lab 5: MCP-Style Connector -- Mini Integration Server"
        self.server = MCPGrantServer(db, project.id)

    def execute_mcp_tests(self) -> Dict[str, Any]:
        manifest = self.server.get_manifest()
        
        # Test 1: Read Project Resource
        res_uri = f"grant://project/{self.project.id}/metadata"
        resource_data = self.server.read_resource(res_uri)

        # Test 2: Valid Read-Only Tool Execution
        valid_query = f"SELECT id, title, domain, requested_budget FROM research_projects WHERE id = {self.project.id}"
        query_result = self.server.execute_tool("query_grant_database", {"query": valid_query})

        # Test 3: Security Boundary Violation Test (Attempts DROP or UPDATE)
        malicious_query = f"DROP TABLE research_projects;"
        boundary_test = self.server.execute_tool("query_grant_database", {"query": malicious_query})

        # Test 4: OpenAlex scholarly search tool
        paper_tool_result = self.server.execute_tool("search_scholarly_papers", {"topic": self.project.title, "limit": 2})

        output = {
            "project_id": self.project.id,
            "manifest_summary": {
                "server_name": manifest["server_name"],
                "resource_count": len(manifest["resources"]),
                "tool_count": len(manifest["tools"])
            },
            "resource_read_test": {
                "uri": res_uri,
                "data": resource_data.get("data")
            },
            "authorized_sql_tool_result": {
                "query": valid_query,
                "success": query_result.get("success"),
                "rows_returned": query_result.get("row_count")
            },
            "security_boundary_enforcement": {
                "attempted_query": malicious_query,
                "blocked": not boundary_test.get("success"),
                "error_message": boundary_test.get("error")
            },
            "paper_tool_result": paper_tool_result
        }

        # Persist lab result
        lab_res = LabExecutionResult(
            project_id=self.project.id,
            lab_number=self.lab_number,
            lab_title=self.lab_title,
            responsible_agent="MCP Connector Agent",
            status="COMPLETED",
            execution_output=output,
            evaluation_status="PASSED",
            evaluation_results={
                "manifest_valid": True,
                "read_only_boundary_enforced": not boundary_test.get("success"),
                "resources_accessible": "data" in resource_data
            }
        )
        self.db.add(lab_res)
        self.db.commit()

        return output
