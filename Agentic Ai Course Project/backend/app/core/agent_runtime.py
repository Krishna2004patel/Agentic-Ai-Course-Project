import inspect
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime

class ToolRegistry:
    """Registry of executable tools with contracts, input schema and validation."""
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, func: Callable, description: str, input_schema: Dict[str, Any]):
        self._tools[name] = {
            "name": name,
            "func": func,
            "description": description,
            "input_schema": input_schema
        }

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": v["name"],
                "description": v["description"],
                "input_schema": v["input_schema"]
            }
            for v in self._tools.values()
        ]

    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        if name not in self._tools:
            return {"error": f"Tool '{name}' not found in registry."}
        tool = self._tools[name]
        try:
            func = tool["func"]
            if inspect.iscoroutinefunction(func):
                raise ValueError("Async tool must be called via execute_async")
            result = func(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

class SkillRegistry:
    """Registry of reusable structured skills."""
    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, instructions: str, workflow: List[str], constraints: List[str], handler: Callable):
        self._skills[name] = {
            "name": name,
            "instructions": instructions,
            "workflow": workflow,
            "constraints": constraints,
            "handler": handler
        }

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self._skills.get(name)

    def list_skills(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": k,
                "instructions": v["instructions"],
                "workflow": v["workflow"],
                "constraints": v["constraints"]
            }
            for k, v in self._skills.items()
        ]

    def execute(self, name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._skills:
            return {"error": f"Skill '{name}' not registered."}
        skill = self._skills[name]
        try:
            return skill["handler"](context)
        except Exception as e:
            return {"error": str(e), "skill": name}

class ScopedMemory:
    """Project-scoped memory container protecting boundaries between different projects."""
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.session_data: Dict[str, Any] = {}
        self.long_term_facts: Dict[str, Any] = {}
        self.decisions: List[Dict[str, Any]] = []

    def set_session(self, key: str, value: Any):
        self.session_data[key] = value

    def get_session(self, key: str, default=None):
        return self.session_data.get(key, default)

    def record_fact(self, key: str, value: Any, source: str = "agent"):
        self.long_term_facts[key] = {
            "value": value,
            "source": source,
            "updated_at": datetime.utcnow().isoformat()
        }

    def get_fact(self, key: str) -> Optional[Dict[str, Any]]:
        return self.long_term_facts.get(key)

    def record_decision(self, topic: str, rationale: str, decided_by: str = "agent"):
        self.decisions.append({
            "topic": topic,
            "rationale": rationale,
            "decided_by": decided_by,
            "timestamp": datetime.utcnow().isoformat()
        })

class AgentRuntime:
    """
    OpenCLA/OpenClaw-style Agent Runtime.
    Core execution loop: Goal -> Plan -> Act -> Observe -> Revise.
    """
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.tool_registry = ToolRegistry()
        self.skill_registry = SkillRegistry()
        self.memory = ScopedMemory(project_id)
        self.audit_log: List[Dict[str, Any]] = []

    def log_action(self, stage: str, action: str, details: Any):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "project_id": self.project_id,
            "stage": stage,
            "action": action,
            "details": details
        }
        self.audit_log.append(entry)
        return entry

    def run_goal_loop(self, goal_predicate: Callable[[Dict[str, Any]], bool], 
                      planner_func: Callable[[Dict[str, Any], int], Dict[str, Any]], 
                      context: Dict[str, Any], 
                      max_iterations: int = 6) -> Dict[str, Any]:
        """
        Executes the autonomous loop until the goal predicate is satisfied or max iterations reached.
        """
        iteration = 0
        self.log_action("START", "Beginning agent autonomous loop", {"initial_context": context})

        while not goal_predicate(context) and iteration < max_iterations:
            iteration += 1
            # 1. PLAN
            step_plan = planner_func(context, iteration)
            self.log_action("PLAN", f"Iteration {iteration} plan generated", step_plan)

            action = step_plan.get("action")
            action_type = step_plan.get("action_type")  # tool, skill, question, mutate
            params = step_plan.get("parameters", {})

            # 2. ACT
            observation = None
            if action_type == "tool":
                observation = self.tool_registry.execute(action, **params)
            elif action_type == "skill":
                observation = self.skill_registry.execute(action, params)
            elif action_type == "mutate":
                observation = {"mutated_field": action, "new_value": params}
            else:
                observation = {"info": f"Executed action {action}", "params": params}

            # 3. OBSERVE
            self.log_action("OBSERVE", f"Iteration {iteration} observed outcome", observation)
            
            # 4. REVISE / UPDATE CONTEXT
            if "updates" in step_plan:
                context.update(step_plan["updates"])
            if observation and isinstance(observation, dict):
                context[f"iter_{iteration}_result"] = observation

        success = goal_predicate(context)
        stop_reason = "Goal satisfied" if success else "Max iterations reached without achieving goal"
        self.log_action("STOP", stop_reason, {"final_status": success, "iterations": iteration})

        return {
            "success": success,
            "stop_reason": stop_reason,
            "iterations": iteration,
            "context": context,
            "audit_trail": self.audit_log
        }
