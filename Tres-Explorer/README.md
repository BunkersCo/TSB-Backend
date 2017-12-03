<h3>How to install & run:</h3>

1. ./manage makemigrations

2. ./manage.py migrate

3. ./manage.py createsuperuser

4. ./manage.py runserver

<h3>Add Aggregator to your existing Django project:</h3>

1. Add aggregator.apps.AggregatorConfig to INSTALLED_APPS in settings.py - DONE

2. Add url(r'^aggregator/', include('aggregator.urls')) to your project urls.py - DONE

<h3> The ClassPass Crawler </h3>

The crawlers supports 3 types of crawls: smart, studios and studio (notice the plural and singular)

1.	Studios Method - Scrape a list of studios based on a ClassPass location ID

	This crawl will scrape and update the database with a preliminary list of studios using ClassPass.
	Example: ./manage.py classpass_crawler studios N
	N can be an integer between 1 to 30 which are location IDs on the ClassPass database

2.	Studio Method - Singular Scrape an individual studio information a long with the basic schedule)

	This will use the slug field to scrape the appropriate page on ClassPass to gather information about a specific studio
	Example: ./manage.py classpass_crawler studio X
	X can be any id of an existing studio in our database.

3.	Smart Method - This command will only scrape and update only the missing data.

	Example: ./manage.py classpass_crawler smart 1

<h3> Geolocation Search, Spatial Functions and required MySQL 5.6 </h3>

To take advantage of the search function you must use it with >= MySQL 5.6 since this is using the built in spatial search functions that 5.6 provides. If one chooses not to use 5.6, the search will not work and will produce an error page. This is how the query looks like: 

	select id, astext(geom), name, address from aggregator_studioentry where st_within(geom, envelope(linestring(point(LONGITUDE-DISTANCE/abs(cos(radians(LATITUDE))*69), LATITUDE-(DISTANCE/69)), point(LONGITUDE+DISTANCE/abs(cos(radians(LATITUDE))*69), LONGITUDE+(DISTANCE/69)))))   order by st_distance(point(LONGITUDE, LATITUDE), geom) limit  50

	Note that the LATITUDE, LONGITUDE AND DISTANCE are variables

	To perform a search:

		1. Navigate to /search
		2. Enter longitude, latitude and the distance or simply enter a zipcode or an address, geopy will translate to coordinates

