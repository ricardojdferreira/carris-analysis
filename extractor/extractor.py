import requests as rq
import io
import zipfile
from os import listdir
from os.path import isfile, join, dirname
import csv

class GTFS():

    def __init__(self):
        self.data_path = join(dirname(__file__),"data/")

    def get(self, date):
    
        response = rq.get("https://carris.tecmic.com/api/v2.7/GTFS/date/"+date)
        filebytes = io.BytesIO(response.content)
        myzipfile = zipfile.ZipFile(filebytes)

        return myzipfile

    def extract(self, myzipfile, date):
        path = self.data_path+date
        myzipfile.extractall(path=path)
        return

    def add_metadata(self, date):
        # Define data path
        path = self.data_path+date
        
        # Create filenames for csv conversion
        only_files = [[f, f.split(".")[0]+".csv"] for f in listdir(path) if isfile(join(path, f))]
        
        for item in only_files:
            with open(join(path, item[0]), "r") as read_file, open(join(path, item[1]), "w") as write_file:
                
                # Initialize reader objects
                reader = csv.reader(read_file)

                # Initialize writer objects
                writer = csv.writer(write_file)

                for i, line in enumerate(reader):
                    if i == 0:
                        line.append("file_name")
                        line.append("file_date")
                    else:
                        line.append(item[0].split(".")[0])
                        line.append(date)
                    writer.writerow(line)
        return

    def list_csv_files(self, date):
        # Define data path
        data_path = join(dirname(__file__), self.data_path+date)
        
        # Create filenames for csv conversion
        for f in listdir(data_path):
            file_extension = f.split(".")[1]
            file_path = join(data_path, f)

            if isfile(file_path) and file_extension == "csv":
                yield file_path

        
