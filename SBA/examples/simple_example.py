import sys
import os

# Add the SBA folder to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sba import Agent, SBA

# Define a simple tool for Agent 1
def greet_user(name: str):
    return f"Hello, {name}! How can I assist you today?"

# Define a simple tool for Agent 2
def farewell_user(name: str):
    return f"Goodbye, {name}! Have a great day!"

# Define Agent 1
agent1 = Agent(
    name="Greeting Agent",
    instructions=(
        "You are a friendly agent. Greet the user and ask for their name. "
        "Always respond in a concise and professional manner. "
        "Do not include internal reasoning or tags like <think> in your responses."
    ),
    tools=[greet_user],
)
# Define Agent 2
agent2 = Agent(
    name="Farewell Agent",
    instructions=(
        "You are a polite agent. Say goodbye to the user. "
        "Always respond in a concise and professional manner. "
        "Do not include internal reasoning or tags like <think> in your responses."
    ),
    tools=[farewell_user],
)

# Define a handoff tool to transfer from Agent 1 to Agent 2
def transfer_to_farewell_agent():
    return agent2

# Add the handoff tool to Agent 1
agent1.tools.append(transfer_to_farewell_agent)

# Initialize SBA with Agent 1
sba = SBA(agent1)

# Simulate a conversation
print("Start conversation with the user:")
user_input = "Hi!"
print(f"User: {user_input}")

# Agent 1 responds
response = sba.interact(user_input)
print(f"Assistant: {response}")

# User provides their name
user_input = "My name is Alice."
print(f"User: {user_input}")

# Agent 1 responds and performs a handoff to Agent 2
response = sba.interact(user_input)
print(f"Assistant: {response}")

# Agent 2 says goodbye
user_input = "Bye!"
print(f"User: {user_input}")
response = sba.interact(user_input)
print(f"Assistant: {response}")