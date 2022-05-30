
import pandas as pd
from pymongo import MongoClient
import dask.dataframe as dd
from dask_mongo import to_mongo, read_mongo
import dask.bag as bag
import json

#Read pandas dataframe
#df = pd.read_csv('assignment_2/data/Hotel_Reviews.csv')


# Convert datafram to json file
# result = dd.to_json(df, url_path='assignment_2/hotel_reviews.json')

# # convert json file to dask bag
# b = bag.read_text('assignment_2/hotel_reviews.json/*.part').map(json.loads)


# # Write to a Mongo database
# to_mongo(
#     b,
#     database="hotel_reviews",
#     collection="hotel_reviews",
#     connection_kwargs={"host": "mongodb+srv://root:root@cluster0.ixugzkq.mongodb.net/?retryWrites=true&w=majority"}
# )

def get_hotel_data():

    db = MongoClient("mongodb+srv://root:root@cluster0.ixugzkq.mongodb.net/?retryWrites=true&w=majority").hotel_reviews

    def get_hotel_data_1():
        return db.hotel_reviews.aggregate([
            {"$limit": 600000},
            {"$addFields": {"_id": {"$toString": "$_id"}}},
            { 
            "$group" : { 
                "_id" : { 
                    "lat" : "$lat", 
                    "Hotel_Address" : "$Hotel_Address", 
                    "Average_Score" : "$Average_Score", 
                    "Hotel_Name" : "$Hotel_Name", 
                    "lng" : "$lng"
                }
            }
            }, 
            { 
            "$project" : { 
                "Hotel_Name" : "$_id.Hotel_Name", 
                "Hotel_Address" : "$_id.Hotel_Address", 
                "Average_Score" : "$_id.Average_Score", 
                "lat" : "$_id.lat", 
                "lng" : "$_id.lng", 
            }
            }
        ])

       



    df = pd.DataFrame(get_hotel_data_1())

    df_amsterdam = df.loc[((df['lat'] > 52) & (df['lat'] < 53)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_amsterdam['city'] = 'The Netherlands, Amsterdam'
    df_paris = df.loc[((df['lat'] > 48.6) & (df['lat'] < 49)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_paris['city'] = 'France, Paris'
    df_london = df.loc[((df['lat'] > 51) & (df['lat'] < 52)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_london['city'] = 'United Kingdom, London'
    df_vienna = df.loc[((df['lat'] > 48) & (df['lat'] < 48.5)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_vienna['city'] = 'Austria, Vienna'
    df_milan = df.loc[((df['lat'] > 45) & (df['lat'] < 46)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_milan['city'] = 'Italy, Milan'
    df_barcelona = df.loc[((df['lat'] > 41) & (df['lat'] < 42)), ['lat', 'lng', 'Hotel_Address', 'Hotel_Name', 'Average_Score']]
    df_barcelona['city'] = 'Spain, Barcelona'

    df_comb = pd.concat([df_amsterdam, df_paris, df_london, df_vienna, df_milan, df_barcelona])
    print(df_comb)

    df_comb.to_csv('EU_hotels_map.csv')

get_hotel_data()




