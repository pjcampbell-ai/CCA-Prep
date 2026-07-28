import anthropic

client = anthropic.Anthropic()

# The system prompt - Claude's persistent instructions
system_prompt = """You are a stern 1970s British headmaster. You speak formally, 
use old-fashioned English, and occasionally quote Latin. You disapprove of modern 
technology and shortcuts. Keep responses to two sentences maximum."""

messages = []

print("Chat with the Headmaster (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye.")
        break
    
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=system_prompt,  # <-- NEW: the system prompt goes here
        messages=messages
    )
    
    reply = response.content[0].text
    
    messages.append({
        "role": "assistant",
        "content": reply
    })
    
    print(f"\nHeadmaster: {reply}\n")