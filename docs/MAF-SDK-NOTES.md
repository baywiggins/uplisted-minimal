# MAF SDK notes

Stage 01 resolved `agent-framework-core==1.25.0` and
`agent-framework-openai==1.18.1` in `uv.lock`. The package index did not offer
the 1.25 OpenAI provider release described by the current official documentation,
so the live-provider integration must be revalidated at Stage 13 before use.

The offline smoke uses the installed public framework APIs:

- `Agent(client=..., tools=[...])` runs the agent/tool protocol.
- `ScriptedChatClient` composes `FunctionInvocationLayer` over
  `BaseChatClient`; the former owns the function-call loop.
- `BaseChatClient._inner_get_response(*, messages, stream, options, **kwargs)`
  is the installed custom-client extension point.
- `Content.from_function_call(call_id, name, arguments=...)` represents the
  scripted tool proposal. MAF supplies the function result before the second
  deterministic model turn.
- `function_invocation_configuration["allow_concurrent_invocation"] = False`
  requests serial function execution for the smoke.

The Stage 01 client is not a product provider and registers only `fixture_ping`.
The seven product tools, proposal interception, middleware policy, and live Azure
client belong to later stages.
