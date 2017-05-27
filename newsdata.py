#! /usr/bin/env python3
import psycopg2


def main():
    """ Run the main loop """
    # Set up the connection to the database
    conn = psycopg2.connect(dbname="news")
    c = conn.cursor()

    delete_spam(c)
    print("\nDatabase cleaned.\n\n")
    print("Top 3 viewed articles:\n")
    get_article_views(c, " LIMIT 3")
    print("Authors by view count:\n")
    get_author_views(c)
    print("Dates with error percent over 1%:")
    get_error_perc(c)

    conn.close()


def iterate_dict(d, end=None):
    """ Present the result of the SQL result dictionary neatly

    Keyword arguments:
    d -- dictionary to print
    end -- index of end of key
    """
    for key, value in d:
        print("\"" + str(key)[0:end] + "\" - " + str(value))
    print("\n")


def delete_spam(c):
    """ Cleans the database of any spam

    Keyword argument:
    c -- psycopg2 connection cursor
    """
    c.execute("UPDATE log SET path = 'spam'" +
              "WHERE path = '/+++ATH0' OR path = '/%20%20%20'" +
              "OR path = '/spam-spam-spam-humbug';")
    c.execute("DELETE from log WHERE path = 'spam';")


def get_article_views(c, limit=""):
    """ Get 3 most popular articles by checking the log
         for the amount of times they were viewed

    Keyword argument:
    c -- psycopg2 connection cursor
    """
    c.execute("SELECT title, COUNT(*) AS views" +
              " FROM articles, log" +
              " WHERE articles.slug = SUBSTRING(log.path, 10)" +
              " GROUP BY articles.title ORDER BY views DESC" + limit)
    iterate_dict(c.fetchall())


def get_author_views(c):
    """ Order authors by views of all their articles

    Keyword argument:
    c -- psycopg2 connection cursor
    """
    c.execute("SELECT name, COUNT(*) as views" +
              " FROM authors, articles, log" +
              " WHERE authors.id = articles.author" +
              " AND path = CONCAT('/article/', slug)" +
              " GROUP BY name" +
              " ORDER BY views desc;")
    iterate_dict(c.fetchall())


def get_error_perc(c):
    """ Get days with an error percent of over 1%

    Keyword argument:
    c -- psycopg2 connection cursor
    """
    c.execute("SELECT date, err/total AS ratio" +
              " FROM (SELECT time::date as date," +
              " COUNT(*) AS total," +
              " SUM((status != '200 OK')::int)::float AS err" +
              " FROM log" +
              " GROUP BY date) AS errors" +
              " WHERE err/total > 0.01;")
    if(c.rowcount != 0):
        iterate_dict(c.fetchall(), end=10)
    else:
        print("No results found.")


main()
