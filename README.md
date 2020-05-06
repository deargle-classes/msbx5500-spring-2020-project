## MSBX5500 Final Project Repo Readme

### Contributors
  * Dave Eargle | Project Leader | [deargle](https://github.com/deargle)
  * Junji Wiener | Contributor | [8Jun](https://github.com/8Jun)
  * Alex Qaddourah | Contributor | [aqaddourah](https://github.com/aqaddourah)
  * Matthew Kuchar | Contributor | [mtmrevolt](https://github.com/mtmrevolt)
  * Jason Engel | Contributor | [birdsofjay](https://github.com/birdsofjay)
  * Seth Grossman | Contributor | [Sethegrossman](https://github.com/Sethegrossman)
  * Paul Telesca | Contributor | [shadow12490](https://github.com/shadow12490)

### Project Overview

This repository is for the Final project for class MSBX5500 - Security Analytics in Python. The project was to train a machine learning model to make predictions on network traffic and deploy a web solution that would be used in a SOC setting. The project is described in depth in the [report.md](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/report.md).

### How to start the application
  1. Start the GCP instance (Docker optimized OS) and ssh into it.

  2. Git clone this repository into your instance.

  3. Enter command: ```bash docker-compose build```

  4. Enter command: ```bash docker-compose up```

  5. If you want to check that all services are operating properly, use ```bash docker-compose ps``` in a new ssh tab. This command checks that all Docker services are working. All three services should be up and running.

	6. Enter command: ```bash docker-compose run web python init_psql_db.py``` while the web application is being run.

  7. After this, navigate to your external IP listed in your instance and the web app should be displayed. NOTE: Be sure that it is going to Port 80, and that the connection is HTTP, and not HTTPS.

  8. Once this is set up, the user will be able to upload (small) pcap files and see the alerts show up in the top part of the webpage.

### Notes
  1. Files that are uploaded to the web application may take some time to upload and process.

  2. Currently, large pcap files uploaded will cause a timeout with Heroku. Please only use small pcap files if possible.

  3. Because of the file size problem, this web application was not able to be uploaded using Heroku.
