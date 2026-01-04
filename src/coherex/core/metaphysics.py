# File: src/coherex/core/metaphysics.py
from enum import Enum
from typing import Any, Dict, List, Optional
from src.coherex.core.analyzer import BaseAnalyzer, PlaceholderAnalyzer
from src.coherex.core.planner import BasePlanner, PlaceholderPlanner
from src.coherex.core.renderer import BaseRenderer, PlaceholderRenderer
from src.coherex.core.committer import BaseCommitter, PlaceholderCommitter


class CyclePhase(Enum):
    RED = "red"  # Initial analysis, asymmetry identified, rigidities noted
    GREEN = "green"  # Condensation, forming a coherent whole (Planning and Rendering)
    REFACTOR = "refactor"  # Rarefaction, simplifying and clarifying (currently implied/integrated)
    COMMIT = "commit"  # Committing the refined output

class CondensationResult:
    def __init__(
        self,
        phase: CyclePhase,
        success: bool,
        quality_score: float = 0.0,
        message: str = "",
        rigidities_identified: Optional[List[str]] = None,
        knowledge_preserved: Optional[List[str]] = None,
        affected_domains: Optional[List[str]] = None,
    ):
        self.phase = phase
        self.success = success
        self.quality_score = quality_score
        self.message = message
        self.rigidities_identified = rigidities_identified if rigidities_identified is not None else []
        self.knowledge_preserved = knowledge_preserved if knowledge_preserved is not None else []
        self.affected_domains = affected_domains if affected_domains is not None else []

class MetaphysicalEngine:
    def __init__(
        self,
        analyzer: Optional[BaseAnalyzer] = None,
        planner: Optional[BasePlanner] = None,
        renderer: Optional[BaseRenderer] = None,
        committer: Optional[BaseCommitter] = None,
    ):
        # Initialize with provided components or default Placeholder implementations
        self.analyzer: BaseAnalyzer = analyzer if analyzer else PlaceholderAnalyzer()
        self.planner: BasePlanner = planner if planner else PlaceholderPlanner()
        self.renderer: BaseRenderer = renderer if renderer else PlaceholderRenderer()
        self.committer: BaseCommitter = committer if committer else PlaceholderCommitter()
        self.history: List[Dict[str, Any]] = [] # To store cycle results for debugging/auditing

    def execute_cycle(self, input_payload: Dict[str, Any], target_asymmetry: str) -> CondensationResult:
        """
        Executes a full RGR cycle.
        RED: Analyze input, identify rigidities.
        GREEN: Plan and render based on analysis.
        REFACTOR: Refine rendered output (currently implied or part of render/commit).
        COMMIT: Commit the final result.
        """
        # --- RED Phase: Analysis ---
        analysis_result = self.analyzer.analyze(input_payload)
        self.history.append({"phase": CyclePhase.RED, "result": analysis_result})

        if not analysis_result.get("is_valid", False):
            return CondensationResult(
                phase=CyclePhase.RED,
                success=False,
                quality_score=analysis_result.get("quality_score", 0.0),
                message="RED Phase failed: Analysis deemed invalid. Aborting cycle.",
                rigidities_identified=analysis_result.get("rigidities_identified", []),
                knowledge_preserved=analysis_result.get("knowledge_gained", []),
                affected_domains=analysis_result.get("affected_domains", [])
            )
        
        # --- GREEN Phase: Plan and Render (Condensation) ---
        plan = self.planner.generate_plan(analysis_result)
        
        # Initialize an empty dict for rendered_output to ensure it's always defined
        rendered_output: Optional[Dict[str, Any]] = None
        try:
            rendered_output = self.renderer.render(plan, {"input_payload": input_payload, "target_asymmetry": target_asymmetry})
            self.history.append({"phase": CyclePhase.GREEN, "result": rendered_output})
        except ValueError as e: # Catching specific rendering errors
            # --- FIX START ---
            # Append GREEN phase failure to history before returning
            green_phase_failure_result = {
                "success": False,
                "error_message": str(e),
                "rigidities_identified": analysis_result.get("rigidities_identified", []),
                "knowledge_preserved": analysis_result.get("knowledge_gained", []),
                "affected_domains": analysis_result.get("affected_domains", [])
            }
            self.history.append({"phase": CyclePhase.GREEN, "result": green_phase_failure_result})
            # --- FIX END ---
            return CondensationResult(
                phase=CyclePhase.GREEN,
                success=False,
                quality_score=analysis_result.get("quality_score", 0.0), # Pass initial quality from analysis
                message=f"GREEN Phase failed: Rendering error - {e}",
                rigidities_identified=analysis_result.get("rigidities_identified", []),
                knowledge_preserved=analysis_result.get("knowledge_gained", []),
                affected_domains=analysis_result.get("affected_domains", [])
            )
        
        # --- REFACTOR Phase: Rarefaction (Simplified for now, could be a separate step) ---
        # For Episode 2, we assume any refactoring logic is either part of rendering
        # or will be a more complex interaction in future episodes.
        # The engine primarily orchestrates RED, GREEN (plan/render), and COMMIT.
        
        # --- COMMIT Phase ---
        # Ensure rendered_output is not None before committing, though the try-except should handle it
        if rendered_output is None:
             # This scenario implies an unexpected state if the exception wasn't caught or rendered_output wasn't set
             # Add appropriate error handling or raise an exception if this state is invalid
             return CondensationResult(
                phase=CyclePhase.GREEN, # or a new UNEXPECTED_FAILURE phase
                success=False,
                quality_score=0.0,
                message="Unexpected error: Rendered output was None before commit.",
                rigidities_identified=analysis_result.get("rigidities_identified", []),
                knowledge_preserved=analysis_result.get("knowledge_gained", []),
                affected_domains=analysis_result.get("affected_domains", [])
            )

        commit_result = self.committer.commit(rendered_output, {"input_payload": input_payload, "target_asymmetry": target_asymmetry})
        self.history.append({"phase": CyclePhase.COMMIT, "result": commit_result})

        # Final result based on overall success and the last successful quality score
        final_quality_score = analysis_result.get("quality_score", 0.0) # Placeholder for more complex aggregation

        return CondensationResult(
            phase=CyclePhase.COMMIT, # Indicates successful completion through this phase
            success=True,
            quality_score=final_quality_score,
            message="RGR cycle completed successfully.",
            rigidities_identified=analysis_result.get("rigidities_identified", []),
            knowledge_preserved=analysis_result.get("knowledge_gained", []),
            affected_domains=analysis_result.get("affected_domains", [])
        )