## Welcome to Branch's Data Engineering take home project!

## Getting Started:

The goal is wrangle through some data, and test your basic knowledge of data engineering.
For this project, we will we using  the public *randomuser.me* API. 
This [API Endpoint](https://randomuser.me/api/?results=500) should be used for all the tasks

## Tasks:

1. Using the json response from the endpoint. Model, and design the database table/tables.
	-	You can use [dbdiagram](https://dbdiagram.io/d) to generate the ERD
	-	_Deliverable_: Export of ERD  - [Link](https://github.com/sanjaykmenon/branch_takehome/tree/main/erd)

	Some notes on the table modeling:
	-	the address_id, user_id columns are generated during the API call.
	-	These columns are used for indexing purposes. Even though UUIDs could be used as a 		primary key because UUIDs will end up taking more memory (16 bytes) as compared to 		INT values (4-bytes) or even big INT types (8-bytes)
	-	Debugging could be more complicated, for example imagine the expression WHERE id = 		'df3b7cb7-6a95-11e7-8846-b05adad3f0ae' instead of WHERE id = 5454346
	-	UUIDs could also have performance issues as they are not ordered unlike INT.

2. Build an end to end process in Python3, that generates a csv file for each of the tables you have designed
	-  The JSON results must be flatten
	-  The column names must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_)
	-  _Deliverable_: The python code, that can generate the csv files. [Link](https://github.com/sanjaykmenon/branch_takehome/blob/main/api_data_collection.py)



3. Now imagine this is a production ETL process. How would you design it? What tests would you put in place?
  - _Deliverable_: Any diagrams/text files that can show us your design. 



Please place the deliverables from all the tasks in a git repo and send us a link to review.


## File description

-	main.sh
	Runs the requirements.txt, salt.sh and api_data_collection.py files. 
	Set up environment and create csv files

-	salt.sh
	add env variables. This should not be added in a git repo but is added here for testing / reproducability.

-	api_data_collection.py
	The actual api call script that creates individual csv / tables.

-	branch_take_home.png
	ERD diagram

-	{date}_{entity}.csv
	Files containing table data for a particular day.


## Running this repo

-	navigate to the folder in your terminal
-	run the command "chmod +x main.sh"
-	run "sh main.sh" on your terminal 

## ETL Discuss

-	How would you design it?
	A few things I'd need to consider:
	-	Memory Efficiency
		If this API were to provide large data, to ensure that memory usage is efficient, I'd recommend re-writing the script to process the data as mini batches  / chunks of 100 or whatever applicable size. This will ensure no out of Memory errors while data transformation. Using this approach is also beneficial when it is a paid API service to ensure we minimize the number of API calls and thereby reduce costs.

	-	Backfilling
		If we are missing any information due to any service outage of the API, it would be beneficial to add a backfilling pipeline. For example, 3 months after running this API, we find that a new column has been added that has not been captured earlier. In this case, it would be beneficial to add a created_at column in the tables that can be used to then re-run the pipelines from a previous date to capture this missing data. This could also be setup as a check using some orchestration framework such as Airflow / Dagster.

	-	Logging  / Alerting
		Add Cloudwatch logs or equivalent in GCP to monitor stages of pipeline and generate alerts.

	-	Scaling

		GCP Batch can be used to scale this to run API calls specific to a data model (for example, one API call for address, one for users depending on the pricing setup)

-	What tests would you put in place?

-	I think testing can be done in a couple of ways.
	-	Testing during data ingestion:
		This approach means writing the data pipeline to check that it meets a particular pre-defined schema during data ingestion and then perform data transformations. The convenient part of this approach is that mistakes  / errors can be caught at the start. The cons here would be that it can be memory intensive based on the data being consumed and may not work well in a large scale distributed data framework. A possible approach is using PySpark infer schema to read JSON and load it as a Dataframe.

	-	Testing post ingestion:
		This involves running tests on the raw data after it has landed in the data warehouse / lake using something like dbt. The advantage here is that error-checking is moved to the landing zone where it is more performant (as this can be done using SQL), with the cons being that it can only be caught after it has been ingested, and the pipeline may need to be backfilled  / run again causing a disruption to stakeholders.

-	Anomaly Detection:
	Running data quality tests such as null count, min, max, stat distribution etc. to ensure the data being ingested is in line with a validation test suite. This can be done using PyDeequ / Great expectations. This could also be set up as a CI / CD check if the pipeline is managed through a dedicated git repo using GitHub actions / something similar. 


If you have any questions, concerns or suggestions please feel free to contact us. Happy coding!
