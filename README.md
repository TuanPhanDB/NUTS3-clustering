# Clustering of NUTS3 Regions Using Eurostat Data with Unsupervised Machine Learning

The goal is to categorize or group these regions based on the available data by identifying similarities using unsupervised machine learning techniques. The clustering will be purely data-driven since we currently have no predefined categories or hypotheses about these regions.

## Notes:

1. Set up the database
   -
   - Install Docker and PostgreSQL
   - Follow this link to create a database in Docker: https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/
   - Run the compose.yml file in the terminal using the command:
     
       **"docker-compose up -d"**

2. Data processing
   -
   - Open Docker and start the database
   - Run main.py for processing data and put it in the database
   - Use DBeaver to view the data or perform queries
   - visualize_prep.py will generate Excel files used for visualization task

