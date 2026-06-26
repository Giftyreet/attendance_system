from db import db, students_collection

print("Database:", db.name)
print("Collection:", students_collection.name)
print("Document count:", students_collection.count_documents({}))

for doc in students_collection.find():
    print(doc)