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

def get_page_course_urls(url) -> list:
    HEADER = "https://www.mcgill.ca"
    output = []

    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return None

    html = response.read()
    soup = bs.BeautifulSoup(html, 'html.parser')
    course_links = soup.findAll('h4', attrs={'class' : 'field-content'})
    for h4 in course_links:
        output.append(HEADER + h4.find('a')['href'])
    return output

def get_all_urls() -> None:
    URL = "https://www.mcgill.ca/study/2022-2023/courses/search?page="
    with open("../output/course_urls.txt","w") as fobj:
        for i in range(520):
            url = URL + str(i)
            page_urls = get_page_course_urls(url)
            for link in page_urls:  
                fobj.write(link + '\n')

if __name__ == "__main__":
    get_all_urls()
    pass