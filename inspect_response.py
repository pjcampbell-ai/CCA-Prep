import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,   # Deliberately low, so we can trigger max_tokens
    messages=[
        {"role": "user", "content": "Write a 500-word essay on the history of tea."}
    ]
)

# The actual reply text
print("Reply text:")
print(response.content[0].text)

print("\n" + "="*40 + "\n")

# The interesting bits
print(f"Stop reason: {response.stop_reason}")
print(f"Model used: {response.model}")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total tokens: {response.usage.input_tokens + response.usage.output_tokens}")

# Rough cost estimate for Sonnet 4.5 (approximate — check current pricing)
input_cost = response.usage.input_tokens * 3 / 1_000_000    # $3 per million input tokens
output_cost = response.usage.output_tokens * 15 / 1_000_000  # $15 per million output tokens
print(f"Estimated cost: ${input_cost + output_cost:.6f}")