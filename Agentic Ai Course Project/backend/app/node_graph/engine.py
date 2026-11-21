from typing import Dict, Any, List, Callable, Optional
from datetime import datetime

class GraphNode:
    """Represents an executable node in the research grant DAG workflow."""
    def __init__(
        self,
        node_id: str,
        name: str,
        responsible_agent: str,
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
        success_condition: Callable[[Dict[str, Any]], bool],
        retry_limit: int = 2
    ):
        self.node_id = node_id
        self.name = name
        self.responsible_agent = responsible_agent
        self.handler = handler
        self.success_condition = success_condition
        self.retry_limit = retry_limit
        
        self.status = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED, RETRIED
        self.retry_count = 0
        self.input_data: Optional[Dict[str, Any]] = None
        self.output_data: Optional[Dict[str, Any]] = None
        self.error_message: Optional[str] = None
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None

    def execute(self, state: Dict[str, Any]) -> bool:
        self.status = "RUNNING"
        self.started_at = datetime.utcnow().isoformat()
        self.input_data = dict(state)
        
        try:
            res = self.handler(state)
            self.output_data = res
            
            # Check success condition
            if self.success_condition(res):
                self.status = "COMPLETED"
                self.completed_at = datetime.utcnow().isoformat()
                state.update(res)
                return True
            else:
                raise ValueError("Node output failed validation predicate.")
        except Exception as e:
            self.error_message = str(e)
            if self.retry_count < self.retry_limit:
                self.retry_count += 1
                self.status = "RETRIED"
                return self.execute(state)
            else:
                self.status = "FAILED"
                self.completed_at = datetime.utcnow().isoformat()
                return False

class AgenticNodeGraphEngine:
    """
    Workflow graph engine supporting sequential & branched execution,
    node inspection, retry strategy, and execution graph states.
    """
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.nodes: List[GraphNode] = []
        self.current_state: Dict[str, Any] = {}

    def add_node(self, node: GraphNode):
        self.nodes.append(node)

    def run_graph(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        self.current_state = dict(initial_state)
        execution_trace = []

        all_passed = True
        for node in self.nodes:
            success = node.execute(self.current_state)
            execution_trace.append({
                "node_id": node.node_id,
                "name": node.name,
                "responsible_agent": node.responsible_agent,
                "status": node.status,
                "retries": node.retry_count,
                "error": node.error_message,
                "output_keys": list(node.output_data.keys()) if node.output_data else []
            })
            if not success:
                all_passed = False
                break

        return {
            "all_passed": all_passed,
            "total_nodes": len(self.nodes),
            "completed_nodes": sum(1 for n in self.nodes if n.status == "COMPLETED"),
            "graph_trace": execution_trace,
            "final_state": self.current_state
        }

    def get_graph_schema(self) -> List[Dict[str, Any]]:
        """Returns visual representation schema for the UI."""
        return [
            {
                "id": n.node_id,
                "label": n.name,
                "agent": n.responsible_agent,
                "status": n.status,
                "retries": n.retry_count,
                "retry_limit": n.retry_limit
            }
            for n in self.nodes
        ]
