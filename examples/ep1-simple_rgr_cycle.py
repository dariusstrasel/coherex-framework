# File: examples/simple_rgr_cycle.py
import sys
import os
from typing import Any, Dict

# Calculate the absolute path to the project root.
# This script is in the 'examples/' directory, so we go up one level (..)
# to reach the project root 'coherex-metaphysical-framework'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the project root into sys.path to make 'src' and 'tests' importable
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now, import modules using their full paths relative to the project root.
# Python will now correctly find 'src' and 'tests' as top-level packages.
from src.coherex.core.metaphysics import MetaphysicalEngine, CondensationResult, CyclePhase
from tests.test_core.mocks.MockComponents import MockAnalyzer, MockPlanner, MockRenderer, MockCommitter

def main():
    """
    Demonstrates running simple MetaphysicalEngine RGR cycles with mock components.
    This serves as an example and user exercise to verify process flow.
    """
    analyzer_instance = MockAnalyzer()
    planner_instance = MockPlanner()
    renderer_instance = MockRenderer()
    committer_instance = MockCommitter()

    engine = MetaphysicalEngine(
        analyzer=analyzer_instance,
        planner=planner_instance,
        renderer=renderer_instance,
        committer=committer_instance
    )

    print("Starting RGR cycle demonstration with mock components...")
    try:
        # The execute_cycle method takes input_payload and target_asymmetry
        # It internally starts with the RED phase for analysis.
        input_data: Dict[str, Any] = {"context": "Demonstration of RGR cycle with mock components.", "some_initial_data": 123}
        target_description = "metaphysical_framework_development"

        result: CondensationResult = engine.execute_cycle(
            input_payload=input_data,
            target_asymmetry=target_description
        )

        print("\nRGR cycle completed successfully.")
        print(f"Final Phase: {result.phase.value}")
        print(f"Success: {result.success}")
        print(f"Quality Score: {result.quality_score:.2f}")
        print(f"Message: {result.message}")
        print(f"Rigidities Identified: {', '.join(result.rigidities_identified)}")
        print(f"Knowledge Preserved: {', '.join(result.knowledge_preserved)}")
        print(f"Affected Domains: {', '.join(result.affected_domains)}")

    except Exception as e:
        print(f"\nAn error occurred during cycle execution: {e}")
        print("Please ensure your MockComponents and MetaphysicalEngine methods are correctly implemented for this example.")

if __name__ == "__main__":
    main()