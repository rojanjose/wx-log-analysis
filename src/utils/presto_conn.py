import prestodb
import os
from dotenv import load_dotenv

class PrestoConnection:

    def __init__(self):
        # Load the .env file
        load_dotenv()

        self.PRESTO_HOST = os.environ["PRESTO_HOST"]
        self.PRESTO_HOST_PORT = os.environ["PRESTO_HOST_PORT"]
        self.PRESTO_USER = os.environ["PRESTO_USER"]
        self.PRESTO_PASSWORD = os.environ["PRESTO_PASSWORD"]
        self.PRESTO_CATALOG = os.environ["PRESTO_CATALOG"]
        self.PRESTO_SCHEMA = os.environ["PRESTO_SCHEMA"]
        self.PRESTO_CERT_PATH = os.environ["PRESTO_CERT_PATH"]

    def set_catalog(self, catalog_name):
        self.PRESTO_CATALOG = catalog_name

    def set_schema(self, schema_name):
        self.PRESTO_SCHEMA = schema_name

    # Establish the connection with SSL certificates
    def connect(self, secure_connection):
           
        self.conn = prestodb.dbapi.connect(
            host = self.PRESTO_HOST,
            port = self.PRESTO_HOST_PORT,
            user = self.PRESTO_USER,
            catalog = self.PRESTO_CATALOG,
            schema = self.PRESTO_SCHEMA,
            http_scheme = 'https',
            auth = prestodb.auth.BasicAuthentication(self.PRESTO_USER, self.PRESTO_PASSWORD)
        )

        if secure_connection is True:
            self.conn._http_session.verify = self.PRESTO_CERT_PATH
        else:
            print("Using unsecure mode of connection..")
            self.conn._http_session.verify = False


    # Query Presto DB
    def query(self, query):
        # Create a cursor to execute the query
        cursor = self.conn.cursor()
        cursor.execute(query)
        
        # Fetch and print the results
        rows = cursor.fetchall()
        # for row in rows:
        #     print(row)
        cursor.close()
        
        return rows
    

    #Close presto connection
    def close_connection(self):
        self.conn.close()
