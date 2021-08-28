import pymongo
import pandas as pd
from urllib.parse import quote_plus
from pymongo import IndexModel, ASCENDING, DESCENDING



####################################################################################################
#                                             Setting                                              #
####################################################################################################



####################################################################################################
#                                             Variable                                             #
####################################################################################################



####################################################################################################
#                                             Function                                             #
####################################################################################################
class Mongo():

    # Initialize Connect Information
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = quote_plus(password)

    
    # Check Connection Status
    def check2mongo(self) -> None:
        try:
            with pymongo.MongoClient(f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?authSource={self.database}') as client:
                print(client.server_info())
                print('\nSuccess to connect Mongo!')
        except:
            print('Fail to connect Mongo!')


    # Connect To Mongo
    def connect2mongo(self, connect2db: bool=True):
        with pymongo.MongoClient(f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?authSource={self.database}') as client:
            if connect2db:
                db = client[self.database]
                return db
            else:
                return client
    

    # Mongo To DataFrame
    def mongo2dataframe(self, query: list, table: str, no_id: bool=True) -> pd.DataFrame:
        # connect
        db = self.connect2mongo()
        collection = db[table]
        # convert to DataFrame
        data = collection.aggregate(pipeline=query)
        df = pd.DataFrame(data=data)
        # delete Mongo default column '_id'
        if (no_id) and ('_id' in df.columns):
            del df['_id']
        # strip
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.strip()
        
        return df
    
    
    # DataFrame To Mongo
    def dataframe2mongo(self, df: pd.DataFrame, table: str) -> None:
        # connect
        db = self.connect2mongo()
        collection = db[table]
        # insert into Mongo
        records = df.to_dict(orient='records')
        collection.insert_many(records)


    # Delete Mongo Data
    def delete2mongo(self, filter: dict, table: str) -> None:
        # connect
        db = self.connect2mongo()
        collection = db[table]
        # delete from Mongo
        collection.delete_many(filter=filter)



