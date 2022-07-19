import os
import json
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

INPUT_FOLDER = 'input' 
INPUT_FILE = os.path.join(INPUT_FOLDER, 'urls.input')
OUTPUT_FOLDER = 'output'

def delete_output_dir():
    for url_folder in os.listdir(OUTPUT_FOLDER): # for every url folder in output
        local_folder_path = os.path.join(OUTPUT_FOLDER, url_folder)
        for file in os.listdir(local_folder_path): # delete every file in url dir
            os.remove(os.path.join(local_folder_path, file))
        os.rmdir(local_folder_path) # eventually remove the empty url dir

def create_url_folder(index: str):
    os.mkdir(os.path.join(OUTPUT_FOLDER, f"url_{str(index+1)}"))

def get_html(browser: webdriver.Chrome) -> str:
    return browser.page_source

def get_external_links(browser: webdriver.Chrome) -> list:
    imageLinks = [image.get_attribute("src") for image in browser.find_elements_by_xpath("//a//img")]
    website_urls = [elem.get_attribute("href") for elem in browser.find_elements_by_xpath("//a[@href]")]
    return imageLinks + website_urls

def init_output_folder():
    if not os.path.isdir(OUTPUT_FOLDER): # if output dir doesn't exists
        os.mkdir(OUTPUT_FOLDER)
    else:
        delete_output_dir() # delete everything inside

def get_urls_from_file() -> list:
    urls = open(INPUT_FILE,'r').read().split('\n')
    urls_index = [i for i in range(len(urls))]
    return list(zip(urls, urls_index))

def write_json(url_path: str, json_data: dict):
    with open(os.path.join(url_path, 'browse.json'), 'w',encoding='utf-8') as f:
        json.dump(json_data, f)

def scrape_page(url: list):
    create_url_folder(url[1]) # create a new folder for the url
    data = {}
    url_path = os.path.join(OUTPUT_FOLDER, f"url_{url[1]+1}") # save local path to url folder
    browser = webdriver.Chrome()
    browser.get(url[0]) # open url
    data["html"] = get_html(browser)
    data["resources"] = get_external_links(browser)
    data["screenshot"] = browser.get_screenshot_as_base64() 
    browser.save_screenshot(os.path.join(url_path, 'screenshot.png'))
    write_json(url_path,data)

def main():  
    urls = get_urls_from_file()
    init_output_folder()

    with ThreadPoolExecutor(max_workers=8) as executor: # init a thread pool executor
        executor.map(scrape_page, urls) # for each of the urls start func scrape_page

if __name__ == "__main__":
    main()