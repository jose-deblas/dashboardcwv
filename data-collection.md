# CLAUDE FILE 2 data-collection.md

This is a Core Web Vitals Dashboard built with Python and MySQL.

The project use Docker and the first time we install it in a server or computer the database. You can see how docker build different containers in the @docker-compose.yml
The Docker installation will provide a MySQL server.
The file @database/cwv_database.sql provides the queries to create the database and its tables.
We have and @Makefile with the usual options needed.
The project use uv for python dependencies.
The project will have a README.md file with all the explanation to install the app in local for developers.

The project is divided in two parts: Data Collection and Dashboard. We are gonna implement the job needed for Data Collection

### Data Collection

We'll have a part to make jobs that in the future could be executed, for example, from a jenkins server. 
The folder for jobs is located at @src/jobs/ and we need to complete the job needed to collect the data through the PageSpeed Insights API: @src/jobs/collect_pagespeed_data.py
So that, the job will take the urls from the 'urls' table. 
For each one, we'll call the PageSpeed Insights API passing as params: 
* url (urls.url)
* key (the .env api key value)
* strategy (urls.device)
* category: ['performance']

Use the resultant json with the class @src/domain/pagespeed_insights_metrics.py
The class PageSpeedInsightsMetrics can extract the relevant metrics necesaries to insert rows to the url_core_web_vitals database table. 
Find a better place into the folder structure for this class if necessary.
The target is to insert the core web vitals data in the table 'url_core_web_vitals' with the proper execution date.

If for some reason the script fails, some urls will last without data.
So that, if we execute the script again, we'll avoid to repeat the execution with the urls that already have data. That means that we'll use just those urls without data in 'url_core_web_vitals' for the current execution date.

Please, create as many tests as necessary with mockups to ensure that the job work as expected.
