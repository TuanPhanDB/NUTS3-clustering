#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------Library import------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
import pandas as pd
import eurostat
import numpy as np
from datetime import date
import re
import gc
import pickle
import os
import json
from sqlalchemy import create_engine, text
import psycopg2
from psycopg2 import sql
from sqlalchemy import URL
import tempfile

#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------Connect to database-------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
#Parameters for database connection
user=""
password=""
host = ""
database=""
port=

# Create connection string
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

def execute_query(query):
    try:
        # Connect to the PostgreSQL database
        engine = create_engine(connection_string)
        #print('Connection successful')

        with engine.connect() as connection:
            res = connection.execute(query)
            df = pd.DataFrame(res.fetchall(), columns=res.keys())

        gc.collect()
        return df

    except Exception as e:
        print("Error:", e)
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------xxxxxxxxxxxxxxxxxxx-------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
with open("geo_list", "rb") as fp:   
   geo_l = pickle.load(fp)

with open("period_list", "rb") as fp:   
   ped_l = pickle.load(fp)
   
category = ['Annual national accounts', 'Tourism', 'Energy', 'Road Accident', 'National road',
            'Patent', 'Structure of agricultural holdings', 'Agri-environmental indicators', 
            'Projected', 'Area', 'Demography', 'Business demography', 'Population and housing censuses 2001',
            'Population and housing censuses 2011', 'Population and housing censuses 2021',
            'Intellectual property rights', 'Police record', 'Labour force survey']


#Loop through category and geo
for cat in category:
    visual_df = pd.DataFrame(columns=['geo', 'Period', 'Available'])

    #Get all geo in current category
    query = text(f"SELECT * FROM final_data WHERE category = '{cat}';")
    df = execute_query(query)
    cur_geo_l = df['geo'].unique()
    
    #Loop through each geo
    for geo in cur_geo_l:

        cur_df = df[df['geo'] == geo]
        
        #Choose only year cols
        cols = ['category', 'unit', 'geo', 'id']
        cur_df = cur_df.drop([col for col in cols], axis=1)

        #Choose non_null cols in df
        avai_ped = list(set(cur_df.columns[cur_df.notnull().any()]))
        avai_ped.sort()

        #Prepare data for cur_df
        geo_list = [geo] * len(ped_l)
        avai_list = []
        for p in ped_l:
            if p in avai_ped:
                avai_list.append(1)
            else:
                avai_list.append(0)

        #Create empty df
        empty_df = pd.DataFrame()
        empty_df['geo'] = geo_list
        empty_df['Period'] = ped_l
        empty_df['Available'] = avai_list

        #Concat final df
        visual_df = pd.concat([visual_df, empty_df], ignore_index=True)
        gc.collect()
        
    #Export df to excel
    visual_df.to_excel(cat + ".xlsx")
    print(cat, len(visual_df))

        


