import anthropic

client = anthropic.Anthropic()

# The conversation history - this is what makes it "multi-turn"
messages = []

print("Chat with Claude (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye.")
        break
    
    # Add your message to the history
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Send the ENTIRE history to Claude every time
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=messages
    )
    
    reply = response.content[0].text
    
    # Add Claude's reply to the history too
    messages.append({
        "role": "assistant",
        "content": reply
    })
    
    print(f"\nClaude: {reply}\n")