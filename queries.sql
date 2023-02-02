-- Створення таблиці wiki_articles з назвами статей
CREATE TABLE wiki_articles (
	article_id serial PRIMARY key,
	title varchar(100) NULL,
	number_links int4 NULL
);

-- Створення таблиці articles_links з назвами статей, на які посилається стаття з таблиці articles_links
CREATE TABLE articles_links (
  link_id serial PRIMARY key,
  link_title varchar null
);

-- Створення таблиці wiki_art_art_links, яка містить зв'язки таблиці wiki_articles з articles_links
CREATE TABLE wiki_art_art_links (
  id serial PRIMARY key,
  aid INT,
  lid INT,
  CONSTRAINT fk_wiki_articles FOREIGN KEY(aid) REFERENCES wiki_articles(article_id),
  CONSTRAINT fk_articles_links FOREIGN KEY(lid) REFERENCES articles_links(link_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Топ 5 найпопулярніших статей (ті що мають найбільшу кількість посилань на себе)
SELECT articles_links.link_title, COUNT(articles_links.link_title)
FROM articles_links
JOIN wiki_art_art_links ON articles_links.link_id = wiki_art_art_links.lid
GROUP by articles_links.link_title
ORDER BY count DESC
limit 5

-- Топ 5 статей з найбільшою кількістю посилань на інші статті
SELECT wiki_articles.title, COUNT(wiki_articles.title)
FROM wiki_articles
JOIN wiki_art_art_links ON wiki_articles.article_id = wiki_art_art_links.aid
GROUP BY wiki_articles.title
ORDER BY count DESC
limit 5

-- Для заданної статті 'Дружба' знайти середню кількість потомків другого рівня
SELECT AVG((SELECT COUNT(1) FROM wiki_articles JOIN wiki_art_art_links ON wiki_articles.article_id = wiki_art_art_links.aid and a1.link_title = wiki_articles.title))
FROM
(SELECT articles_links.link_title
FROM wiki_articles
JOIN wiki_art_art_links ON wiki_articles.article_id = wiki_art_art_links.aid AND wiki_articles.title = 'Дружба'
JOIN articles_links ON articles_links.link_id = wiki_art_art_links.lid) a1