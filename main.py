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
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
from sqlalchemy import URL
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------Data collection-----------------------------------------------------------------#
#-----------------------------Perform collect all possible NUTS-3 data-------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

# pd.set_option('display.max_colwidth', None)
# pd.reset_option('display.max_colwidth')

def data_collect():
  #Get all possible dataset from eurostat
  try:
    toc_df = eurostat.get_toc_df()
  except Exception as e:
    print(e)

  #Take data related to NUTS 3
  df = pd.DataFrame(columns=['table_id', 'min', 'max', 'table_name'])
  for idx, row in toc_df.iterrows():
    if 'NUTS 3' in row['title']:
      new_row = {'table_id': row['code'], 'min': row['data start'], 'max': row['data end'], 'table_name': row['title']}
      df = df._append(new_row, ignore_index=True)

  #List NUTS 3 dataset from GitHub
  url = 'https://raw.githubusercontent.com/sumtxt/regionaldata-guide-eu/refs/heads/main/files/eurostat_nuts3_tables_avail.csv'
  df1 = pd.read_csv(url)

  #Remove decimal point in df1
  df1['min'] = df1['min'].astype(str).apply(lambda x: x.replace('.0',''))
  df1['max'] = df1['max'].astype(str).apply(lambda x: x.replace('.0',''))

  #Check if GitHub data not exist in df, append it to df
  for idx, row in df1.iterrows():
    if row['table_id'].upper() not in df['table_id'].to_list():
      new_row = {'table_id': row['table_id'], 'min': row['min'], 'max': row['max'], 'table_name': row['table_name']}
      df = df._append(new_row, ignore_index=True)


  #These are sub-data of some datasets, can be deleted
  data_deleted = ['NAMA_10R_3EMPERS$DV_1564', 'NAMA_10R_3GDP$DV_1562', 'NAMA_10R_3GVA$DV_1563',
                 'NRG_CHDDR2_M', 'DEMO_R_FIND3$DV_1541', 'DEMO_R_GIND3$DV_1542',
                 'ROAD_GO_NA_RL3G$DV_1581', 'ROAD_GO_NA_RU3G$DV_1582', 'DEMO_R_PJANIND3$DV_1561',
                 'DEMO_R_MWEEK3', 'DEMO_R_MWK3_10', 'DEMO_R_MWK3_20', 'DEMO_R_MWK3_T', 'DEMO_R_MWK3_TS'
                 ]

  df = df[~df['table_id'].isin(data_deleted)]

  #Insert new column 'Category'
  if 'Category' not in df.columns:
    df.insert(1, 'Category', 'NaN')

  #Categorized the data
  categories = {'Tourism': 'TOUR',
                'Annual national accounts': 'NAMA_10R' ,
                'Energy': 'NRG_CHDDR2_A',
                'Road Accident': 'TRAN_SF',
                'Patent': 'PAT_EP',
                'Structure of agricultural holdings': 'EF_R',
                'Projected': 'PROJ',
                'Area': 'REG_AREA3',
                'Demography': 'DEMO_R',
                'National road': 'ROAD_GO',
                'Intellectual property rights': 'IPR',
                'Agri-environmental indicators': 'AEI',
                'Business demography': 'BD',
                'Population and housing censuses 2001': 'CENS_01',
                'Population and housing censuses 2011': 'CENS_11',
                'Population and housing censuses 2021': 'CENS_21',
                'Police record': 'CRIM_GEN',
                'Labour force survey': 'lfst_r'
                }

  def classify(s):
    for category in categories:
        if re.match(categories.get(category), s):
            return category
    return "NaN"

  #Write into Category column
  for idx, row in df.iterrows():
    df.at[idx, 'Category'] = classify(row['table_id'])

  #Reset index
  df = df.reset_index(drop=True)
  return df
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------Data processing------------------------------------------------------------------#
#-----------------------------Function to selecting target columns-----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
def selecting_cols(cur_data, row):

  #Get all year columns
  cur_df = cur_data.select_dtypes(include=np.number)

  #Reduce memory usage
  for i in cur_df.columns:
    cur_df[i] = pd.to_numeric(cur_df[i], downcast='float')
    cur_df[i] = cur_df[i].astype('float32')

  #Add 'table_id' column
  cur_df.insert(0, 'id', row['table_id'])
  #Add 'category' column
  cur_df.insert(1, 'category', row['Category'])
  #Add 'geo' column
  cur_df.insert(2, 'geo', cur_data['geo\\TIME_PERIOD'])

  #Add 'unit' column
  if 'unit' in cur_data.columns:
    cur_df.insert(3, 'unit', cur_data['unit'])
  else:
    cur_df.insert(3, 'unit', 'NaN')

  return cur_df
#----------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------Function to concat df with sample df------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
def concat_data(df):
    #Create a sample df to ensure all dataframe have same schema
    sample_df = pd.DataFrame(columns=ped_l)
    sample_df.insert(0, 'id', '')
    sample_df.insert(1, 'category', '')
    sample_df.insert(2, 'geo', '')
    sample_df.insert(3, 'unit', '')

    #Concat first data with empty final_df
    sample_df = pd.concat([sample_df, df], ignore_index=True)

    return sample_df
   
#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------Perform writing data to database-------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
#Prepare dataframe
df = data_collect()

#Unpickling all available countries list and period list
with open("geo_list", "rb") as fp:   
   geo_l = pickle.load(fp)

with open("period_list", "rb") as fp:   
   ped_l = pickle.load(fp)

#Parameters for database connection
user=""
password=""
host = ""
database=""
port=

# Create connection string
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Connect to the PostgreSQL database
engine = create_engine(connection_string)


try:
    #Loop through all dataset in df
    for idx, row in df.iterrows():

        #Get current dataset
        cur_data = eurostat.get_data_df(row['table_id'])

        #Perform choosing cols
        cur_df = selecting_cols(cur_data, row)

        #Call concat function
        final_df = concat_data(cur_df)
        print(row['table_id'])

        #Insert data to table
        final_df.to_sql('final_data', engine, if_exists='append', index=False, chunksize=1000)

        gc.collect()
    
    print(f"Data written successfully to database '{database}'.")

except Exception as e:
    print("Error:", e)


