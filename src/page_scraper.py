import urllib.request
import bs4 as bs 

def get_html_soup(url:str) -> bs.BeautifulSoup:
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return None
    html = response.read()
    soup = bs.BeautifulSoup(html, "html.parser")
    return soup

def get_title_words(html:bs.BeautifulSoup) -> list:
    title = html.title.string
    return title.split("|")[0].split()

def get_course_code(title:list) -> str:
    return title[0].lower() + title[1]

def get_course_credits(title:list) -> str:
    if "credit" in title[-1]:
        return title[-2].strip("(")
    return 0

def get_course_name(title:list) ->str:
    if len(title) > 2:
        return " ".join(title[2:-2])
    return ""

def get_faculty(html:bs.BeautifulSoup) -> str:
    string = html.find_all("div",class_='meta')[0]
    string = string.getText().strip().split('\n')[0]
    return string.removeprefix("Offered by: ")

def get_terms(html:bs.BeautifulSoup) -> list:
    string = html.find_all("p",class_="catalog-terms")[0]
    string = string.getText().strip()
    string = string.removeprefix("Terms:")
    output = string.strip().split(",")
    if "not" in output[0]:
        return []
    return output 

def get_profs(html:bs.BeautifulSoup) -> dict:
    output = {
        'fall':[],
        'winter':[],
        'summer':[],
    }

    string = html.find_all("p",class_="catalog-instructors")[0]
    string = string.getText().strip()
    if "There are no" in string:
        return {}
    profs = string.removeprefix("Instructors:").strip()
    if "(Fall)" in string:
        temp = profs.split("(Fall)")
        output["fall"] += [x.strip() for x in temp[0].split(";")]
        if len(temp) > 1:
            profs = temp[1].strip()
    if "(Winter)" in string:
        temp = profs.split("(Winter)")
        output["winter"] += [x.strip() for x in temp[0].split(";")]
        if len(temp) > 1:
            profs = temp[1].strip()
    if "(Summer)" in string:
        temp = profs.split("(Summer)")
        output["summer"] += [x.strip() for x in temp[0].split(";")]
        if len(temp) > 1:
            profs = temp[1].strip()
    return output

def get_overview(html:bs.BeautifulSoup) -> str:
    string = html.find(class_='node node-catalog clearfix').find(class_="content").select("p:nth-child(2)")[0]
    output = string.getText().strip()
    return output

def get_notes(html:bs.BeautifulSoup) -> list:
    notes = html.find_all("ul","catalog-notes")
    if not notes:
        return []
    string = notes[0]
    output = string.getText()
    output = output.strip().split("\n\n")
    return output

def get_prerequisites(notes:list) -> list:
    for note in notes:
        if note.startswith("Prerequisite"):
            try:
                output = note.split(":")[1].strip()
            except: 
                output = note.strip()
            return output

def get_corequisites(notes:list) -> str:
    for note in notes:
        if note.startswith("Corequisite"):
            output = note.split(":")[1].strip()
            try:
                output = note.split(":")[1].strip()
            except: 
                output = note.strip()
            return output

def get_restrictions(notes:list) -> str:
    for note in notes:
        if note.startswith("Restriction"):
            output = note.split(":")[1].strip()
            try:
                output = note.split(":")[1].strip()
            except: 
                output = note.strip()
            return output

def get_other_notes(notes:list) ->list:
    output = []
    for note in notes:
        if not (note.startswith("Restriction") or note.startswith("Corequisite") or note.startswith("Prerequisite")):
            output.append(note.strip())
    return output

def get_page_json(url:str) -> dict:
    print(f"Currently parsing {url}")
    course = get_html_soup(url)
    course_code = url.split('/')[-1].strip()
    course_code = "".join(course_code.split('-'))

    if not course:
        return {
            "course_code":course_code,
            "message": f'Invalid url at {url}'}
    try:
        title = get_title_words(course)
        notes = get_notes(course)
        return {
            "url": url,
        "course_code": get_course_code(title),
        "credits": get_course_credits(title),
        "course_name": get_course_name(title),
        "offered_by": get_faculty(course),
        "year": "2022-2023",
        "terms": get_terms(course),
        "overview": get_overview(course),
        "instructors": get_profs(course),
        "prerequisites": get_prerequisites(notes),
        "corequisites": get_corequisites(notes),
        "restriction": get_restrictions(notes),
        "other_notes": get_other_notes(notes)
        }
    except:
        return {
                "course_code":course_code,
                "message": f'Error at url: {url}'
            }

if __name__ == "__main__":
    url = "https://www.mcgill.ca/study/2022-2023/courses/math-323"
    print(get_page_json(url))
