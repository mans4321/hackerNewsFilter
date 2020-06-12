import requests
import webbrowser
import sys

from bs4 import BeautifulSoup

INTEREST = {
    "devops",
    "mongo",
    "aws",
    "javascript",
    "js",
    "spring",
    "react",
    "css",
    "docker",
    "cicd",
    "python"
}


def must_be_int_and_larger_than(num_of_pages, larger):
    if not isinstance(num_of_pages, int):
        raise ValueError("page number should be int")
    if num_of_pages <= larger:
        raise ValueError("page number should bigger than 1")


def sort_hn_by_points(hn):
    return sorted(hn, key=lambda k: k["points"])


def get_soup_parser(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def is_news_of_interest(title):
    keywords = title.split()
    for word in keywords:
        if word.casefold() in INTEREST:
            return True
    else:
        return False


class HackerNews:

    def __init__(self):
        self.top_hn = []
        self.my_top_hn = []
        self.link = "https://news.ycombinator.com/news"

    def get_points(self, votes):
        if len(votes):
            return int(votes[0].getText().replace("points", ""))
        else:
            return 0

    def get_news(self, link, subtext):
        title = link.getText()
        href = link.get('href', None)
        votes = subtext.select('.score')
        points = self.get_points(votes)
        return {"title": title, "link": href, "points": points}

    def create_custom_news(self, links, subtexts):
        for idx, link in enumerate(links):
            news = self.get_news(link, subtexts[idx])
            title = news["title"]
            points = news["points"]
            if is_news_of_interest(title):
                self.my_top_hn.append(news)
            elif points > 99:
                self.top_hn.append(news)

    def get_hn_soup(self, page_num=1):
        link = f"{self.link}?p{page_num}"
        soup = get_soup_parser(link)
        return soup

    def scrape(self, num_of_pages=1):
        must_be_int_and_larger_than(num_of_pages, 0)
        for page in range(1, num_of_pages + 1):
            hn_soup = self.get_hn_soup(page)
            links = hn_soup.select(".storylink")
            subtext = hn_soup.select(".subtext")
            self.create_custom_news(links, subtext)


def get_new_index_from_user(list_size):
    while True:
        try:
            id = int(input("please enter the news number or 0 to exit: "))
            if id == 0:
                sys.exit()
            if id < 0 or id >= list_size:
                print(f"please enter a  larger than or equal 0 or smaller than {list_size}")
                continue
            return id
        except ValueError:
            print("please enter a number")


def read_news(my_top_hn):
    list_size = len(my_top_hn) + 1
    for idx, news in enumerate(my_top_hn):
        print(f"{idx + 1}. {news['title']}")
    print()
    while True:
        id = get_new_index_from_user(list_size) - 1
        url = my_top_hn[id]["link"]
        webbrowser.open(url)


def main():
    hakerNews = HackerNews()
    hakerNews.scrape(1)
    my_top_hn = hakerNews.my_top_hn
    top_hn = hakerNews.top_hn
    sort_hn_by_points(my_top_hn)
    sort_hn_by_points(top_hn)
    my_top_hn.extend(top_hn)
    read_news(my_top_hn)


main()
