"""Deterministic chat client for exercising the real MAF tool loop offline."""

from __future__ import annotations

from collections.abc import AsyncIterable, Awaitable, Mapping, Sequence
from typing import Any

from agent_framework import (
    BaseChatClient,
    ChatResponse,
    ChatResponseUpdate,
    Content,
    FunctionInvocationLayer,
    Message,
    ResponseStream,
)


class ScriptedChatClient(FunctionInvocationLayer[dict[str, Any]], BaseChatClient[dict[str, Any]]):
    """Emit a fixed tool proposal followed by a fixed final response."""

    def __init__(self) -> None:
        super().__init__(
            function_invocation_configuration={
                "allow_concurrent_invocation": False,
                "max_function_calls": 1,
                "max_iterations": 2,
            }
        )
        self.model_turns = 0
        self.tool_result_seen_by_model = False

    def _inner_get_response(
        self,
        *,
        messages: Sequence[Message],
        stream: bool,
        options: Mapping[str, Any],
        **kwargs: Any,
    ) -> Awaitable[ChatResponse[None]] | ResponseStream[ChatResponseUpdate, ChatResponse[None]]:
        del options, kwargs
        self.model_turns += 1
        self.tool_result_seen_by_model = self.tool_result_seen_by_model or any(
            content.type == "function_result"
            for message in messages
            for content in message.contents
        )
        if self.model_turns == 1:
            update = ChatResponseUpdate(
                role="assistant",
                contents=[Content.from_function_call("fixture-call-1", "fixture_ping", arguments={})],
            )
        else:
            update = ChatResponseUpdate(
                role="assistant",
                contents=[Content.from_text("fixture-pong confirmed")],
            )

        if stream:
            return self._stream_response(update)

        async def response() -> ChatResponse[None]:
            return ChatResponse.from_updates([update])

        return response()

    @staticmethod
    def _stream_response(
        update: ChatResponseUpdate,
    ) -> ResponseStream[ChatResponseUpdate, ChatResponse[None]]:
        async def updates() -> AsyncIterable[ChatResponseUpdate]:
            yield update

        return ResponseStream(updates(), finalizer=ChatResponse.from_updates)
