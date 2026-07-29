# CCA-Prep
**Week 1 .py Explanations**
**Hello.py** -  Uses the Anthropic Library to send and receive a single response, showing off the ability of API Interaction
**Conversation.py** - user and assistant converse over multiple lines, text is remembered and it will die when script closes 
**System-prompt.py **- character or persona is created to respond in a certain way or manner, it is in a separate parameter, it will persist for whole conversation
**Streaming.py** response comes back piece by piece as Claude generates it, seems live rather than one block at once)
**Inspect_response.py** response requires check on tokens limit, will give a "Stop Reason: for the likes of {max Tokens} and not continue the text (also End_turn - natural end of text, max_tokens - cut off, tool_use wants to call a tool, usage tracks input/output for tokens)
**Structured_output.py ** the use of json - extracts key info from a messy text (prefiling) - continuing on from what claude has given it. forcing its hand to continue to follow the layout you have given it.
