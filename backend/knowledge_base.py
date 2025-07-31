from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pickle

def create_knowledge_base(documents):
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    texts = [doc["content"] for doc in documents]
    metadatas = [{"source": doc["url"]} for doc in documents]
    
    documents = text_splitter.create_documents(texts, metadatas=metadatas)
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    
    # Save the knowledge base
    db.save_local("company_knowledge")
    print("Knowledge base created successfully")

if __name__ == "__main__":
    import json
    with open("scraped_data.json", "r") as f:
        documents = json.load(f)
    create_knowledge_base(documents)