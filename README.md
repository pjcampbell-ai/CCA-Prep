# CCA-Prep
**Week 1 .py Explanations**
**Hello.py** -  Uses the Anthropic Library to send and receive a single response, showing off the ability of API Interaction
**Conversation.py** - user and assistant converse over multiple lines, text is remembered and it will die when script closes 
**System-prompt.py **- character or persona is created to respond in a certain way or manner, it is in a separate parameter, it will persist for whole conversation
**Streaming.py** response comes back piece by piece as Claude generates it, seems live rather than one block at once)
**Inspect_response.py** response requires check on tokens limit, will give a "Stop Reason: for the likes of {max Tokens} and not continue the text (also End_turn - natural end of text, max_tokens - cut off, tool_use wants to call a tool, usage tracks input/output for tokens)
**Structured_output.py ** the use of json - extracts key info from a messy text (prefiling) - continuing on from what claude has given it. forcing its hand to continue to follow the layout you have given it.
## Session log

### Session — [13/08/2026]

**Completed:**
- Consolidation phase (10-24 Aug) closed cleanly
- All 5 gap concepts from failed check-up now locked or close:
  - Roles (`user` / `assistant`)
  - Stateless memory model
  - Missing assistant-append bug
  - `response.content[0].text` indexing
  - System prompt placement (`system=` parameter, not in messages)
- Week 5 MCP concept intro — 3/3 on concept check
- Third session running with accurate reporting

**Next up:**
- [ ] Read MCP official intro: https://modelcontextprotocol.io/introduction
- [ ] Report back with one thing reinforced + one thing new/unclear
- [ ] Hands-on MCP next session: install filesystem MCP server, connect to Claude Desktop
