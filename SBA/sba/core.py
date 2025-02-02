from typing import List, Dict
from .agent import Agent, Response
from .utils import function_to_schema, execute_tool_call
from langchain_ollama import OllamaLLM  # Updated import

# Initialize your custom LLM
llm = OllamaLLM(model="deepseek-r1:1.5b")  # Updated class name

def clean_response(response: str) -> str:
    """
    Remove <think> tags and internal reasoning from the response.
    """
    if "<think>" in response:
        # Extract only the part after the last </think> tag
        response = response.split("</think>")[-1].strip()
    return response

def run_full_turn(agent: Agent, messages: List[Dict]) -> Response:
    current_agent = agent
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools = {tool.__name__: tool for tool in current_agent.tools}

        # Prepare the prompt for the LLM
        prompt = "\n".join([msg["content"] for msg in messages if msg["role"] in ["system", "user"]])
        response = llm.generate(prompts=[prompt])  # Updated to use `prompts`

        # Extract the generated message and clean it
        message_content = response.generations[0][0].text
        message_content = clean_response(message_content)  # Clean the response
        message = {"role": "assistant", "content": message_content}
        messages.append(message)

        if message['content']:
            print(f"{current_agent.name}: {message['content']}")

        if not message.get('tool_calls', []):
            break

        for tool_call in message['tool_calls']:
            result = execute_tool_call(tool_call, tools, current_agent.name)

            if isinstance(result, Agent):
                print(f"Handing off to {result.name}...")  # Debugging: Log the handoff
                current_agent = result
                result = f"Transferred to {current_agent.name}. Adopt persona immediately."

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": result,
            }
            messages.append(result_message)

    return Response(agent=current_agent, messages=messages[num_init_messages:])

class SBA:
    def __init__(self, initial_agent: Agent):
        self.agent = initial_agent
        self.messages = []

    def interact(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        response = run_full_turn(self.agent, self.messages)
        self.agent = response.agent
        self.messages.extend(response.messages)
        return response.messages[-1]['content']