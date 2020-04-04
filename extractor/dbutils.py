import psycopg2
import os
import csv

class DB():

    def __init__(self):
        pass
    
    def connect(self, dbname, user, password, host, port):
        uri = f"dbname='{dbname}' user='{user}' host='{host}' port = '{port}' password='{password}'"
        self.connection = psycopg2.connect(uri)
        return

    def _table_exists(self, table_name):
        query = f"select * from information_schema.tables where table_name='{table_name}'"
        
        with self.connection.cursor() as cur:
            cur.execute(query)
            table_found = bool(cur.rowcount)
        
        return table_found
    
    def insert_data(self, file):
        _, file_name = os.path.split(file)
        table_name = file_name.split(".")[0]

        # create table if don't exist
        if not self._table_exists(table_name):
            # TODO: Add tableschema
            self._create_table(table_name, file)           
        
        # load data
        with self.connection.cursor() as cur:
            with open(file, "r") as file_buffer:
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV DELIMITER ',' QUOTE '\"' HEADER", file_buffer)
                self.connection.commit()
    
    def _create_table(self, table_name, file):
        
        # Open file to read header
        with open(file, "r") as read_file:
            reader = csv.DictReader(read_file)
            header = reader.fieldnames
        
        # Generate query to create table
        query_start = f"CREATE TABLE {table_name} (\n"
        query_middle = []
        for field in header:
            query_middle.append(f"{field} text")
        query_end = "\n);"
        query = query_start+",\n".join(query_middle)+query_end

        with self.connection.cursor() as cur:
            cur.execute(query)
        self.connection.commit()

        

            
