"""Integration test for the real offline MAF function loop."""

from __future__ import annotations

import pytest

from uplisted.agent.runtime import run_maf_smoke


@pytest.mark.asyncio
async def test_maf_runs_scripted_model_tool_result_final_round_trip() -> None:
    result = await run_maf_smoke()

    assert result.final_text == "fixture-pong confirmed"
    assert result.model_turns == 2
    assert result.tool_calls == 1
    assert result.tool_result_seen_by_model is True
