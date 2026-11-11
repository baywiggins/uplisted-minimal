"""Offline Microsoft Agent Framework smoke runtime."""

from __future__ import annotations

from dataclasses import dataclass

from agent_framework import Agent

from uplisted.providers.scripted_chat_client import ScriptedChatClient


@dataclass(frozen=True)
class MafSmokeResult:
    """Observable evidence from the harmless framework tool round trip."""

    final_text: str
    model_turns: int
    tool_calls: int
    tool_result_seen_by_model: bool


async def run_maf_smoke() -> MafSmokeResult:
    """Run one framework-managed tool call with no external provider."""
    tool_calls = 0

    def fixture_ping() -> str:
        """Return the deterministic fixture response used by this offline smoke test."""
        nonlocal tool_calls
        tool_calls += 1
        return "fixture-pong"

    client = ScriptedChatClient()
    agent = Agent(
        client=client,
        name="StageOneSmokeAgent",
        instructions="Use fixture_ping once, then confirm the result.",
        tools=[fixture_ping],
    )
    response = await agent.run("Run the offline smoke tool.")

    return MafSmokeResult(
        final_text=response.text,
        model_turns=client.model_turns,
        tool_calls=tool_calls,
        tool_result_seen_by_model=client.tool_result_seen_by_model,
    )
