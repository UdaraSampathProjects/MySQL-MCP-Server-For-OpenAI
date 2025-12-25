import os
import json
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()


openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_user_query(user_input: str):
    # Path to your server.py relative to the root
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Fetch tools
            mcp_resp = await session.list_tools()
            tools = [{
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                }
            } for t in mcp_resp.tools]

            messages = [
                {"role": "system", "content": "You are a database assistant."},
                {"role": "user", "content": user_input}
            ]

            response = await openai_client.chat.completions.create(
                model="gpt-4o", messages=messages, tools=tools
            )
            
            response_message = response.choices[0].message
            
            if response_message.tool_calls:
                messages.append(response_message)
                for tool_call in response_message.tool_calls:
                    result = await session.call_tool(
                        tool_call.function.name, 
                        json.loads(tool_call.function.arguments)
                    )
                    messages.append({
                        "role": "tool", 
                        "tool_call_id": tool_call.id, 
                        "content": str(result.content)
                    })

                final = await openai_client.chat.completions.create(
                    model="gpt-4o", messages=messages
                )
                return final.choices[0].message.content
            
            return response_message.content