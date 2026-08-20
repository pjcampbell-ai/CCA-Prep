# CCA-F Practice Question Bank

*Compiled from PJ's coaching sessions, July–September 2026*

---

## How to use this document

- Questions are grouped by concept area (broadly aligned with CCA-F exam domains)
- **Do not scroll to the answer key until you've written your answer**
- Score yourself honestly — this is the same accurate-reporting muscle we've been building
- Some questions have appeared multiple times in slightly different framings — I've kept one clean version of each
- Where I've paraphrased rather than reproduced verbatim, questions are marked with (~)
- A few questions from earliest sessions couldn't be reconstructed with full confidence — those are omitted rather than fabricated

## Suggested study approach

1. **Cold-run mode:** answer all questions in a section without looking at answers, then check the whole section at once
2. **Deep-dive mode:** for any wrong answer, don't just note the right one — write out *why* each wrong option is wrong. That's what the exam actually tests.
3. **Repeat schedule:** re-run the full bank every 2 weeks. Concepts you get right two runs in a row can drop out. Concepts you keep missing need a different kind of practice than just re-testing.

---

# Section 1: API Basics — Messages, Roles, System Prompts

## Q1

A developer's API call fails with error: *"messages.1: role must be 'user' or 'assistant'"*. Their code:

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "system", "content": "Be brief"},
    {"role": "user", "content": "Explain photosynthesis"}
]
```

What's the fix?

- **a)** Reorder so user and assistant strictly alternate
- **b)** Remove the system message from `messages` and pass it via the `system=` parameter on `client.messages.create()`
- **c)** Change `"system"` to lowercase throughout
- **d)** Add an assistant message before the system one

## Q2

You're building a customer support bot. It should always speak formally, refuse off-topic queries, and escalate refund requests. Robust design says:

- **a)** Include these rules in every user message
- **b)** Set them once via `system=` parameter on `client.messages.create()`
- **c)** Prepend as an `{"role": "system", ...}` in the messages list
- **d)** Set them via `assistant=` parameter

## Q3

An engineer wants all interactions with an internal legal-triage bot to (a) speak formally, (b) refuse anything outside legal topics, and (c) survive attempted jailbreaks in later user messages. Where should these instructions be placed?

- **a)** In the first `user` message so the user can see the constraints
- **b)** In the `system` parameter, because it persists for the conversation and is harder to override
- **c)** Repeated as a preamble in every `user` message
- **d)** In an initial `assistant` message so Claude sees them as its own

## Q4

A developer's code uses these roles: `"user"`, `"agent"`, and `"system"`. The API returns a 400 error. Which change fixes it?

- **a)** Rename `"system"` to `"instructions"` and keep `"agent"`
- **b)** Rename `"agent"` to `"assistant"` and move `"system"` content into the separate `system` parameter
- **c)** Rename `"user"` to `"human"` and `"agent"` to `"bot"`
- **d)** Add a `"tool"` role between `"user"` and `"agent"`

## Q5

A developer adds a system prompt by doing this:

```python
messages.append({"role": "system", "content": "You are a legal assistant."})
```

Then calls `client.messages.create(model=..., messages=messages)`. What happens?

- **a)** The API accepts it and Claude follows the persona
- **b)** The API accepts it but Claude ignores the system message
- **c)** The API returns an error because `system` is not a valid role
- **d)** The system prompt works but is much weaker than using the `system=` parameter

---

# Section 2: Prompt Engineering — Streaming, Structured Output, Prefilling

## Q6

You are designing a nightly batch job that summarises 20,000 documents. Each summary is stored to a database for later retrieval. Should you use streaming for the API calls?

- **a)** Yes — streaming reduces total token cost for large batches
- **b)** Yes — streaming avoids hitting rate limits
- **c)** Yes — streaming produces higher-quality responses in batch settings
- **d)** No — streaming has no benefit when no human is watching in real time

## Q7

Claude sometimes returns JSON wrapped in markdown fences (` ```json `), breaking your parser. You've already added "return only valid JSON" to the system prompt but the issue persists intermittently. What's the most reliable additional technique?

