import email
import quopri
import sys
from bs4 import BeautifulSoup

def extract_mhtml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
    
    html_content = ""
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            if payload:
                html_content += payload.decode('utf-8', errors='ignore')
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Trying to find the main post text. Typically LinkedIn posts have specific classes, but we can just grab text from paragraphs and spans.
        texts = []
        for tag in soup.find_all(['p', 'span']):
            if tag.string:
                clean = tag.string.strip()
                if len(clean) > 50:
                    texts.append(clean)
        
        with open('extracted.txt', 'w', encoding='utf-8') as out:
            for t in texts:
                out.write(f"{t}\n")
    else:
        print("No HTML content found.")

if __name__ == "__main__":
    extract_mhtml("data/loveit.mhtml")
