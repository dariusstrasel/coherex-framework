# File: tests/test_core/test_data.py
from datetime import datetime
from typing import List, Optional
import pytest # Not strictly needed if only data, but useful for fixtures

from src.coherex.core.metaphysics import CondensationResult, CyclePhase

class TestData:
    """Central repository for shared test data and utility functions."""

    @staticmethod
    def get_condensation_result_success_green(
        quality_score: float = 0.9,
        rigidities_identified: Optional[List[str]] = None,
        knowledge_preserved: Optional[List[str]] = None,
        affected_domains: Optional[List[str]] = None,
        message: str = "Added login feature",
        # --- FIX START ---
        # Removed timestamp as CondensationResult does not accept it in __init__
        # timestamp: Optional[datetime] = None 
        # --- FIX END ---
    ) -> CondensationResult:
        """Returns a typical successful GREEN phase CondensationResult."""
        return CondensationResult(
            phase=CyclePhase.GREEN,
            success=True,
            quality_score=quality_score,
            rigidities_identified=rigidities_identified if rigidities_identified is not None else ["new_debt"],
            knowledge_preserved=knowledge_preserved if knowledge_preserved is not None else ["new_pattern"],
            affected_domains=affected_domains if affected_domains is not None else ["frontend"],
            message=message,
            # --- FIX START ---
            # Do not pass timestamp to CondensationResult.__init__
            # timestamp=timestamp if timestamp is not None else datetime.now() 
            # --- FIX END ---
        )

    # --- FIX START ---
    # Add other helper functions as needed if they use CondensationResult,
    # ensuring they also do not pass a timestamp.
    @staticmethod
    def get_condensation_result_success_refactor(
        quality_score: float = 0.8,
        rigidities_identified: Optional[List[str]] = None,
        knowledge_preserved: Optional[List[str]] = None,
        affected_domains: Optional[List[str]] = None,
        message: str = "Cleaned up old code"
    ) -> CondensationResult:
        """Returns a typical successful REFACTOR phase CondensationResult."""
        return CondensationResult(
            phase=CyclePhase.REFACTOR,
            success=True,
            quality_score=quality_score,
            rigidities_identified=rigidities_identified if rigidities_identified is not None else ["old_rigidity"],
            knowledge_preserved=knowledge_preserved if knowledge_preserved is not None else ["clean_architecture"],
            affected_domains=affected_domains if affected_domains is not None else ["backend"],
            message=message,
        )
    # --- FIX END ---