- **a)** Retry the request until valid JSON is returned
- **b)** Set `temperature` to 0
- **c)** Prefill the assistant message with `"{"` to force JSON continuation
- **d)** Switch to structured output mode with a JSON schema in system

---

# Section 3: Response Handling — content blocks, stop_reason

## Q8

A developer's agent code has:

```python
if response.stop_reason == "tool_result":
    handle_tool(response.content[0])
```

Why is it broken?

- **a)** `stop_reason` attribute doesn't exist on response objects
- **b)** `"tool_result"` is not a valid `stop_reason` — the correct value when Claude wants a tool is `"tool_use"`
- **c)** `response.content[0]` should be `response.content.first`
- **d)** The comparison needs `.value` on `stop_reason`

## Q9

A tool-enabled call returns `response.content` as:

```python
[TextBlock(text="Let me check..."), ToolUseBlock(name="get_weather", input={...}, id="abc")]
```

Your code does `tool_block = response.content[0]`. What happens?

- **a)** It correctly grabs the ToolUseBlock
- **b)** It grabs the TextBlock, then crashes when you try to access `.name` or `.input`
- **c)** The API rejects the response for having two content blocks
- **d)** Content blocks are automatically re-ordered so `tool_use` is first

---

# Section 4: Context Management — Stateless Memory, Cost Scaling

## Q11

A user chats with a Claude-powered bot for 20 turns. The developer restarts the Python process. On turn 21, the user asks: *"What was that number I asked you to remember?"* What happens?

- **a)** Claude retrieves it from server-side session state
- **b)** Claude has no memory — the `messages` list was in-memory and is now empty
- **c)** Anthropic caches conversation history for 24 hours by API key
- **d)** Claude asks the user to log in to restore session

## Q12

A user has been chatting with a Claude-powered bot for 20 turns. The developer decides to restart the Python process. On turn 21, the user asks: *"What did I say earlier about my project deadline?"* What happens?

- **a)** Claude retrieves the earlier context from Anthropic's server-side session cache
- **b)** Claude admits it has no record of the earlier conversation
- **c)** Claude asks the user to log back in
- **d)** The API returns an error because the session token is stale

## Q13

Which statement about conversation memory in the Anthropic API is accurate?

- **a)** Anthropic maintains conversation state per API key for 30 minutes
- **b)** The API is stateless; the developer must send the full transcript with every request
- **c)** Only the last 10 exchanges are cached server-side for continuity
- **d)** The `assistant` role stores state; the `user` role does not

## Q14

Agent A completes tasks in 5 turns on average. Agent B does the same tasks but takes 30 turns (more careful reasoning). Same model, same tools, same per-turn message lengths. Approximate cost ratio B/A per session?

- **a)** ~6x (turns proportional to cost)
- **b)** ~30x or more (input tokens accumulate — earlier turns re-sent in later ones)
- **c)** Same cost (Anthropic caches conversation history)
- **d)** ~2-3x (efficiency gains scale sublinearly)

## Q15

A support chatbot's cost per conversation is £0.30 at 15 turns. Assuming user and assistant message lengths remain similar throughout, what would you roughly expect a 30-turn session to cost?

- **a)** £0.30 — cost is flat because conversation content is cached
- **b)** About £0.60 — twice as many turns, twice the cost
- **c)** Significantly more than £0.60 — later turns send more history than earlier turns
- **d)** About £0.45 — the model is more efficient with longer context

## Q16

A developer's chatbot works fine in isolated tests but "forgets things" in longer conversations. Their code:

```python
messages = []
while True:
    user_input = input()
    messages.append({"role": "user", "content": user_input})
    response = client.messages.create(...)
    print(response.content[0].text)
```

What's the bug?

