Selects top 3 articles, orders authors by view,
 and finds dates with >1% failed requests
To run the program enter directory and enter 
 the following command:'python newsdata.py'

Source - newsdata.py
Output - output.txt

Methods:

	main() - runs the program

	iterate_dict(d, end) - present the result of the
		 SQL result dictionary neatly

		@arg c psycopg2 connection cursor

	delete_spam(c) - cleans the database of existing spam
		@arg c psycopg2 connection cursor

	get_article_views(c) - gets the top 3 most view articles
		@arg c psycopg2 connection cursor

	get_author_views(c) - gets the authors by view count
		@arg c psycopg2 connection cursor

	get_error_perc(c) - gets the dates with a >1% error requests
		@arg c psycopg2 connection cursor
