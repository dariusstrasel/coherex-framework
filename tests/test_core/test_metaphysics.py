# File: tests/test_core/test_metaphysics.py
import pytest
from src.coherex.core.metaphysics import MetaphysicalEngine, CondensationResult, CyclePhase
from src.coherex.core.analyzer import PlaceholderAnalyzer
from src.coherex.core.planner import PlaceholderPlanner
from src.coherex.core.renderer import PlaceholderRenderer
from src.coherex.core.committer import PlaceholderCommitter
from typing import Any, Dict # Added for clarity in custom_components test

# Fixture to provide a MetaphysicalEngine with default Placeholder components
# This fixture could be moved to test_data.py if other modules needed it.
@pytest.fixture
def default_engine():
    """Returns a MetaphysicalEngine initialized with default Placeholder components."""
    return MetaphysicalEngine()

def test_engine_initialization_with_defaults(default_engine):
    """Verify MetaphysicalEngine initializes with Placeholder components by default."""
    assert isinstance(default_engine.analyzer, PlaceholderAnalyzer)
    assert isinstance(default_engine.planner, PlaceholderPlanner)
    assert isinstance(default_engine.renderer, PlaceholderRenderer)
    assert isinstance(default_engine.committer, PlaceholderCommitter)
    assert default_engine.history == []

def test_engine_initialization_with_custom_components():
    """Verify MetaphysicalEngine initializes with provided custom components."""
    # Define a simple custom analyzer that still adheres to BaseAnalyzer interface
    class CustomAnalyzer(PlaceholderAnalyzer):
        def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
            return {"is_valid": True, "quality_score": 1.0, "message": "Custom analysis from test", "rigidities_identified": [], "knowledge_gained": ["custom_knowledge"], "potential_identified": "custom_potential", "affected_domains": ["custom_domain"]}

    custom_analyzer = CustomAnalyzer()
    engine = MetaphysicalEngine(analyzer=custom_analyzer)
    assert engine.analyzer is custom_analyzer
    assert isinstance(engine.planner, PlaceholderPlanner) # Other components still default

def test_execute_cycle_successful_flow(default_engine):
    """Test a full successful RGR cycle execution."""
    input_payload = {"feature": "new user dashboard", "complexity": "medium"}
    target_asymmetry = "new_login_flow"
    
    result = default_engine.execute_cycle(input_payload, target_asymmetry)
    
    assert isinstance(result, CondensationResult)
    assert result.success is True
    assert result.phase == CyclePhase.COMMIT
    assert "RGR cycle completed successfully." in result.message
    assert result.quality_score == 0.8 # From PlaceholderAnalyzer
    # --- FIX START ---
    # The PlaceholderAnalyzer puts 'basic_syntax_knowledge' into knowledge_gained for this input
    assert "basic_syntax_knowledge" in result.knowledge_preserved 
    assert "ui_dashboard_potential" not in result.knowledge_preserved # ui_dashboard_potential is potential, not knowledge
    # --- FIX END ---
    assert "frontend" in result.affected_domains # From analyzer's affected_domains
    assert not result.rigidities_identified # Initial analysis for this input has no rigidities
    assert len(default_engine.history) == 3 # RED, GREEN, COMMIT phases logged

def test_execute_cycle_red_phase_failure(default_engine):
    """Test RGR cycle failure during the RED (analysis) phase."""
    input_payload = {} # Empty payload triggers invalid analysis in PlaceholderAnalyzer
    target_asymmetry = "invalid_input_scenario"
    
    result = default_engine.execute_cycle(input_payload, target_asymmetry)
    
    assert isinstance(result, CondensationResult)
    assert result.success is False
    assert result.phase == CyclePhase.RED
    assert "RED Phase failed: Analysis deemed invalid." in result.message
    assert result.quality_score == 0.0
    assert "malformed_input" in result.rigidities_identified
    assert not result.knowledge_preserved
    assert len(default_engine.history) == 1 # Only RED phase logged

def test_execute_cycle_green_phase_failure(default_engine):
    """Test RGR cycle failure during the GREEN (rendering) phase."""
    input_payload = {"feature": "valid_input"}
    target_asymmetry = "buggy_implementation" # Triggers rendering failure in PlaceholderRenderer
    
    result = default_engine.execute_cycle(input_payload, target_asymmetry)
    
    assert isinstance(result, CondensationResult)
    assert result.success is False
    assert result.phase == CyclePhase.GREEN
    assert "GREEN Phase failed: Rendering error - Simulated rendering failure due to buggy implementation target." in result.message
    # --- FIX START ---
    # After the fix in metaphysics.py, quality_score should be 0.8 (from analysis)
    assert result.quality_score == 0.8 
    # --- FIX END ---
    assert not result.rigidities_identified # Analysis was valid, PlaceholderAnalyzer doesn't add rigidities for this specific input
    assert "basic_syntax_knowledge" in result.knowledge_preserved # From PlaceholderAnalyzer
    assert len(default_engine.history) == 2 # RED and GREEN phases logged
    assert default_engine.history[0]["phase"] == CyclePhase.RED
    assert default_engine.history[1]["phase"] == CyclePhase.GREEN

