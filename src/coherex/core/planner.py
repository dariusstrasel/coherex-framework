from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BasePlanner(ABC):
    @abstractmethod
    def generate_plan(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Generates a list of actionable steps based on analysis results.
        """
        pass

class PlaceholderPlanner(BasePlanner):
    def generate_plan(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Minimal placeholder logic: generates a plan based on identified rigidities and potential.
        """
        plan: List[str] = []
        rigidities = analysis_result.get("rigidities_identified", [])
        potential = analysis_result.get("potential_identified", None)

        if "high_complexity" in rigidities:
            plan.append("break_down_complex_modules")
        if "malformed_input" in rigidities:
            plan.append("define_input_validation_schema")
        if potential == "ui_dashboard_potential":
            plan.append("design_user_interface")
            plan.append("implement_data_visualization")
        elif potential:
            plan.append(f"explore_potential: {potential}")
        
        if not plan:
            plan.append("review_general_architecture") # Default plan
        return plan