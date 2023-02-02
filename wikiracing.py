import json
import re
import time
from time import process_time
from collections import deque
import networkx as nx
from typing import List

import requests

from db_connect import connect, insert

requests_per_minute = 100
limit_time = 60  # time limit of 100 requests
links_per_page = 200
max_time = 200  # max time for searching
host = 'https://uk.wikipedia.org/wiki/'
regex = r'<a href=\"/wiki/[%A-Z0-9-_\(\)]+\" title=\"[\(\)\w]+[^:][\(\)\w\s-]+\">\D+</a>'


class WikiRacer:

    def time_elapsed(self, starting_time):
        """
           This function returns the elapsed time of the search.
           starting_time: The clock time when the WikiRacer start searching
        """
        current_time = process_time()
        return (current_time - starting_time) * 10

    def get_path_titles(self, link: str) -> List[str]:
        """
           This function returns the titles of all the links on the page.
           link: The article title of the page on which all links are parsed.
        """
        titles = []

        # get content from wikipedia
        try:
            contents = requests.get(f'{link}').content.decode('utf-8')
        except Exception:
            print(f"Error! The link {link} does not exist!")
            return titles

        # get page titles
        if contents:
            links = re.findall(f'{regex}', contents)[:links_per_page]
            for link in links:
                link = link.split('"')
                titles.append(link[3])
        return titles

    def find_path(self, start: str, finish: str) -> List[str]:
        """
           This function uses a graph to represent link-connectivity between the start and end pages.
           The shortest path is found using the Dijkstra's algorithm.
           start: title of the starting page
           finish: title of the end page
        """
        start_time = process_time()
        num_requests = requests_per_minute
        lim_time = limit_time
        print(f'WikiRacer is searching for the shortest path between "{start}" and "{finish}".')
        graph = nx.Graph()
        pages = deque()
        pages.append(start)
        found = False
        number_of_requests = 0

        while not found:

            for page in list(pages):
                query = f"SELECT articles_links.link_title FROM wiki_articles " \
                        f"INNER JOIN wiki_art_art_links ON wiki_articles.article_id = wiki_art_art_links.aid " \
                        f"INNER JOIN articles_links ON wiki_art_art_links.lid = articles_links.link_id " \
                        f"WHERE wiki_articles.title='{page}'"
                answer = connect(query)

                if answer:
                    links = [i[0] for i in answer]
                else:
                    links = self.get_path_titles(f'{host}{page}')
                    number_of_requests += 1
                    insert(page, links)

                print(f'{number_of_requests} requests to WIKI, {links}')

                # links = list(set(links))
                no_doubl_links = []
                [no_doubl_links.append(i) for i in links if i not in no_doubl_links]
                links = no_doubl_links
                if finish in links:
                    graph.add_edge(page, finish)
                    print(f'Processing time: {self.time_elapsed(start_time)} sec')
                    found = True
                    return nx.dijkstra_path(graph, start, finish)

                for title in links:
                    pages.append(title)
                    graph.add_edge(page, title)

                pages.popleft()
                processing_time = self.time_elapsed(start_time)
                print(f'{processing_time} sec')

                if processing_time >= lim_time and number_of_requests < num_requests:
                    lim_time += limit_time
                    num_requests = number_of_requests
                    num_requests += requests_per_minute

                if number_of_requests >= num_requests:
                    print(f'sleep {lim_time - processing_time} sec')
                    time.sleep(lim_time - processing_time)
                    num_requests += requests_per_minute
                    lim_time += limit_time

                if processing_time >= max_time:
                    msg = 'Path not found! The search time limit has expired!'
                    return []


def main():
    racer = WikiRacer()
    # print(racer.find_path('Дружба', 'Рим'))
    # print(racer.find_path('Мітохондріальна ДНК', 'Вітамін K'))
    # print(racer.find_path('Марка (грошова одиниця)', 'Китайський календар'))
    # print(racer.find_path('Фестиваль', 'Пілястра'))
    # print(racer.find_path('Дружина (військо)', '6 жовтня'))


if __name__ == '__main__':
    main()
