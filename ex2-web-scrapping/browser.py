import os
import json
from django.urls import path
from selenium import webdriver

INPUT_FOLDER = 'input' 
INPUT_FILE = os.path.join(INPUT_FOLDER, 'urls.input').replace("\\","/")
OUTPUT_FOLDER = 'output'

def delete_output_dir():
    for url_folder in os.listdir(OUTPUT_FOLDER):
        local_folder_path = os.path.join(OUTPUT_FOLDER, url_folder)
        for file in os.listdir(local_folder_path):
            os.remove(os.path.join(local_folder_path, file))
        os.rmdir(local_folder_path)

def create_url_folders(urls: list):
    for i in range(len(urls)):
        os.mkdir(os.path.join(OUTPUT_FOLDER, f"{str(i+1)}_url"))

def get_html(browser: webdriver.Chrome) -> str:
    return browser.page_source

def get_external_links(browser: webdriver.Chrome) -> list:
    imageLinks = [image.get_attribute("src") for image in browser.find_elements_by_xpath("//a//img")]
    website_urls = [elem.get_attribute("href") for elem in browser.find_elements_by_xpath("//a[@href]")]
    return [imageLinks + website_urls]

def init_output_folder():
    if not os.path.isdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    else:
        delete_output_dir() 

def get_urls_from_file() -> list:
    return open(INPUT_FILE,'r').read().split('\n')

def main():  
    urls = get_urls_from_file()
    init_output_folder()
    create_url_folders(urls)
    
    #browser = webdriver.Chrome()
    #browser.get('http://selenium.dev/')
    #browser.save_screenshot('screenshot.png')

if __name__ == "__main__":
    main()