# Start here: learn before coding

Stage 00 is a guided orientation. No prior agent, Azure or framework knowledge is assumed.

Copilot should teach: a model proposes actions; MAF runs the conversation/tool loop; tools call application services; services validate facts and permissions; the human approves exact content. Walk through “Prepare a rental listing” with property lookup, rental evidence, a draft and review.

Explain the difference between Microsoft Agent Framework (the Python orchestration library), Azure OpenAI (the hosted model), and Foundry Agent Service (a managed agent service compared in Stage 18).

Use a simple diagram and plain definitions before introducing terminology. Explain scripted tests as the real MAF machinery receiving predetermined model responses. Ask one optional question only after the example. If the learner does not know, teach it again with a smaller example. Recommend documented defaults; never quiz the learner about implementation decisions that the specification already makes.

[Stage 00 prompt](../../prompts/00-start.md) · [Checkpoint](../checkpoints/00.md) · [MAF contract](../../docs/08-microsoft-agent-framework.md)
