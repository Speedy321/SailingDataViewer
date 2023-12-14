import pandas as pd
import argparse
from mongita import MongitaClientDisk
from mongita.database import Database
from mongita.collection import Collection
from bson import ObjectId, InvalidBSON

aparser= argparse.ArgumentParser()
aparser.add_argument("db_path")
aparser.add_argument("db_name")
aparser.add_argument("output_name")
args = aparser.parse_args()

db_client = MongitaClientDisk(args.db_path)
db: Database = eval(f"db_client.{args.db_name}")
print(f"{db.name}, {db.list_collection_names()}")

def extract_all_data(coll_name: str) -> pd.DataFrame:
    coll: Collection = eval(f"db.{coll_name}")
    success = True
    data = []
    last_time = 0
    while success:
        try:
            d = coll.find_one({"time": {"$gt": last_time}})
            if d:
                print(".", end=" ")
                last_time = d["time"]
                data.append(d)
            else:
                success = False
        except Exception as e:
            print(f"Failed with {type(e)}{e}")
            success = False

    return pd.DataFrame(data)

master_data = pd.DataFrame([])
for coll in db.list_collection_names():
    print(coll)
    d = extract_all_data(coll)
    print(d.dtypes)
    print(d)
    master_data = pd.concat([master_data, d], axis=1)

print(master_data)