# McGill-Course-Scraper
Scraper written in Python that scrapes all courses from McGill University and their relevant information.

Only valid for the 2022-2023 school year for now.

---

"This project is **not** affiliated, endorsed, or vetted by McGill University. It is an open-source tool that uses publicly available information from the university and is intended for research and educational purposes only. Please refer to McGill University's terms of use for details on your rights to use the information downloaded. Remember - the information provided is intended for personal use only."

---

## News
Version 0.2:
- Added multithreading to speed-up individual page scrapings.

## Requirements
```
pip install -r requirements.txt
```

## Usage
MacOS
```
python3 src/main.py --num-threads=25 [default: 50]
```
Windows
```
py src/main.py --num-threads=25 [default: 50]
```

The program starts by scraping the URL of all courses on McGill University's official website and storing them in a `.txt` in `/output`. This should take a few minutes.

The program then requests each URL in the file and parses the individual pages one by one, with 50 threads by default. This should take under 2 min, but feel free to change the number of threads in `main.py` to slow the requests down out of politeness. The process status will be printed out in the terminal as the program executes.

The output will be stored in `/output/courses.json`. See `/docs/structure.json` for a miniature example of what the file will look like.

## Contributing
Fork the repo and open a PR to `/dev` with the appropriate title and descriptions.
