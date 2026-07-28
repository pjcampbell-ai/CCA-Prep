import anthropic
import json

client = anthropic.Anthropic()

messy_text = """
Sarah Chen, 34, joined the company as VP of Engineering last March. 
She previously worked at Stripe for 6 years and holds a PhD in 
Computer Science from Stanford. Her direct reports include two 
principals and eight senior engineers.
"""

# Stronger prompt: start Claude's reply for it, so it has no choice but JSON
prompt = f"""Extract information from this text as JSON.

Text:
{messy_text}

Return JSON with this exact structure:
{{
  "name": string,
  "age": number,
  "role": string,
  "previous_company": string,
  "education": string,
  "team_size": number
}}

Do not include markdown code fences. Do not include any text before or after the JSON."""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt},
        # Pre-fill Claude's response with the opening brace of JSON
        # This forces Claude to continue as JSON from the start
        {"role": "assistant", "content": "{"}
    ]
)

raw_reply = response.content[0].text

# Because we pre-filled "{", the reply starts with the REST of the JSON
# So we prepend the "{" back on
full_json = "{" + raw_reply

# Defensive: strip any markdown fences just in case
full_json = full_json.replace("```json", "").replace("```", "").strip()

print("Raw response from Claude:")
print(full_json)
print()

# Now parse
data = json.loads(full_json)

print("Parsed data:\n")
print(f"Name: {data['name']}")
print(f"Age: {data['age']}")
print(f"Role: {data['role']}")
print(f"Previous company: {data['previous_company']}")
print(f"Education: {data['education']}")
print(f"Team size: {data['team_size']}")