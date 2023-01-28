# mcgill-course-scraper
Scraper written in Python that scrapes all courses from McGill University and their relevant information

---

"This project is **not** affiliated, endorsed, or vetted by McGill University. It is an open-source tool that uses publicly available information from the university and is intended for research and educational purposes only. Please refer to McGill University's terms of use for details on your rights to use the information downloaded. Remember - the information provided is intended for personal use only."

---

## Requirements
```
pip install -r requirements.txt
```

## Usage
MacOS 
```
python3 src/main.py 
```
Windows
```
py src/main.py
```

The program starts by scraping the URL of all courses on McGill University's official website and storing them in a `.txt` in `/output`. This should take a few minutes.

The program then requests each URL in the file and parses the individual pages one by one. This takes quite a bit longer, the process will be printed out on the terminal.

