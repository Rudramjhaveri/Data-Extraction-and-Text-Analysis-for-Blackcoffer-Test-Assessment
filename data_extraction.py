import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm  # For progress bar

def extract_article(url):
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.find('h1', class_='entry-title').get_text(strip=True) if soup.find('h1', class_='entry-title') else ""

        # For Blackcoffer insights specifically, target the main article content
        article_content = soup.find('div', class_='td-post-content')
        
        if article_content:
            # Get all paragraphs within the article content
            paragraphs = article_content.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol'])
            
            # Process each paragraph
            processed_text = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                
                # Skip empty paragraphs and common unwanted elements
                if not text:
                    continue
                    
                # Skip navigation/sharing related text
                if any(skip in text.lower() for skip in ['share this:', 'click to share', 'previous article', 'next article']):
                    continue
                
                # Skip short promotional texts
                if len(text) < 20 and any(promo in text.lower() for promo in ['follow us', 'subscribe', 'sign up']):
                    continue
                
                processed_text.append(text)

            # Join all the processed text with proper spacing
            article_text = '\n\n'.join(processed_text)
            
            # Clean up extra whitespace
            article_text = re.sub(r'\n\s*\n', '\n\n', article_text)
            
            return f"{title}\n\n{article_text}"
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None

def main():
    # Set input and output paths
    input_file_path = 'D:/project/Input.xlsx'
    output_dir = 'extracted_articles'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the Excel file
    try:
        data = pd.read_excel(input_file_path)
        print(f"Successfully loaded {len(data)} articles from Excel file")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return
    
    # Create a log file for failed extractions
    failed_extractions = []
    
    # Process each URL with a progress bar
    for index, row in tqdm(data.iterrows(), total=len(data), desc="Extracting articles"):
        url_id = row['URL_ID']
        url = row['URL']
        
        # Extract article text
        article_text = extract_article(url)
        
        if article_text:
            # Save article to text file
            output_file_path = os.path.join(output_dir, f"{url_id}.txt")
            try:
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(article_text)
            except Exception as e:
                print(f"Error saving file {url_id}: {e}")
                failed_extractions.append((url_id, url, f"Error saving file: {str(e)}"))
        else:
            failed_extractions.append((url_id, url, "Failed to extract content"))
    
    # Save failed extractions to a log file
    if failed_extractions:
        log_path = os.path.join(output_dir, 'failed_extractions.txt')
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write("Failed Extractions:\n")
            for url_id, url, error in failed_extractions:
                log_file.write(f"URL_ID: {url_id}\nURL: {url}\nError: {error}\n\n")
        print(f"\nWarning: {len(failed_extractions)} articles failed to extract. See 'failed_extractions.txt' for details.")
    
    print("\nExtraction completed!")
    print(f"Successfully processed: {len(data) - len(failed_extractions)} articles")
    print(f"Failed: {len(failed_extractions)} articles")
    print(f"Articles saved in '{output_dir}' directory")

if __name__ == "__main__":
    main()