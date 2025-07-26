import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_website(website):
    print("Launching chrome browser..")
    chrome_driver_path = "./chromedriver.exe"

    # Anti-scraping bypass techniques
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    
    # Set user-agent to mimic human browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(website)
        print("Page loaded..")
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extract structured info
        data = {
            "title": soup.title.string if soup.title else "No title",
            "metadata": {
                "description": soup.find('meta', attrs={'name': 'description'})['content'] 
                               if soup.find('meta', attrs={'name': 'description'}) else "",
                "keywords": soup.find('meta', attrs={'name': 'keywords'})['content'] 
                             if soup.find('meta', attrs={'name': 'keywords'}) else "",
                "viewport": soup.find('meta', attrs={'name': 'viewport'})['content'] 
                             if soup.find('meta', attrs={'name': 'viewport'}) else ""
            },
            "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])],
            "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
            "links": [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(('http', 'https'))],
            "tables": [str(table) for table in soup.find_all('table')],
            "accessibility": {
                "alt_tags": sum(1 for img in soup.find_all('img') if img.get('alt', '').strip()),
                "total_images": len(soup.find_all('img')),
                "aria_roles": len(soup.find_all(attrs={"role": True}))
            }
        }

        return data

    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return {
            "error": str(e)
        }
        
    finally:
        driver.quit()