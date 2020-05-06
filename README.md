## MSBX5500 Final Project Repo Readme

### Project Overview

Final project for MSBX5500 - Security Analytics in Python. Using the given CTU-13 dataset, we created a web application allowing a user to upload a pcap file, parsed it into netflow records, classify the traffic as a botnet or not, and allow the user to resolve alerts generated from the machine learning model on that uploaded traffic file.

#### [Project Proposal Document](https://github.com/deargle-classes/msbx5500-spring-2020/blob/master/project-proposal.md)

### Deliverables
* A single class github repository
* A heroku deployment of the final repo for each class member
* A markdown writeup within the final git repository which follows CRIPSP-DM format
  - [CRISP-DM Report](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/report.md)
* Cyber-security sudents: in class presentation

### High-Level Design

major high-level stuff about the code (e.g., that it's a Flask app along with a provided Dockerfile,
major dependencies such as argus and sklearn)

#### Modules
* Python function that parses pcaps into netflows
* Single code file that trains the models themselves, based on any arbitrary ctu-13 dataset. outputs the models, in pickled format
	* `models = [model for model in pickle.load(os.listdir('models'))]``
	* multiple models --
		* different datasets
		* different classifiers for a single given dataset
	* start with a single dataset, two classifiers
	* flask code which loads pickled models
* CRISP-DM report on the performance of the chosen models
	* feature importances
	* talks about all of this code in the deployment
* a way for the user to upload pcap files to a mongodb
* a way to store and display alerts if netflows surpass a certain malware-likelihood threshold/cutoff with psql

* Professor will provide
	* javascript to interact with skeleton routes that y'all will fill out for the app
	* flask route shells
	* a docker container which includes argus preinstalled

### Quickstart
"just use docker-compose and run it with a command like ____, yo." Except more formal and stuff

	1. Enter command: `docker-compose run web python init_psql_db.py` or it won't work
