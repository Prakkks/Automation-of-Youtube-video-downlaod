from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pytube import YouTube

# Define the search queries
urls = [
    'k+xa+%3F',
    'python subject'
]

def get_first_video_url(query):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Path to your webdriver executable
    
    driver = webdriver.Chrome( options=chrome_options)

    try:
        # Open YouTube search results for the given query
        driver.get(f'https://www.youtube.com/results?search_query={query}')
        
        # Wait for a few seconds to ensure the page loads completely
        driver.implicitly_wait(5)

        # Get the page source and parse it with BeautifulSoup using html.parser
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'html.parser')

        # Find the first video URL
        first_video = soup.find('a', id='video-title')
        if first_video:
            video_url = 'https://www.youtube.com' + first_video['href']
            return video_url
        else:
            return None
    finally:
        driver.quit()

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if stream:
            stream.download()
            print(f"Downloaded: {yt.title}")
        else:
            print("No suitable streams found")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    query = input("Enter a query")
    # query = urls[1]
    video_url = get_first_video_url(query)
    if video_url:
        print(f"First video URL: {video_url}")
        download_video(video_url)
    else:
        print("No video found")
