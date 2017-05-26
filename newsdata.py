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
    c.execute("SELECT name, COUNT(*) AS views" +
              " FROM articles, authors, log" +
              " WHERE articles.author = authors.id" +
              " GROUP BY name")
    iterate_dict(c.fetchall())


def get_error_perc(c):
    """ Get days with an error percent of over 2.5%

    Keyword argument:
    c -- psycopg2 connection cursor
    """
    c.execute("SELECT views.day, views.cnt FROM" +
              " (SELECT datelog.day," +
              "  (" +
              "   CAST(COUNT(CASE WHEN datelog.status != '200 OK'" +
              "    THEN 1 ELSE null END) AS float)" +
              "   /" +
              "   CAST(COUNT(*) AS float)" +
              "   ) AS cnt" +
              "   FROM (SELECT DATE(time) AS day," +
              "    status FROM log) AS datelog" +
              "   GROUP BY datelog.day" +
              "  ) AS views" +
              " WHERE views.cnt > 0.025")
    if(c.rowcount != 0):
        iterate_dict(c.fetchall(), end=10)
    print("No results found.")


main()
