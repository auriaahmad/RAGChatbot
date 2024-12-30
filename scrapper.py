import os
import requests
from bs4 import BeautifulSoup

# Function to parse the local sitemap file
def parse_local_sitemap(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'xml')
            urls = [loc.text for loc in soup.find_all("loc")]
            return urls
    except Exception as e:
        print(f"Error reading sitemap file: {e}")
        return []

# Function to extract textual content from a webpage
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content
            text_content = soup.get_text(separator='\n', strip=True)

            return text_content
        else:
            print(f"Failed to fetch URL: {url} (Status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to save text with source URL
def save_text_with_url(text, url, save_directory, index):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"page_{index+1}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Source URL: {url}\n\n{text}")
    print(f"Saved text content for: {url}")

# Main execution
if __name__ == "__main__":
    sitemap_file = "sitemap.xml"  # Name of the sitemap file in the root folder
    save_directory = "text_pages"  # Directory to save text content

    # Parse the sitemap and extract URLs
    urls = parse_local_sitemap(sitemap_file)
    if urls:
        print(f"Found {len(urls)} URLs in the sitemap.")
        for index, url in enumerate(urls):
            text_content = extract_text_from_url(url)
            if text_content:
                save_text_with_url(text_content, url, save_directory, index)
    else:
        print("No URLs found in the sitemap.")