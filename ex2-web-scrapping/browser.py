import os
import json
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from shutil import rmtree

INPUT_FOLDER = 'input' 
INPUT_FILE = os.path.join(INPUT_FOLDER, 'urls.input')
OUTPUT_FOLDER = 'output'

def get_external_links(browser: webdriver.Chrome) -> list:
    """
    Returns a list of URLs containing all the external links and images in a page'

    Args:
      browser (webdriver.Chrome): Current used browser

    Returns:
      list: A list of strings contaning external links and images
    """
    imageLinks = [image.get_attribute("src") for image in browser.find_elements_by_xpath("//a//img")]
    website_urls = [elem.get_attribute("href") for elem in browser.find_elements_by_xpath("//a[@href]")]
    
    return imageLinks.extend(website_urls)

def init_output_folder():
    if os.path.isdir(OUTPUT_FOLDER):
        rmtree(OUTPUT_FOLDER)
    os.mkdir(OUTPUT_FOLDER)

def read_urls_from_file() -> list:
    """
    Reads a local INPUT_FILE file, arranges the URLs with their indexes in a list of tuples

    Returns:
      list: list of tuples contaning URL,index
    """

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        urls = f.read().split('\n')
    urls_index = list(range(len(urls)))
    
    return list(zip(urls, urls_index))

def scrape_page(url: list):
    """
    Scrapes a page and saves its info in a unique folder inside the 'output' dir

    Args:
      list: (url) that contains the URL of the page and its index
    """
    #save local path to url folder
    url_path = os.path.join(OUTPUT_FOLDER, f"url_{url[1]+1}")
    os.mkdir(url_path)
    data = {}
    browser = webdriver.Chrome()
    browser.get(url[0])
    data["html"] = browser.page_source
    data["resources"] = get_external_links(browser)
    data["screenshot"] = browser.get_screenshot_as_base64() 
    browser.save_screenshot(os.path.join(url_path, 'screenshot.png'))

    with open(os.path.join(url_path, 'browse.json'), 'w',encoding='utf-8') as f:
        json.dump(data, f)

def main():  
    urls = read_urls_from_file()
    init_output_folder()

    # init a thread pool executor and run the scrape_page func foe each of the url
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scrape_page, urls)


if __name__ == "__main__":
    main()