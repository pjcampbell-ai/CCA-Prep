import anthropic

client = anthropic.Anthropic()

# ============================================================
# 1. DEFINE MULTIPLE TOOLS
# Claude sees all of them and picks whichever fits (or none)
# ============================================================
tools = [
    {
        "name": "calculator",
        "description": "Performs arithmetic on a math expression.",
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
    },
    {
        "name": "word_counter",
        "description": "Counts the number of words in a given text string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text whose words should be counted"
                }
            },
            "required": ["text"]
        }
    }
]
# ============================================================
# 2. TWO ACTUAL FUNCTIONS
# ============================================================
def calculator(expression):
    return str(eval(expression))

def word_counter(text):
    return str(len(text.split()))

# ============================================================
# 3. DISPATCHER
# Central place that maps Claude's tool_name to the real Python function.
# This pattern scales — as tools grow, only this dict changes.
# ============================================================
def run_tool(name, tool_input):
    if name == "calculator":
        return calculator(tool_input["expression"])
    elif name == "word_counter":
        return word_counter(tool_input["text"])
    else:
        return f"Unknown tool: {name}"

# ============================================================
# 4. TRY IT WITH DIFFERENT QUESTIONS
# Change the question below to see Claude pick different tools
# ============================================================
user_question = "What is 234 * 456"

messages = [
    {"role": "user", "content": user_question}
]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print("=" * 50)
print("FIRST API CALL")
print("=" * 50)
print(f"stop_reason: {response.stop_reason}")
print(f"content: {response.content}")
print()

# ============================================================
# 5. HANDLE THE TOOL CALL (same shape as yesterday)
# ============================================================
if response.stop_reason == "tool_use":
    tool_use_block = None
    for block in response.content:
        if block.type == "tool_use":
            tool_use_block = block
            break

    tool_name = tool_use_block.name
    tool_input = tool_use_block.input
    tool_use_id = tool_use_block.id

    print(f"Claude chose to call: {tool_name}")
    print(f"With inputs: {tool_input}")

    # Use the dispatcher instead of a hardcoded call
    result = run_tool(tool_name, tool_input)
    print(f"Tool returned: {result}")
    print()

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

    final_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    print("=" * 50)
    print("FINAL RESPONSE")
    print("=" * 50)
    print(f"stop_reason: {final_response.stop_reason}")
    print(f"text: {final_response.content[0].text}")
else:
    print("Claude answered directly, no tool needed.")
    print(f"Answer: {response.content[0].text}")