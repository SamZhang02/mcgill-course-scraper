import urllib.request
import bs4 as bs 

def get_html_soup(url:str) -> bs.BeautifulSoup:
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs.BeautifulSoup(html, "html.parser")
    return soup

def get_title_words(html:bs.BeautifulSoup) -> str:
    title = html.title.string
    return title.split("|")[0].split()

def get_course_code(title:list) -> str:
    return title[0].lower() + title[1]

def get_course_credits(title:list) -> int:
    return int(title[-2].strip("("))

def get_course_name(title:list) ->str:
    return " ".join(title[2:-2])

def get_faculty(html:bs.BeautifulSoup) -> str:
    string = html.find_all("div",class_='meta')[0]
    return string.getText().strip().removeprefix("Offered by: ")

def get_terms(html:bs.BeautifulSoup) -> list:
    string = html.find_all("p",class_="catalog-terms")[0]
    string = string.getText().strip()
    string = string.removeprefix("Terms:")
    output = string.strip().split(",")
    if "not" in output[0]:
        return []
    return output 

def get_profs(html:bs.BeautifulSoup) -> list:
    string = html.find_all("p",class_="catalog-instructors")[0]
    string = string.getText().strip()
    string = string.removeprefix("Instructors:")
    string = string.removesuffix("(Winter)")
    output = string.strip().split("(Fall)")
    if "no" in output[0]:
        return []
    for i in range(len(output)):
        output[i] = [x.strip() for x in output[i].split(";")]
    return output

def get_overview(html:bs.BeautifulSoup) -> str:
    string = html.select("#node-22180 > div.content > p:nth-child(2)")[0]
    output = string.getText().strip()
    return output

def get_notes(html:bs.BeautifulSoup) -> list:
    string = html.find_all("ul","catalog-notes")[0]
    output = string.getText()
    output = output.strip().split("\n\n")
    return output


if __name__ == "__main__":
    course = get_html_soup("https://www.mcgill.ca/study/2022-2023/courses/mgcr-271")
    title = get_title_words(course)
    print(get_course_code(title))
    print(get_course_credits(title))
    print(get_course_name(title))
    print(get_faculty(course))
    print(get_terms(course))
    print(get_profs(course))
    print(get_overview(course))
    print(get_notes(course))
    pass