- **a)** Missing a system prompt
- **b)** Claude's response is never appended to `messages` — Claude only sees user turns in history
- **c)** The loop should use streaming
- **d)** `max_tokens` is undefined

## Q17

A developer wants Claude to have full conversation memory. Which of these code patterns achieves that?

**Pattern A:**
```python
messages.append({"role": "user", "content": user_input})
response = client.messages.create(messages=messages)
# nothing else
```

**Pattern B:**
```python
messages.append({"role": "user", "content": user_input})
response = client.messages.create(messages=messages)
messages.append({"role": "assistant", "content": response.content[0].text})
```

**Pattern C:**
```python
response = client.messages.create(messages=[{"role": "user", "content": user_input}])
```

- **a)** Pattern A
- **b)** Pattern B
- **c)** Pattern C
- **d)** All three achieve full memory

## Q18

If Claude correctly appends both user and assistant messages every turn, how many entries are in the `messages` list at the end of a 10-turn conversation?

- **a)** 10
- **b)** 20
- **c)** 11 (10 user + 1 assistant summary)
- **d)** Depends on the `max_tokens` setting

## Q19

You accidentally delete the line that appends the assistant reply back to `messages`. The script still runs without errors. What behaviour changes?

- **a)** Nothing — Claude tracks its own responses server-side
- **b)** Claude will loop indefinitely because it never sees a stop signal
- **c)** Claude will respond as if every turn were the first — no memory of prior replies, but still responds to each user message
- **d)** The next API call will crash with a role-alternation error

---

# Section 5: Tool Use — The Loop, tool_use Blocks, tool_result

## Q20

You've built a tool-enabled agent. A user asks a question Claude can answer using an available tool. Why does the interaction require two API calls rather than one?

- **a)** The first call authenticates the tool; the second executes it
- **b)** Claude checks its answer twice for accuracy
- **c)** The first returns Claude's request to use a tool; after your code runs the tool, the second sends the result back for Claude to compose the final answer
- **d)** The first is a dry-run to estimate cost; the second is the real call

## Q21

Claude decides to use a tool. What does the response contain?

- **a)** The executed result of the tool
- **b)** A `tool_use` block describing which tool to call and with what inputs, along with a unique ID
- **c)** A text answer that includes the tool name in brackets
- **d)** A stop_reason of `tool_result`

## Q22

You've defined a `get_stock_price` tool. A user asks: *"What's Apple's stock price?"* You inspect `response.content` from the first API call. Which best describes what's inside?

- **a)** A string: `"[TOOL: get_stock_price(ticker='AAPL')]"`
- **b)** A list containing a `ToolUseBlock` object with `name='get_stock_price'`, `input={'ticker': 'AAPL'}`, and a unique `id`
- **c)** A string with Apple's stock price already looked up by Claude
- **d)** An empty list — the tool was executed silently

## Q23

Your Python code has run a tool and now needs to send the result back to Claude. What is the correct `role` for the message containing the `tool_result` block?

- **a)** `assistant`
- **b)** `tool`
- **c)** `user`
- **d)** `system`

## Q24

Claude's response contains three `tool_use` blocks (parallel tool calls). How should you structure the response back to the API?

- **a)** Three separate messages, each with one `tool_result` and its matching id
- **b)** One `user` message whose content is a list of three `tool_result` blocks with matching ids
- **c)** One `assistant` message containing all three results concatenated as text
- **d)** Send only the first result; Claude will re-request the others

## Q25

Claude's response contains two tool_use blocks with IDs `"toolu_abc"` and `"toolu_xyz"`. What's true about your response back to the API?

- **a)** Send one `tool_result` message, then wait for Claude to ask for the next
- **b)** Send both `tool_result` blocks in a single `user` message, each with matching `tool_use_id`
- **c)** `tool_use_id` is optional when there's only one recent tool call
- **d)** Order and IDs don't matter — the API pairs them automatically

## Q26