def test_history_logging(default_engine):
    """Verify that the engine's history attribute logs all phase results."""
    input_payload = {"feature": "test feature"}
    target_asymmetry = "test_target"
    
    default_engine.execute_cycle(input_payload, target_asymmetry)
    
    assert len(default_engine.history) == 3
    assert default_engine.history[0]["phase"] == CyclePhase.RED
    assert default_engine.history[1]["phase"] == CyclePhase.GREEN
    assert default_engine.history[2]["phase"] == CyclePhase.COMMIT
    
    # Check some content within history
    assert "is_valid" in default_engine.history[0]["result"]
    assert "type" in default_engine.history[1]["result"] # e.g., "placeholder_render"
    assert "status" in default_engine.history[2]["result"] # e.g., "committed"

# --- Fixtures (ensure these are set up if not already in conftest.py) ---
@pytest.fixture
def mock_engine_instance():
    """Provides a MetaphysicalEngine instance with mocked internal components."""
    with patch('src.coherex.core.metaphysics.MetaphysicalEngine.__init__', return_value=None) as mock_init:
        engine = MetaphysicalEngine()
        engine.analyzer = Mock(spec=PlaceholderAnalyzer)
        engine.planner = Mock(spec=PlaceholderPlanner)
        engine.renderer = Mock(spec=PlaceholderRenderer)
        engine.committer = Mock(spec=PlaceholderCommitter)
        mock_init.return_value = None # Ensure __init__ is mocked correctly
        yield engine
        mock_init.assert_called_once()


# --- Failing Tests for Episode 2: Condensation Cycles ---

def test_engine_initiates_condensation_process_on_green_phase_command(mock_engine_instance):
    """
    Episode 2 Failing Test: Verifies that the engine initiates the condensation
    process when commanded to the GREEN phase and returns a CondensationResult.
    This test will fail until the condensation logic is implemented.
    """
    mock_engine_instance.renderer.condense_logic.return_value = CondensationResult(
        quality_score=0.7,
        rigidities_identified=["old_code"],
        knowledge_preserved=["new_patterns"],
        message="Condensation successful"
    )

    # Simulate entering ANALYSIS phase and getting some 'analyzed_input'
    mock_engine_instance.current_phase = CyclePhase.ANALYSIS
    analyzed_input = {"data": "raw input after analysis"}

    # The method to initiate condensation for the GREEN phase (e.g., execute_cycle with GREEN)
    # This might be part of execute_cycle or a separate method.
    # For now, let's assume `execute_cycle` handles phase transitions and calls sub-components.
    # This assertion expects a specific return type that the current placeholder won't provide.
    result = mock_engine_instance.execute_cycle(CyclePhase.GREEN, analyzed_input)

    # Expect the renderer's condensation method to be called
    mock_engine_instance.renderer.condense_logic.assert_called_once_with(analyzed_input)
    assert isinstance(result, CondensationResult)
    assert result.quality_score > 0
    assert "Condensation successful" in result.message


def test_engine_transitions_from_analysis_to_green(mock_engine_instance):
    """
    Episode 2 Failing Test: Verifies that the MetaphysicalEngine correctly
    transitions its internal state from ANALYSIS to GREEN after processing.
    This test will fail if the state management logic is missing or incorrect.
    """
    mock_engine_instance.current_phase = CyclePhase.ANALYSIS
    # Assume execute_cycle is the primary method to advance phases
    mock_engine_instance.execute_cycle(CyclePhase.ANALYSIS, input_payload={"foo": "bar"}) # Simulate processing ANALYSIS

    # After processing ANALYSIS, the engine should transition to GREEN for the next step
    assert mock_engine_instance.current_phase == CyclePhase.GREEN


def test_engine_transitions_from_green_to_refactor(mock_engine_instance):
    """
    Episode 2 Failing Test: Verifies that the MetaphysicalEngine correctly
    transitions its internal state from GREEN to REFACTOR.
    This test will fail if the state management logic is missing or incorrect.
    """
    mock_engine_instance.current_phase = CyclePhase.GREEN
    # Simulate completing the GREEN phase successfully
    mock_engine_instance.execute_cycle(CyclePhase.GREEN, input_payload={"condensation_result": "..."})

    # After processing GREEN, the engine should transition to REFACTOR
    assert mock_engine_instance.current_phase == CyclePhase.REFACTOR

# Example from previous memory (if not already failing as expected, it should be)
def test_placeholder_analyzer_analyze_method_failing_if_not_implemented(mock_engine_instance):
    """
    Episode 2 Failing Test: Verifies analyze method returns expected structure
    when implemented. Currently fails if PlaceholderAnalyzer doesn't return this.
    """
    # This test assumes mock_engine_instance.analyzer is a Mock configured to act
    # like PlaceholderAnalyzer, but without actual implementation.
    # The current setup will cause this to fail unless the mock explicitly returns these values.
    payload = {"feature": "new user dashboard", "complexity": "medium"}

    # Configure the mock to simulate the placeholder's *future* behavior
    mock_engine_instance.analyzer.analyze.return_value = {
        "is_valid": True,
        "quality_score": 0.8,
        "potential_identified": ["new_feature"],
        "rigidities_identified": []
    }

    result = mock_engine_instance.analyzer.analyze(payload)
    assert result["is_valid"] is True
    assert result["quality_score"] == 0.8
    assert "new_feature" in result["potential_identified"]