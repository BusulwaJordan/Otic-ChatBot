from bs4 import BeautifulSoup
import requests
from langchain.document_loaders import WebBaseLoader
import html2text

def scrape_website(base_url):
    # Fetch all pages (you might need to customize this)
    loader = WebBaseLoader(base_url)
    documents = loader.load()
    
    # Convert HTML to clean text
    h = html2text.HTML2Text()
    h.ignore_links = False
    
    cleaned_docs = []
    for doc in documents:
        cleaned = h.handle(doc.page_content)
        cleaned_docs.append({
            "url": doc.metadata["source"],
            "content": cleaned
        })
    
    return cleaned_docs

if __name__ == "__main__":
    company_url = "https://oticfoundation.org/" 
    scraped_data = scrape_website(company_url)
    print(f"Scraped {len(scraped_data)} pages")