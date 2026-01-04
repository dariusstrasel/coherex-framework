# NEW: docs/episodes/01-condensation-cycle.md
---
title: "Episode 1: The Condensation Cycle"
teaching: 15
exercises: 10
questions:
  - "What is a condensation cycle in metaphysical programming?"
  - "How does Red-Green-Refactor map to condensation and rarefaction?"
objectives:
  - "Explain the condensation-rarefaction cycle."
  - "Execute a basic RGR cycle using the COHEREX CLI."
keypoints:
  - "Condensation is the process of potential solidifying into working code."
  - "Rarefaction is the deliberate release of rigidity through refactoring."
  - "Each RGR cycle should be small, verifiable, and committed atomically."
---

## The Metaphysical Basis

In COHEREX, development is seen as a breath:
1. **Inhalation (Condensation)**: Requirements → Tests → Working Code
2. **Exhalation (Rarefaction)**: Working Code → Refactored → Released Knowledge

## A Practical Example

Let's trace a real cycle:

```bash
# 1. RED: We have a failing test
$ coherex run-test tests/test_shopping.py::test_discount
✗ FAILED: Expected total 90, got 100

# 2. GREEN: Implement minimal fix
$ coherex condense --test test_discount --strategy minimal
✓ Implementing discount calculation...
✓ Test passes!

# 3. REFACTOR: Apply rarefaction
$ coherex rarefy --strategy extract-method
✓ Extracted calculate_discount() method...
✓ Commit created: [CONDENSATION] Add discount logic