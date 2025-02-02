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

# Define a handoff tool to transfer from Agent 1 to Agent 2
def transfer_to_farewell_agent():
    """Transfer the conversation to the Farewell Agent."""
    return agent2

# Define Agent 1
agent1 = Agent(
    name="Greeting Agent",
    instructions=(
        "You are a friendly agent. Greet the user and ask for their name. "
        "If the user says 'Bye!' or indicates they want to end the conversation, "
        "call the `transfer_to_farewell_agent` tool to hand off the conversation to the Farewell Agent. "
        "Always respond in a concise and professional manner. "
        "Do not include internal reasoning or tags like <think> in your responses."
    ),
    tools=[transfer_to_farewell_agent],  # Add the handoff tool
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


# Initialize SBA with Agent 1
sba = SBA(agent1)

# Simulate a conversation
print("Start conversation with the user:")
user_input = "Hi!"
print(f"User: {user_input}")

# Agent 1 responds
response = sba.interact(user_input)


# User provides their name
user_input = "My name is Alice."
print(f"User: {user_input}")

# Agent 1 responds and performs a handoff to Agent 2
response = sba.interact(user_input)


# Agent 2 says goodbye
user_input = "Bye!"
print(f"User: {user_input}")
response = sba.interact(user_input)
