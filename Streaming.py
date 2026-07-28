import anthropic

client = anthropic.Anthropic()

print("Ask Claude anything (streaming):\n")

user_input = input("You: ")

print("\nClaude: ", end="", flush=True)

# The 'with client.messages.stream(...)' syntax opens a streaming connection
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": user_input}
    ]
) as stream:
    # Loop through the text pieces as they arrive
    for text_chunk in stream.text_stream:
        # Print each chunk immediately, don't wait for a newline
        print(text_chunk, end="", flush=True)

print("\n")