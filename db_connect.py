import json

import psycopg2
from config import config


def connect(sql='SELECT version()'):
    """ Connect to the PostgreSQL database server """

    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql)

        # display the PostgreSQL database server version
        res = cur.fetchall()
        if sql == 'SELECT version()':
            print(f'PostgreSQL database version: \n{res[0]}')
        return res

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


def insert(page, links):
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # insert data into the database
        insert_query = """ INSERT INTO wiki_articles (title, number_links) VALUES (%s,%s) RETURNING article_id """
        record_to_insert = (page, len(links))
        cursor.execute(insert_query, record_to_insert)
        article_id = cursor.fetchone()[0]
        connection.commit()

        for link in links:

            sql = f"SELECT link_id, link_title FROM articles_links WHERE link_title='{link}'"
            cursor.execute(sql)
            answer = cursor.fetchone()

            if answer:
                lid = answer[0]
                insert_query = """ INSERT INTO wiki_art_art_links (aid, lid) VALUES (%s,%s) """
                record_to_insert = (article_id, lid)
                cursor.execute(insert_query, record_to_insert)
                connection.commit()

            else:

                insert_query = """ INSERT INTO articles_links (link_title) VALUES (%s) RETURNING link_id """
                record_to_insert = (link,)
                cursor.execute(insert_query, record_to_insert)
                link_id = cursor.fetchone()[0]

                insert_query = """ INSERT INTO wiki_art_art_links (aid, lid) VALUES (%s,%s) """
                record_to_insert = (article_id, link_id)
                cursor.execute(insert_query, record_to_insert)
                connection.commit()

        # print(count, "Record inserted successfully into DB")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into DB", error)
        return error

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")


if __name__ == '__main__':
    connect()