You have five tools available: `get_weather`, `calculator`, `stock_lookup`, `translate_text`, and `word_count`. A user asks: *"How many words are in the French translation of 'Hello world'?"* How does Claude decide which tool(s) to use, and in what order?

- **a)** Claude reads the tool descriptions, reasons about the request, and may call multiple tools sequentially or in parallel as needed
- **b)** Claude runs all five tools and returns the best result
- **c)** Claude uses the tool with the alphabetically first name that matches keywords in the question
- **d)** Claude asks the user which tool to use

---

# Section 6: Tool Use — Error Handling & Data Types

## Q28

A developer's tool function has no try/except wrapping. During a live user session, the tool raises an unhandled `requests.exceptions.Timeout`. What does the user see?

- **a)** Claude apologises and offers alternative sources of information
- **b)** Claude retries the tool automatically
- **c)** Claude answers from its own training data instead
- **d)** A Python traceback; the script terminates before the second API call is made

## Q29

Your `get_stock_price` tool doesn't wrap its API call in try/except. During a live user session, the stock API returns a 503 and `requests.raise_for_status()` throws. What does the user see in the chat interface?

- **a)** Claude saying: "The stock service is currently unavailable, please try again later"
- **b)** A blank screen while Claude retries in the background
- **c)** Nothing visible; the script terminates with a Python traceback in the developer's terminal, no message ever reaches the chat interface
- **d)** Claude answering with its best guess of Apple's stock price from training data

## Q30

Your tool returns the string `"Error: database connection timed out after 30s"` when the DB is unreachable. What is Claude most likely to do with this in the final response?

- **a)** Include the technical error verbatim in the user-facing response
- **b)** Ignore the error and fabricate an answer from training data
- **c)** Read the error, understand it as a failure, and translate it into user-appropriate language (apology, alternatives)
- **d)** Retry the tool up to three times before giving up

## Q31

A tool function returns `len(some_string)` (an integer). The developer puts it directly in the tool_result content field:

```python
{"type": "tool_result", "tool_use_id": id, "content": len_result}
```

What happens?

- **a)** It works fine — the API accepts any content type
- **b)** The API returns a 400 error — tool_result content must be a string
- **c)** Claude interprets the integer as a token count
- **d)** The response is silently truncated

## Q32

You're designing an agent for graceful degradation when external tools fail. Which design pattern is essential?

- **a)** Adding a "try harder" instruction to the system prompt
- **b)** Wrapping tool functions in try/except that convert exceptions into informative error strings returned to Claude
- **c)** Using streaming so partial responses are shown even on failure
- **d)** Setting `max_tokens` higher so Claude has room to explain errors

---

# Section 7: MCP — Concepts and Ecosystem

## Q33

Which best describes an **MCP client**?

- **a)** A program that provides tools (like GitHub or Postgres access) to be consumed by AI apps
- **b)** An AI application (Claude Desktop, Cursor, Claude Code) that consumes tools from MCP servers
- **c)** The underlying JSON-RPC protocol that transports MCP messages
- **d)** A remote server hosted by Anthropic that stores connector configurations

## Q34 (~)

Which best describes an **MCP server**?

- **a)** An AI application that consumes tools
- **b)** A program that provides tools, resources, or prompts to be consumed by AI apps
- **c)** A configuration file listing available connectors
- **d)** The wire format used to transport messages

## Q35

An engineer says: *"I can just write tools inline in my Python script like weeks 3-4. Why do I need MCP?"* What's the strongest argument for MCP?

- **a)** MCP tools are faster than inline tools
- **b)** MCP tools bypass the tool_use loop, reducing API calls
- **c)** MCP separates tool definitions from AI applications, so one tool implementation (e.g., a GitHub server) can be reused across many AI apps without code duplication
- **d)** MCP tools work without Claude having to reason about them

## Q36

A user asks Claude: *"What's in the file at `C:\Users\me\project\notes.md` right now?"* Claude can only answer accurately if:

