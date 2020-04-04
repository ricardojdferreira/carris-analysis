import extractor
import dbutils
import datetime
import argparse
import sys
import time

def main(args):
    print(">>> main: started extractor")

    # time variables
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    today -= delta
    days = args.days

    # postgres variables
    database = args.database 
    user = args.user
    password = args.password
    host = args.host
    port = args.port

    db = dbutils.DB()
    db_connection_success = False
    while not db_connection_success:
        try:
            db.connect(database, user, password, host, port)
            db_connection_success = True
        except:
            print(">>> dbutils: No db connection, waiting 5 sec")
            time.sleep(5)
    print(">>> dbutils: Connection successful")

    # Extractor 
    xtract = extractor.GTFS()

    while days != 0:
        date = today.strftime('%Y-%m-%d')

        # download zip
        print(f">>> extractor: Downloading {date} data")
        myzipfile = xtract.get(date)

        # extract zip & save to db
        print(f">>> extractor: Extracting {date} date")
        xtract.extract(myzipfile, date)

        # add extra columns to files
        print(f">>> extractor: Adding metadata to {date} files")
        xtract.add_metadata(date)

        for file in xtract.list_csv_files(date):
            print(f">>> dbutils: Loading {file} to database")
            db.insert_data(file)

        today -= delta
        days -= 1
    print(">>> main: finished extractor")

if __name__ == "__main__":

    # User input
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("--database")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("--days", type=int)
    args = parser.parse_args(args)
    print(args)
    main(args)
