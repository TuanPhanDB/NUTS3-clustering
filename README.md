# Clustering of NUTS3 Regions Using Eurostat Data with Unsupervised Machine Learning

The goal is to categorize or group these regions based on the available data by identifying similarities using unsupervised machine learning techniques. The clustering will be purely data-driven since we currently have no predefined categories or hypotheses about these regions.

## 1. Set up the database
   - Install Docker and PostgreSQL
   - Follow this link to create a database in Docker: https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/
   - Run the compose.yml file in the terminal using the command:
     
       **"docker-compose up -d"**
     
## 2. Data processing
   - Open Docker and start the database
   - In **main.py**, fill in the information of the database to the connection part
     
   ![connecting](https://github.com/user-attachments/assets/2e4312c2-81ae-4586-b20f-59b9f626be6b)

   - Run **main.py** for processing data and put it in the database
   - Perform the same process for **visualize_prep.py**. This file will generate Excel files used for the visualization task
   - If you want to view the data or perform queries, you can use DBeaver to connect to your PostgreSQL database 
   
## 3. Visualization
   - Open file **Visualization.ipynb**
   - There are 2 sections: **TIME visualization** and **COUNTRY visualization**
   - Run all the cells in your target section, and then you can start choosing filters for the visualization
   - When running the **TIME visualization**, change the path to your target folder that contains Excel files generated from the below steps
   - When running the **COUNTRY visualization**, it will take time because the script needs to read data and filter it
   - **Notes: There are some errors in the visualization**:

      - There are 2 missing parts in the CSV folder: **'Projected'** and **'Population and housing censuses 2011'**
      - Normally, the heatmap will be shown like this
    
     ![normal](https://github.com/user-attachments/assets/43e8e235-4841-4576-b325-89eac5616c6d)
     
      - However, when the chosen data contains only a 0 value, the heatmap will be filled with only green instead of grey
    
     ![error_all_0](https://github.com/user-attachments/assets/913e698c-04a5-49bc-88c6-4b52bb560a21)

      - In case the selected 'geo' is not available in the current filtered data frame, the heatmap will be shown below

     ![no_available](https://github.com/user-attachments/assets/9c6e7565-e2a1-4681-913d-e001955a7d8c)