- **a)** The file was part of Claude's training data
- **b)** Claude has access to a filesystem MCP server that can read the file at runtime
- **c)** The user copy-pastes the file contents into the message
- **d)** Both B and C would work

## Q37

You're browsing a public directory of MCP servers and find one that says it "makes any AI 10x better at coding" from an unknown author. What's the appropriate response?

- **a)** Install it — MCP servers run in sandboxes, so there's no risk
- **b)** Install it and just review the code afterwards if it's slow
- **c)** Treat it like installing a random browser extension or unverified app — the risk is code execution on your machine and potential data exposure; stick to reputable sources
- **d)** Install it only if it has more than 100 GitHub stars

## Q38 (~)

Why does the Linux Foundation governance shift for MCP matter for someone learning it today?

- **a)** It means MCP servers now require paid licensing
- **b)** MCP is now an industry standard maintained across multiple vendors (Anthropic, OpenAI, Google, Microsoft, AWS), so skills transfer across platforms rather than being vendor-locked
- **c)** MCP tools are now hosted centrally on Linux Foundation servers
- **d)** It affects which MCP servers you're legally allowed to use

## Q39 (~)

Between stdio and HTTP transports for MCP servers, when would you use each?

- **a)** stdio for personal machine / local tools; HTTP for remote / shared servers
- **b)** stdio only for testing; HTTP always in production
- **c)** HTTP for personal machine; stdio for enterprise
- **d)** They're interchangeable — pick whichever you prefer

---

# Section 8: MCP — Building Servers

## Q40 (~)

You've written a Python function and put `@mcp.tool()` above it in a FastMCP server. What does that decorator do?

- **a)** It runs the function immediately when the server starts
- **b)** It exposes the function as an MCP tool, auto-generating the input schema from the function's type hints and using the docstring as the tool description
- **c)** It converts the function to run asynchronously
- **d)** It caches the function's return value

## Q41 (~)

You wrote a docstring on your MCP tool function: *"Get the current English Premier League table..."*. What role does that docstring play when a client like Claude Desktop uses this server?

- **a)** Just for other developers reading your code — Claude doesn't see it
- **b)** It becomes the tool's description that Claude reads to decide when to use the tool
- **c)** It's shown to the end user as help text
- **d)** It's logged for debugging purposes

## Q42 (~)

Your MCP server runs and works in the MCP Inspector via `mcp dev`. What needs to happen for Claude Desktop to be able to use this server in a real chat?

- **a)** Nothing — Claude Desktop auto-discovers running MCP servers
- **b)** You need to add the server to Claude Desktop's config file (or install it as an extension) and restart Claude Desktop
- **c)** You need to publish the server to a public registry first
- **d)** You need to get Anthropic to approve the server

---

# Section 9: Extra Concept Consolidation

## Q45 (~)

In one sentence, what does `str()` do in the context of preparing a value to return from a tool function?

- **a)** Removes all non-alphabetic characters
- **b)** Converts any Python value (int, float, dict, list) into its string representation, which is the format `tool_result` content requires
- **c)** Truncates a value to 100 characters
- **d)** Adds quotes around a string

## Q46 (~)

Why is fixing a data-type conversion inside the tool function itself (rather than at the send-back point) generally safer?

- **a)** Functions are faster than external conversions
- **b)** If the function is called from multiple places, one fix inside the function protects all call sites; if you fix it externally, you have to remember to do it every time
- **c)** External conversions cause the API to reject the request
- **d)** Only functions can convert types in Python

---

# Section 3 (additional)

## Q10

You want Claude to explain its reasoning to the user *before* calling a tool — something like *"Let me check the weather for you..."* — and then still call the tool. What actually happens in practice?

- **a)** Impossible — Claude can only produce a `tool_use` block in a tool-use response, no text
- **b)** Claude often produces both a TextBlock (explaining intent) AND a ToolUseBlock in the same response — both appear in `response.content`
- **c)** You have to make two separate API calls: one for the text, one for the tool call
- **d)** The `tool_use` block must always be the first content block, before any text

