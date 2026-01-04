# File: tests/mocks/mock_components.py
from typing import Dict, List, Any
from datetime import datetime

# Define Mock components for testing purposes
class MockAnalyzer:
    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # This implementation is for testing MetaphysicalEngine's flow, not the analyzer's logic
        if not payload or "feature" not in payload:
            return {"is_valid": False, "rigidities": ["malformed_input"], "knowledge_gained": [], "affected_domains": []}
        return {
            "is_valid": True,
            "rigidities": ["legacy_db_schema"] if payload.get("feature") == "complex_feature" else [],
            "knowledge_gained": ["api_pattern_suggestion"],
            "quality_score": 0.75 if payload.get("feature") == "complex_feature" else 0.9,
            "potential_identified": f"Improved {payload['feature']}",
            "affected_domains": ["core_logic"] # Added affected_domains
        }

class MockPlanner:
    def generate_plan(self, analysis_result: Dict[str, Any]) -> List[str]:
        # This implementation is for testing MetaphysicalEngine's flow, not the planner's logic
        rigidities = analysis_result.get("rigidities", [])
        plan = []
        if "legacy_db_schema" in rigidities:
            plan.append("refactor_db_access_layer")
        if not plan:
            plan.append("optimize_existing_code")
        return plan

class MockRenderer:
    def execute_rarefaction(self, plan: List[str]) -> Dict[str, Any]:
        # This implementation is for testing MetaphysicalEngine's flow, not the renderer's logic
        released = []
        preserved = []
        if "refactor_db_access_layer" in plan:
            released.append("legacy_db_schema_rigidity")
            preserved.append("decoupled_db_access_pattern")
        return {"rigidities_released": released, "knowledge_preserved": preserved, "success": True, "quality_score": 0.8, "affected_domains": ["database"]}

    def condense_logic(self, context: Dict[str, Any], target_asymmetry: str) -> Dict[str, Any]:
        # This implementation is for testing MetaphysicalEngine's flow, not the renderer's logic
        return {
            "success": True,
            "quality_score": 0.95,
            "new_rigidities": [],
            "knowledge_preserved": context.get("knowledge_preserved", []) + ["new_design_concept"],
            "affected_domains": ["frontend", "backend"] # Added affected_domains
        }

class MockCommitter:
    def commit_changes(self, message: str, result: Any, rarefaction_result_info: Any) -> str:
        # This implementation is for testing MetaphysicalEngine's flow, not the committer's logic
        return f"mock_git_hash_{hash(message + str(datetime.now())) & 0xFFFFFFFF}"