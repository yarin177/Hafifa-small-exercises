import os
import json
import requests

def delete_output_dir():
    for url_folder in os.listdir('output'):
        local_folder_path = os.path.join('output', url_folder)
        for file in os.listdir(local_folder_path):
            os.remove(os.path.join(local_folder_path, file))
        os.rmdir(local_folder_path)

def create_url_folders(urls: list):
    for i in range(len(urls)):
        os.mkdir('output//' + str(i+1) +  '_url')

def get_html(url: str) -> str:
    r = requests.get(url)

    if r.status_code == 200:
        return r.text
    else:
        return 'Could not retrieve HTML'

def main():
    if not os.path.isdir("output"):
        os.mkdir("output")
    else:
        delete_output_dir()  

    
    urls = open('input//urls.input','r').read().split('\n')
    create_url_folders(urls)
    get_html(urls[0])

if __name__ == "__main__":
    main()