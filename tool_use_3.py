import anthropic
import requests

client = anthropic.Anthropic()

# ============================================================
# 1. DEFINE THE TOOL
# Notice: description tells Claude WHEN to use it (weather questions),
# not HOW it works. Claude doesn't need internals.
# ============================================================
tools = [
    {
        "name": "get_current_weather",
        "description": "Gets the current weather for a given city. Returns temperature in Celsius and a text description.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. 'London', 'Tokyo', 'Sydney'"
                }
            },
            "required": ["city"]
        }
    }
]

# ============================================================
# 2. THE REAL FUNCTION — calls a live API
# We wrap the whole thing in try/except so a crash returns
# an error string, not an unhandled exception.
# ============================================================
def get_current_weather(city):
    try:
        # First — convert city name to coordinates using Open-Meteo's geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()   # Errors if HTTP status is bad
        geo_data = geo_response.json()

        # Handle: city not found
        if "results" not in geo_data or len(geo_data["results"]) == 0:
            return f"Error: Could not find city '{city}'"

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # Then — get weather for those coordinates
        weather_url = geo_url = f"https://geocoding-api.open-meteo.com/v1/BROKEN?name={city}&count=1"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        temp = weather_data["current"]["temperature_2m"]
        code = weather_data["current"]["weather_code"]

        # A tiny lookup for weather code → description
        # (Real code would use the full table from Open-Meteo docs)
        descriptions = {
            0: "clear sky",
            1: "mainly clear", 2: "partly cloudy", 3: "overcast",
            45: "foggy", 48: "foggy",
            51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
            61: "light rain", 63: "rain", 65: "heavy rain",
            71: "light snow", 73: "snow", 75: "heavy snow",
            95: "thunderstorm"
        }
        desc = descriptions.get(code, f"weather code {code}")

        return f"The temperature in {city} is {temp}°C with {desc}."

    except requests.exceptions.Timeout:
        return f"Error: Weather service timed out for '{city}'"
    except requests.exceptions.RequestException as e:
        return f"Error: Weather service failed: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error: Unexpected response format from weather service"
    except Exception as e:
        return f"Error: Unexpected problem: {str(e)}"

# ============================================================
# 3. DISPATCHER (same pattern as yesterday)
# Notice we now handle 'unknown tool' — Claude sometimes hallucinates tool names.
# ============================================================
def run_tool(name, tool_input):
    if name == "get_current_weather":
        return get_current_weather(tool_input["city"])
    else:
        return f"Error: Unknown tool '{name}'"

# ============================================================
# 4. ASK CLAUDE
# ============================================================
user_question = "What's the weather like in Dublin?"
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

# ============================================================
# 5. HANDLE THE TOOL LOOP
# ============================================================
if response.stop_reason == "tool_use":
    # Collect ALL tool_use blocks (there may be more than one)
    tool_use_blocks = [block for block in response.content if block.type == "tool_use"]
    
    print(f"Claude wants to make {len(tool_use_blocks)} tool call(s)")
    print()
    
    # Run each tool and collect results
    tool_results = []
    for block in tool_use_blocks:
        print(f"  Calling: {block.name}")
        print(f"  Inputs: {block.input}")
        result = run_tool(block.name, block.input)
        print(f"  Returned: {result}")
        print()
        
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result
        })
    
    # Send Claude's response and ALL tool_results back in one message
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": tool_results   # <-- a list containing ALL the tool_result blocks
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
    print("Claude answered directly:")
    print(response.content[0].text)