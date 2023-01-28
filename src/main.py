from page_scraper import get_page_json
from catalog import get_all_urls 
import json
from os import path
import sys

def scrape() -> None:
    with open('../output/courses.json', 'w') as outfile:
            json.dump({"courses":{}}, outfile)

    if not path.exists("../output/course_urls.txt"):
        get_all_urls()

    with open("../output/course_urls.txt",'r') as fobj:
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

        with open('../output/courses.json', 'r') as outfile:
            json_dict = json.load(outfile)
        with open('../output/courses.json', 'w') as outfile:
            json_dict["courses"][course_code] = data
            json.dump(json_dict, outfile)

if __name__ == "__main__":
    scrape()
    pass