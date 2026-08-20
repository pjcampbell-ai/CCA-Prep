import anthropic

client = anthropic.Anthropic()

# ============================================================
# 1. DEFINE THE TOOL
# We describe the tool to Claude: name, what it does, what inputs it takes.
# Claude never runs our code — it just decides when to ASK us to run it.
# ============================================================
tools = [
    {
        "name": "calculator",
        "description": "Performs arithmetic. Give it a math expression as a string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression like '2 + 2' or '145 * 892'"
                }
            },
            "required": ["expression"]
        }
    }
]

# ============================================================
# 2. THE ACTUAL PYTHON FUNCTION
# This is what runs when Claude asks to use the calculator.
# eval() is dangerous in real code but fine for this learning exercise.
# ============================================================
def calculator(expression):
    return str(eval(expression))

# ============================================================
# 3. ASK CLAUDE SOMETHING THAT NEEDS THE TOOL
# ============================================================
messages = [
{"role": "user", "content": "What colour is the sky on a clear day?"}   ]

# ============================================================
# 4. FIRST API CALL
# Claude sees the question AND the available tools, and decides what to do.
# ============================================================
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print("=" * 50)
print("FIRST API CALL — Claude's response")
print("=" * 50)
print(f"stop_reason: {response.stop_reason}")
print(f"content: {response.content}")
print()

# ============================================================
# 5. HANDLE THE TOOL CALL
# If Claude wants a tool, stop_reason will be 'tool_use'.
# ============================================================
if response.stop_reason == "tool_use":
    # Find the tool_use block in the response
    tool_use_block = None
    for block in response.content:
        if block.type == "tool_use":
            tool_use_block = block
            break

    # What does Claude want to run?
    tool_name = tool_use_block.name
    tool_input = tool_use_block.input
    tool_use_id = tool_use_block.id  # A unique ID we need to send back

    print(f"Claude wants to call: {tool_name}")
    print(f"With inputs: {tool_input}")

    # Actually run the tool
    if tool_name == "calculator":
        result = calculator(tool_input["expression"])
        print(f"Tool returned: {result}")
        print()

    # ============================================================
    # 6. BUILD THE FOLLOW-UP MESSAGE
    # We append Claude's tool_use response, then a tool_result message with the answer.
    # ============================================================
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": result
            }
        ]
    })

    # ============================================================
    # 7. SECOND API CALL — Claude uses the tool result to answer
    # ============================================================
    final_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    print("=" * 50)
    print("SECOND API CALL — Claude's final answer")
    print("=" * 50)
    print(f"stop_reason: {final_response.stop_reason}")
    print(f"text: {final_response.content[0].text}")