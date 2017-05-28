Selects top 3 articles, orders authors by view,
 and finds dates with >1% failed requests

Install vagrant with database:
https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip

Get newsdata.sql:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

To create the database enter directory and enter 
 the following command: 'psql -d news -f newsdata.sql'

To run the program enter directory and enter 
 the following command:'python newsdata.py'

Database - newsdata.sql
Source - newsdata.py
Output - output.txt

Methods: 

	main() - runs the program

	iterate_dict(d, end) - present the result of the
		 SQL result dictionary neatly

	get_article_views(c) - gets the top 3 most view articles
		@arg c psycopg2 connection cursor

	get_author_views(c) - gets the authors by view count
		@arg c psycopg2 connection cursor

	get_error_perc(c) - gets the dates with a >1% error requests
		@arg c psycopg2 connection cursor
