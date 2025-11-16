from crewai import CrewAI, CrewAIError,agents, tools,process


def create_agent(agent_name: str, tool_names: list):
    try:
        selected_tools = [getattr(tools, tool_name) for tool_name in tool_names if hasattr(tools, tool_name)]
        agent = agents.create_agent(agent_name=agent_name, tools=selected_tools)
        return agent
    except CrewAIError as e:
        print(f"Error creating agent: {e}")
        return None

def run_agent(agent, prompt: str):
    try:
        response = agent.run(prompt)
        return response
    except CrewAIError as e:
        print(f"Error running agent: {e}")
        return None

if __name__ == "__main__":
    agent_name = "chat_agent"
    tool_names = ["SearchTool", "MathTool"]
    
    agent = create_agent(agent_name, tool_names)
    if agent:
        prompt = "What is the capital of France and what is 5 + 7?"
        response = run_agent(agent, prompt)
        if response:
            print(f"Agent Response: {response}")
