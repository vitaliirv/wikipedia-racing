# Wikipedia racing
Finding the shortest path between two Wikipedia articles

Problem: Need to go from one Wikipedia article to another with a minimal number of transitions.

To solve this problem, I wrote a function that takes two article names as parameters and returns a list of page names that link to it, or an empty list if no such path is found.

Example:
('Дружба', 'Рим') -> ['Дружба', 'Якопо Понтормо', 'Рим']

### Detailed description

1. Articles are analyzed only in the Ukrainian Wikipedia

2. The following types of technical references were excluded from the analysis:

    - https://uk.wikipedia.org/wiki/%D0%92%D1%96%D0%BA%D1%96%D0%BF%D0%B5%D0%B4%D1%96%D1%8F:%D0%92%D1%96%D0%B9%D0%BD%D0%B0/%D0%A0%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%B8
  
    - https://uk.wikipedia.org/wiki/%D0%9E%D0%B1%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8F:%D0%A8%D0%B5%D0%B2%D1%87%D0%B5%D0%BD%D0%BA%D0%BE_%D0%A2%D0%B0%D1%80%D0%B0%D1%81_%D0%93%D1%80%D0%B8%D0%B3%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%87

3. The frequency of references to Wikipedia is limited. The parameter used is the maximum number of requests per minute.
4. Error handling and retry for requests are provided
5. The program only takes the first 200 links on each page
6. The resulting link information from the page is stored in a postgres database running in the container
7. The next time it runs, it uses the database connections to avoid making the same queries twice
8. I created the following queries against the database, which will fill up after a few runs:

    - Top 5 most popular articles (those with the most references to yourself)
           
    - Top 5 articles with the most links to other articles
           
    - Average number of second-level descendants for a given article
           
    Recorded in the file: queries.sql

### Technologies used

1. The service is written in Python
2. Infrastructure: PostgreSQL run in docker using docker-compose.
3. Libraries: psycopg2, collections - deque, networkx - Graph, requests, re, time
