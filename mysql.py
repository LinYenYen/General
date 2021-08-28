import pyodbc
import pandas as pd



####################################################################################################
#                                             Setting                                              #
####################################################################################################



####################################################################################################
#                                             Variable                                             #
####################################################################################################



####################################################################################################
#                                             Function                                             #
####################################################################################################
class MySQL():
    
    # Initialize Connect Information
    def __init__(self, server: str, port: str, database: str, user: str, password: str):
        self.server = server
        self.port = port
        self.database = database
        self.user = user
        self.password = password


    # Check Connection Status
    def check2mysql(self) -> None:
        try:
            with pyodbc.connect(f'DRIVER=MySQL ODBC 8.0 Unicode Driver;SERVER={self.server};PORT={self.port};DATABASE={self.database};UID={self.user};PWD={self.password};CHARSET=utf8mb4;') as conn:
                print(conn.getinfo(pyodbc.SQL_SERVER_NAME))
                print('\nSuccess to connect MySQL!')
        except:
            print('Fail to connect MySQL!')


    # Connect To MySQL
    def connect2mysql(self) -> pyodbc.connect:
        with pyodbc.connect(f'DRIVER=MySQL ODBC 8.0 Unicode Driver;SERVER={self.server};PORT={self.port};DATABASE={self.database};UID={self.user};PWD={self.password};CHARSET=utf8mb4;') as conn:
            return conn    


    # MySQL To DataFrame
    def mysql2dataframe(self, query: str) -> pd.DataFrame:
        # connect
        conn = self.connect2mysql()
        # convert to DataFrame
        df = pd.read_sql(sql=query, con=conn)
        # strip
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.strip()

        return df
    

    # DataFrame to MySQL
    def dataframe2mysql(self, df: pd.DataFrame, table: str) -> None:
        # connect
        conn = self.connect2mysql()
        # create insert query
        column = ""
        for col in df.columns:
            if column:
                column += f", `{col}`"
            else:
                column += f"`{col}`"

        question_marks = ""
        for i in range(len(df.columns)):
            if question_marks:
                question_marks += ', ?'
            else:
                question_marks += '?'
                
        rows = [tuple(df.loc[idx].to_list()) for idx in df.index]

        query = f"INSERT INTO {table} ( {column} ) VALUES ( {question_marks} )"

        # insert into MySQL
        cursor = conn.cursor()
        cursor.fast_executemany = True
        cursor.executemany(query, rows)
        conn.commit()

    
    # Execute MySQL
    def executeMySQL(self, query: str) -> None:
        # connect
        conn = self.connect2mysql()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()





####################################################################################################
#                                               Test                                               #
####################################################################################################
if __name__ == '__main__':

    import json

    # Load Config
    with open('./config.json', 'r') as j:
        config = json.load(j)
    # MySQL
    SERVER = config['MYSQL']['SERVER']
    PORT = config['MYSQL']['PORT']
    DATABASE = config['MYSQL']['DATABASE']
    USER = config['MYSQL']['USER']
    PASSWORD = config['MYSQL']['PASSWORD']

    mysql = MySQL(server=SERVER, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
    
    df = pd.read_csv(r'D:\Project\PyStock\master\2021/20210517_target.csv', encoding='utf-8')
    df['股票代號'] = df['股票代號'].astype(str)
    mysql.dataframe2mysql(df, table='stock.goodinfo_filter')

    # query = """
    #     -- sql
    #     SELECT *
    #     FROM stock.goodinfo_filter
    #     ;
    #     """

    # df = mysql.mysql2dataframe(query=query)