---

# Section 5 (additional)

## Q27

In a multi-turn tool-using agent, Claude calls a tool, gets a result, then decides based on that result that it needs to call ANOTHER tool. What must your code do for this to work?

- **a)** Claude can only call one tool per session — you'd need to restart
- **b)** You must batch all tool calls upfront — Claude cannot make sequential decisions
- **c)** The agent loop must continue calling the API until `stop_reason` is `end_turn`. Each new `tool_use` response triggers another tool run + reply cycle
- **d)** Claude decides internally and returns all tool results in one final response

---

# Section 8 (additional)

## Q43

You've built an MCP server that wraps a slow external API (30-second response time). A user asks Claude a question that would call this tool. What's a legitimate concern?

- **a)** Claude will time out and lose the conversation
- **b)** The tool call will exceed reasonable user-facing latency — consider async patterns, caching, or progress reporting via streaming
- **c)** MCP servers can't call external APIs at all
- **d)** The tool will auto-fail after 10 seconds

## Q44

You want to write an MCP server that exposes a *read-only* view of your team's PostgreSQL database. What's the safest design?

- **a)** Give the MCP server a superuser database credential so any query works
- **b)** Use a dedicated read-only database role with SELECT-only permissions, so the AI can query but never modify data
- **c)** Add "please don't modify data" to the system prompt and hope for the best
- **d)** Trust the AI to be careful with UPDATE and DELETE statements

---

# Section 10: Prompt Caching

## Q47

Prompt caching in the Anthropic API — what's the primary benefit?

- **a)** It makes model responses faster to generate
- **b)** It reduces cost and latency by caching parts of the input prompt server-side, so they don't need to be re-processed on subsequent calls
- **c)** It stores Claude's responses server-side for faster retrieval next time
- **d)** It lets Claude remember previous conversations without you re-sending them

## Q48

Your agent sends a 20,000-token system prompt (large tool definitions + reference docs) plus a small user query every turn. You enable prompt caching on the large prefix. What effect is likely?

- **a)** The user query gets faster responses because prompts are shorter
- **b)** The 20,000-token prefix is cached after first use; subsequent calls only re-process the small user query, dramatically lowering cost per turn
- **c)** The model produces higher-quality answers
- **d)** The context window effectively doubles in size

---

# Section 11: Claude Code

## Q49

What is Claude Code?

- **a)** A specific model (like Sonnet or Haiku) optimised for code generation
- **b)** A command-line / IDE agent tool from Anthropic that lets developers use Claude as an agent for real coding tasks (edit files, run commands, use MCP tools) in their own terminal
- **c)** A subscription tier on anthropic.com
- **d)** A dataset used to train Claude on code

## Q50

Claude Code needs to work with your codebase. How does it access your files and tools?

- **a)** It uploads your entire codebase to Anthropic servers for analysis
- **b)** It runs locally on your machine — executes commands you approve, reads files you point it at, and sends only relevant context to the Claude API
- **c)** You must manually paste code snippets one at a time into a chat window
- **d)** It uses a proprietary compiler to analyse code offline

## Q51

How do Claude Code and MCP relate?

- **a)** Claude Code is an MCP server that other AI apps can call
- **b)** Claude Code is an MCP client — you can configure MCP servers (GitHub, filesystem, Postgres, etc.) in its config and Claude Code will use them as tools
- **c)** Claude Code replaces MCP entirely — you don't need MCP if you have Claude Code
- **d)** MCP only works with Claude Desktop, not Claude Code

## Q52

You're using Claude Code to refactor a project. Claude proposes running `rm -rf ./build`. What happens by default?

- **a)** The command runs immediately — Claude Code trusts its own suggestions
- **b)** Claude Code shows you the command and waits for your explicit approval before executing it
- **c)** Claude Code runs it but logs it for later review
- **d)** Claude Code refuses to run any file-modifying commands at all

