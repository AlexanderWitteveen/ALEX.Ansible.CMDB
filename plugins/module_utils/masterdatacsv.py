import csv

class masterdatacsv:
    def __init__(self, environment, filename):
        self.environment = environment
        if self.environment not in ["dev", "prod"]:
            raise ValueError("Invalid environment. Must be 'dev' or 'prod'.")
        if self.environment != "dev":
            self.rootpath="/mnt/data-a1146/infrastructure-prod/cmdb/CMDB-MasterData/"
        else:
            self.rootpath="/mnt/data-a1142/infrastructure-dev/cmdb/CMDB-MasterData/"
        self.filename= self.rootpath + filename

    def readall(self):
        result=[]
        with open(self.filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                result.append(row)
        return result
