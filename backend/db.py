import os
from pymongo import MongoClient
import certifi


MONGO_URI = "mongodb://reetsahu:REETSAHU@ac-em9d1cr-shard-00-00.eweiu8z.mongodb.net:27017,ac-em9d1cr-shard-00-01.eweiu8z.mongodb.net:27017,ac-em9d1cr-shard-00-02.eweiu8z.mongodb.net:27017/?ssl=true&replicaSet=atlas-9hm44p-shard-0&authSource=admin&appName=AttendaceCluster"
DB_NAME = os.getenv("DB_NAME", "attendance_system")


def get_client() -> MongoClient:
    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set. Add it to your environment.")

    return MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where()
    )


def get_db():
    client = get_client()
    return client[DB_NAME]


db = get_db()

students_collection = db["students"]

attendance_collection = db["attendance"]

teachers_collection = db["teachers"]

teacher_assignments_collection = db["teacher_assignments"]

attendance_stats_collection = db["attendance_stats"] 
