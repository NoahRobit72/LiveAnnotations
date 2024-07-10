
#
# To do: Change this so that it reads from the correct format. At the moment, the data should just be x,y,z points
#


import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def getRobotData(id, unit):    
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "littlelab"
    url = "http://localhost:8086"
    
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    query_api = client.query_api()
    idString = str(id)
    
    inputString = f'''
        from(bucket: "TaskingProject")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == "measurement1")
        |> filter(fn: (r) => r["ID"] == "{id}")
        |> filter(fn: (r) => r["_field"] == "{unit}")
        |> last()
    '''  
    # print(inputString)

    tables = query_api.query(inputString, org="littlelab")
    
    # print(tables)
    for table in tables:
        for record in table.records:
            returnValue = record["_value"]
    
    return returnValue
    

    
    
    
class robortPositionStructure:
    def __init__(self, ids):
        self.nestedArray = []
        for _id in ids:
            entry = {"ID": _id, 'x': 0, 'z': 0}
            self.nestedArray.append(entry)

    def find_index_by_id(self, target_id):
        for index, item in enumerate(self.nestedArray):
            if item.get("ID") == target_id:
                return index
        return -1  # Return -1 if the ID is not found

    def insertZ(self, ID, z):
        index = self.find_index_by_id(ID)
        if index != -1:
            self.nestedArray[index]["z"] = z
        else:
            print(f"ID {ID} not found in the list.")
            
    def insertX(self, ID, x):
        index = self.find_index_by_id(ID)
        if index != -1:
            self.nestedArray[index]["x"] = x
        else:
            print(f"ID {ID} not found in the list.")
            
    def print_structure(self):
        for item in self.nestedArray:
            print(f"ID: {item['ID']}, x: {item['x']}, z: {item['z']}")
            
    def to_dict(self):
        return {"robots": self.nestedArray}
    
# ids = [1, 2, 3, 4, 5]

if __name__ == "__main__":
    print(getRobotData(6,"x"))
    
# getRobotData(6,"z")


    
# Example usage:
# ids = [1, 2, 3, 4, 5]
# recentDataArray = MostRecentData(ids)
# print(recentDataArray.nestedArray)


# [
#     {"ID": 8, 'x': 0,'z': 0}
#     {"ID": 7, 'x': 0,'z': 0}
# ]