---

# ANSWER KEY

*Fold this section over / cover it up when self-testing.*

## Section 1

- **Q1: b** — System is a parameter, not a role. Only `user` and `assistant` are valid role values.
- **Q2: b** — `system=` parameter persists for the conversation and is more resistant to override attempts than putting rules in user messages.
- **Q3: b** — Same as Q2 — system parameter is architecturally distinct and weighted differently by the model. More jailbreak-resistant.
- **Q4: b** — Two fixes needed: `"agent"` isn't valid (should be `"assistant"`); `"system"` isn't a role (goes in the separate parameter).
- **Q5: c** — API rejects with 400 error. Only `user` and `assistant` roles exist.

## Section 2

- **Q6: d** — Streaming's only benefit is perceived latency for a human. No human = no benefit. Same total time, tokens, cost.
- **Q7: c** — Prefilling with `{` forces Claude's response to continue from that character. Cannot add "Here's the JSON:" preamble because the response literally starts with `{`.

## Section 3

- **Q8: b** — `"tool_result"` is never a valid `stop_reason` value. Real value is `"tool_use"` when Claude wants a tool. Without this fix, the if-block never runs.
- **Q9: b** — `response.content` is a list. Position 0 is whatever happens to be first — often a TextBlock, not the ToolUseBlock. Filter by `.type` instead.

## Section 4

- **Q11: b** — API is stateless. Restart = fresh `messages` list = no memory.
- **Q12: b** — Same as Q10 — no server-side session cache, no "log in to restore."
- **Q13: b** — Stateless API. Full transcript must be re-sent every call.
- **Q14: b** — Roughly quadratic scaling. 5 turns = sum of 1+2+3+4+5 = 15 turn-worths of input. 30 turns = 30*31/2 = 465. Ratio ≈ 31x, not 6x.
- **Q15: c** — Same principle as Q13 — not linear because later turns send more history.
- **Q16: b** — Missing assistant append. Claude sees only user side of conversation on each new call.
- **Q17: b** — Pattern B correctly appends both user AND assistant to `messages`.
- **Q18: b** — 10 user + 10 assistant = 20 entries.
- **Q19: c** — Claude has no memory of its own prior responses, so each turn feels like the first. But it doesn't crash — the API accepts user-only history.

## Section 5

- **Q20: c** — Claude cannot execute code. First call = tool request. Your code runs the tool. Second call = result back to Claude for the final natural-language answer.
- **Q21: b** — Response contains a `tool_use` block with `name`, `input`, and `id`. Claude never runs the tool — it requests one.
- **Q22: b** — Same as Q20 — `ToolUseBlock` with name, input dict, and id.
- **Q23: c** — Role is `user`. Roles are `user` and `assistant` only; anything sent TO Claude is `user`, regardless of content type.
- **Q24: b** — All tool_results in one user message, as a list of blocks, each with its matching `tool_use_id`.
- **Q25: b** — Same as Q23 — one message, list of results, IDs matter.
- **Q26: a** — Claude reads tool descriptions, reasons about the request, plans multi-step tool use itself. This is the beginning of agent behaviour.

## Section 6

- **Q28: d** — Without try/except, Python raises the exception and the script dies. The second API call never happens, so Claude never gets a chance to respond.
- **Q29: c** — Same as Q26. No API call = no Claude response. The user sees whatever the client displays for a hung tool call; the developer sees the traceback.
- **Q30: c** — Claude reads `tool_result` content and reasons about it. A human-readable error string is interpreted as failure and translated into user-appropriate language.
- **Q31: b** — `tool_result` content must be a string. Integer content triggers a 400 error.
- **Q32: b** — try/except that converts exceptions into strings is the essential pattern. Without it, crashes kill the script before Claude can respond.

## Section 7

