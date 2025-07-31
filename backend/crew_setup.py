from crewai import Agent, Task, Crew
from langchain.tools import tool
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Load knowledge base
db = FAISS.load_local("company_knowledge", OpenAIEmbeddings())

@tool
def search_company_knowledge(query: str) -> str:
    """Search the company knowledge base for relevant information"""
    docs = db.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

# Define agents
research_agent = Agent(
    role="Company Knowledge Expert",
    goal="Provide accurate information about the company, its products, and services",
    backstory="An AI that has been trained on all available company information",
    tools=[search_company_knowledge],
    verbose=True
)

support_agent = Agent(
    role="Customer Support Specialist",
    goal="Help customers with their inquiries in a friendly and professional manner",
    backstory="An AI trained in customer service best practices",
    verbose=True
)

# Define tasks
research_task = Task(
    description="Find relevant information about: {query}",
    agent=research_agent,
    expected_output="Accurate information from the company knowledge base"
)

support_task = Task(
    description="Use the provided information to craft a helpful response to: {query}",
    agent=support_agent,
    expected_output="A friendly, professional response that answers the customer's question"
)

# Create crew
crew = Crew(
    agents=[research_agent, support_agent],
    tasks=[research_task, support_task],
    verbose=2
)

def get_response(query):
    result = crew.kickoff(inputs={"query": query})
    return result