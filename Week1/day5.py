import os
import requests
import json
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse

import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI


# Logging Configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - 🔍 %(message)s'
)
logger = logging.getLogger(__name__)

class WebsiteScraperError(Exception):
    """Custom exception with a fun twist."""
    def __init__(self, message):
        super().__init__(f"🕸️ Web Scraping Hiccup: {message}")

import requests
import chardet
from bs4 import BeautifulSoup
import logging

class Website:
    """Enhanced website scraper with robust encoding handling."""
    
    def __init__(self, url: str):
        # URL Validation with Emoji Flair
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        self.url = url
        self.title: str = ""
        self.text: str = ""
        self.links: List[str] = []
        
        try:
            # Improved request with encoding detection
            response = requests.get(
                url, 
                timeout=10,
                headers={'User-Agent': 'CompanyBrochureGenerator/1.0'}
            )
            response.raise_for_status()
            
            # Detect encoding
            encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
            
            # Decode content with detected or fallback encoding
            try:
                decoded_content = response.content.decode(encoding)
            except UnicodeDecodeError:
                # Fallback to utf-8 with error handling
                decoded_content = response.content.decode('utf-8', errors='ignore')
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(decoded_content, "html.parser")
            
            # Title Extraction with Fallback
            self.title = soup.title.string if soup.title else "Unnamed Company"
            
            # Text Extraction with Robust Encoding
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "noscript", "svg"]):
                    irrelevant.decompose()
                
                # Extract text, handling potential encoding issues
                self.text = soup.body.get_text(separator="\n", strip=True)
                
                # Ensure text is clean and readable
                self.text = ''.join(char for char in self.text if ord(char) < 128 or char in '\n\r\t')
            else:
                self.text = "No descriptive content found"
            
            # Smart Link Extraction
            links = [link.get("href") for link in soup.find_all("a") if link.get("href")]
            self.links = [
                link if link.startswith('http') else f"{self.url.rstrip('/')}/{link.lstrip('/')}"
                for link in links 
                if not any(x in link.lower() for x in ['privacy', 'terms', 'cookie', 'contact', '@'])
            ]
        
        except requests.RequestException as e:
            logging.error(f"Failed to access {url}: {e}")
            self.text = f"Unable to scrape website: {e}"
            self.links = []
    def get_contents(self) -> str:
        """Formatted content with emojis!"""
        return f"🌐 Webpage Title: {self.title}\n\n📄 Webpage Contents:\n{self.text}\n\n"

class BrochureGenerator:
    """Brochure generation with enhanced error handling and styling."""
    
    def __init__(self, api_key: Optional[str] = None):
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("🔑 No OpenAI API key provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = 'gpt-4o-mini'
    
    def create_brochure(self, company_name: str, url: str) -> str:
        """Generate a stylish, emoji-rich brochure."""
        system_prompt = """
        🌟 Professional Brochure Writer Mode Activated! 🌟
        
        Create an engaging markdown brochure that captures:
        
        🎯 Company Mission
        🚀 Innovative Services/Products
        🤝 Unique Company Culture
        💼 Career Opportunities
        🌈 Compelling Narrative
        
        Use emotive language, strategic formatting, and 
        highlight what makes this company special!
        """
        
        try:
            website = Website(url)
            
            user_prompt = f"""
            🏢 Company: {company_name}
            🌐 Website: {url}
            
            Detailed Website Analysis:
            {website.get_contents()}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"🚨 Brochure generation error: {e}")
            return f"## 🤖 Brochure Generation Error\n\n{e}"

