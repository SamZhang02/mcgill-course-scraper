from page_scraper import get_page_json
from catalog import get_all_urls 
import json
from os import path
import sys
import threading

def scrape() -> None:
    output_path = path.join(path.dirname(__file__), '..', 'output')
    courses_path = path.join(output_path, 'courses.json')
    with open(courses_path, 'w+') as outfile:
        json.dump({"courses":{}}, outfile)

    urls_path = path.join(output_path, 'course_urls.txt')
    if not path.exists(urls_path):
        get_all_urls(urls_path)

    with open(urls_path,'r') as fobj:
        urls = fobj.read().strip().split("\n")

    for url in urls:
        output = {}
        print(f'Currently parsing {url}')
        try:
            data = get_page_json(url)
        except KeyboardInterrupt:
            sys.exit(130)
        except:
            data = {}

        if "course_code" not in data:
            continue
        course_code = data["course_code"]

        with open(courses_path, 'w+') as outfile:
            json_dict = json.load(outfile)
            json_dict["courses"][course_code] = data
            json.dump(json_dict, outfile)

if __name__ == "__main__":
    scrape()
    pass