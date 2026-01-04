import pytest
from src.coherex.core.planner import BasePlanner, PlaceholderPlanner

def test_placeholder_planner_implements_base_planner():
    """Verify PlaceholderPlanner correctly implements BasePlanner."""
    planner = PlaceholderPlanner()
    assert isinstance(planner, BasePlanner)
    assert hasattr(planner, 'generate_plan')
    assert callable(getattr(planner, 'generate_plan'))

def test_placeholder_planner_with_high_complexity_rigidity():
    """Test generate_plan with analysis result containing 'high_complexity' rigidity."""
    planner = PlaceholderPlanner()
    analysis_result = {
        "rigidities_identified": ["high_complexity"],
        "potential_identified": "general_optimization"
    }
    plan = planner.generate_plan(analysis_result)
    assert "break_down_complex_modules" in plan
    assert "explore_potential: general_optimization" in plan
    assert len(plan) == 2

def test_placeholder_planner_with_malformed_input_rigidity():
    """Test generate_plan with analysis result containing 'malformed_input' rigidity."""
    planner = PlaceholderPlanner()
    analysis_result = {
        "rigidities_identified": ["malformed_input"],
        "potential_identified": "data_integrity"
    }
    plan = planner.generate_plan(analysis_result)
    assert "define_input_validation_schema" in plan
    assert "explore_potential: data_integrity" in plan
    assert len(plan) == 2

def test_placeholder_planner_with_ui_dashboard_potential():
    """Test generate_plan with analysis result identifying 'ui_dashboard_potential'."""
    planner = PlaceholderPlanner()
    analysis_result = {
        "rigidities_identified": [],
        "potential_identified": "ui_dashboard_potential"
    }
    plan = planner.generate_plan(analysis_result)
    assert "design_user_interface" in plan
    assert "implement_data_visualization" in plan
    assert len(plan) == 2

def test_placeholder_planner_empty_analysis_result():
    """Test generate_plan with an empty analysis result (should return default plan)."""
    planner = PlaceholderPlanner()
    analysis_result = {}
    plan = planner.generate_plan(analysis_result)
    assert plan == ["review_general_architecture"]

def test_placeholder_planner_mixed_rigidities_and_potentials():
    """Test generate_plan with a mix of rigidities and potentials."""
    planner = PlaceholderPlanner()
    analysis_result = {
        "rigidities_identified": ["high_complexity", "malformed_input"],
        "potential_identified": "ui_dashboard_potential"
    }
    plan = planner.generate_plan(analysis_result)
    assert "break_down_complex_modules" in plan
    assert "define_input_validation_schema" in plan
    assert "design_user_interface" in plan
    assert "implement_data_visualization" in plan
    assert len(plan) == 4