- **Q33: b** — Client = the AI app that consumes tools (Claude Desktop, Cursor, etc.).
- **Q34: b** — Server = the program that provides tools/resources/prompts. Kitchen (serves) vs diner (consumes).
- **Q35: c** — MCP's real value is reusability across AI apps and separation of tool implementation from consumption.
- **Q36: d** — Both B and C work. Training didn't include your personal files. Either paste the content or have runtime file access via MCP.
- **Q37: c** — MCP servers execute code on your machine with your permissions. Treat unknown sources as untrusted.
- **Q38: b** — Multi-vendor governance means MCP is an industry standard, not an Anthropic thing. Skills transfer across platforms.
- **Q39: a** — stdio = local (server is a subprocess of the client). HTTP = remote/hosted.

## Section 8

- **Q40: b** — `@mcp.tool()` exposes the function as an MCP tool. FastMCP inspects the signature (type hints) to generate the input schema and uses the docstring as the tool description.
- **Q41: b** — The docstring is what Claude reads to decide when to invoke the tool. Clear docstrings = better tool selection.
- **Q42: b** — Register the server in Claude Desktop's config (`claude_desktop_config.json`) or install as an extension, then restart Claude Desktop.

## Section 9

- **Q45: b** — `str()` converts values to their string representation. Needed because `tool_result` content must be a string.
- **Q46: b** — Fix in the function = one fix protects all call sites. Fix at send-back = must remember every time, easy to miss.

## Section 3 (additional)

- **Q10: b** — `response.content` is a list of blocks. Claude regularly produces TextBlock(s) followed by ToolUseBlock(s) in one response. Iterating and handling both types is essential.

## Section 5 (additional)

- **Q27: c** — Agentic behaviour = a loop. While Claude returns `tool_use`, run the tool and send the result back. Only stop when `stop_reason == 'end_turn'`.

## Section 8 (additional)

- **Q43: b** — MCP servers can call any API, but tool response time = user-perceived latency. Slow tools need caching, async patterns, or progress reporting.
- **Q44: b** — Principle of least privilege. Enforce read-only at the database layer (role permissions), not via prompts or model discretion. Core MCP security pattern.

## Section 10: Prompt Caching

- **Q47: b** — Caching stable INPUT prefixes (system prompts, tool definitions, docs) so they aren't re-processed per call. Cache reads are much cheaper than fresh input. Does NOT give Claude memory.
- **Q48: b** — Cache the expensive prefix once. Subsequent calls charge cheaper cache-read rates for the prefix, full rates only on the small changing user query. Cost savings often 90%+ on long-context agents.

## Section 11: Claude Code

- **Q49: b** — Claude Code is Anthropic's agentic coding tool. Runs locally, has filesystem/shell access, uses MCP servers. NOT a model — a client/agent built on top of Claude.
- **Q50: b** — Runs locally as an agent. Files stay on your machine. Only relevant context sent to the API per call. No wholesale codebase upload — core privacy property.
- **Q51: b** — Claude Code is MCP-compatible. Any MCP server (Filesystem, GitHub, custom) becomes available as tools inside Claude Code. This is how you extend its capabilities.
- **Q52: b** — Human-in-the-loop for destructive commands is core to Claude Code's design. You approve. The agent doesn't unilaterally execute. Critical safety property.

---

# Meta: what this list covers vs what it doesn't

**Covered well:**
- API basics (roles, system prompts, message structure)
- Response handling (content blocks, stop_reason)
- Context management (stateless memory, cost scaling, the append bug)
- Tool use (loop, blocks, IDs, error handling, data types)
- MCP concepts and building basics
- Prompt caching (basics)
- Claude Code (concept + MCP integration)

**Not yet covered in your prep — CCA-F will also test:**
- Deeper agentic architecture patterns (evals, guardrails, structured multi-agent workflows)
- Advanced MCP (resources and prompts as primitives, remote HTTP transport, OAuth)
- Structured output with formal JSON schemas
- Context window management strategies at scale

Those are the gaps to focus new material on.

---

*End of question bank. 52 questions across 11 sections.*
