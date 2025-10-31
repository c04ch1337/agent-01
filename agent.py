import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# Set your OpenAI API key (or use os.environ["OPENAI_API_KEY"] = "your-key")
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"

# LLM: The brain
llm = ChatOpenAI(temperature=0)

# TOOLS: Simple calculator
tools = [Tool(name="Calculator", func=lambda x: str(eval(x)), description="For math calculations")]

# Agent: Define the AI agent
agent = Agent(role="Math Solver", goal="Solve math problems accurately", backstory="You are a math expert", tools=tools, llm=llm, verbose=True)

# TASK: The job to do
task = Task(description="What is 5 * (3 + 2)?", expected_output="A numerical answer", agent=agent)

# Crew: Glue it together with memory
crew = Crew(agents=[agent], tasks=[task], memory=True, verbose=2)

# Run and print result
result = crew.kickoff()
print(result)
