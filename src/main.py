from page_scraper import get_page_json
from catalog import get_all_urls
import json
from os import path
from multiprocessing import Pool
import time
from argparse import ArgumentParser

def scrape(args) -> None:
    output_path = path.join(path.dirname(__file__), '..', 'output')
    courses_path = path.join(output_path, 'courses.json')

    urls_path = path.join(output_path, 'course_urls.txt')
    if not path.exists(urls_path):
        get_all_urls(urls_path)

    with open(urls_path,'r') as fobj:
        urls = fobj.read().strip().split("\n")

    t0 = time.time()

    # Get data from each url using multithreading
    with Pool(args.num_threads) as p:
        data = p.map(get_page_json, urls)

    t1 = time.time()
    print(f"Scraped {len(urls)} courses in {t1-t0}s")

    print("writing to disk...")
    data = {d["course_code"]: d for d in data if "course_code" in d}
    with open(courses_path, 'w+') as outfile:
        json_dict = {}
        json_dict["courses"] = data
        json.dump(json_dict, outfile, indent=2)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '-nt',
        '--num-threads',
        type=int, default=10,
        help='Number of threads to use when scraping course data'
    )

    scrape(parser.parse_args())
