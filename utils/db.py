import pymongo
import json

from utils import aws
from bson import json_util

'''
* name : get_db_connection 
* desc :function is designed to establish db connection
* return : connection details
'''
def get_db_connection(secret_details : dict,table_name : str):
    client = pymongo.MongoClient(secret_details['client'])
    mongo_db = client[secret_details['name']]
    mongo_collection = mongo_db[table_name]
    return mongo_collection

'''
* name : get_next_sequence_value
* desc : function is designed to generate unique sequence values in ascending order for a specified collection within a database
* input : sequence name -> string
* return : generated unique sequence value -> string
'''
def get_next_sequence_value(sequence_name):
    secret_details = aws.get_secret_details()
    sequence_doc = get_db_connection(secret_details['mongo_database'], 'sequence').find_one_and_update(
        {"name": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,  
        return_document=True
    )
    return sequence_doc["value"]

'''
* name : get_all_details
* desc : function is specifically crafted to retrieve all stored records within a designated collection of a database. Utilizing a projection technique, it fetches all details excluding the unique object identifiers, providing a comprehensive view of the stored data within the specified collection
* input : collection name -> string
* return : stored records -> list of dict's
'''
def get_all_details(table_name : str):
    secret_details = aws.get_secret_details()
    cursor = get_db_connection(secret_details['mongo_database'],table_name).aggregate([{"$project": {"_id": 0}} ])
    result_list = [doc for doc in cursor]
    return result_list

'''
* name : get_details_with_filter
* desc : function is specifically crafted to retrieve all stored record values for a designated collection within a database. It employs projection techniques to exclude the unique Object ID field, providing a comprehensive set of details for each record. Additionally, the function supports the inclusion of a search dictionary, allowing for filtered results based on specified criteria
* input : collection name -> string , search string -> dict ({"name": "Tanvi Shah"})
* return : filtered stored records -> list of dict's
* note : This function ensures a precise match between the provided search string and the required data types in the database. In cases where the search criteria differ from the expected string type, the function performs a type cast to harmonize the input. This guarantees consistent and accurate results by adapting the search parameters to the expected data types in the database 
'''
def get_details_with_filter(table_name : str,search_string : dict):
    secret_details = aws.get_secret_details()
    cursor = get_db_connection(secret_details['mongo_database'],table_name).aggregate([{"$match": search_string},{"$project": {"_id": 0}} ])
    result_list = [doc for doc in cursor]
    return result_list

'''
* name : update_record
* desc : function is specifically crafted to update record against provided collection name and against provided specific record
* input : collection name -> string , search string -> dict ({"otterz_id": "123..."}), record set -> dict(which need to update)
'''
def update_record(table_name : str,search_string : dict,record_to_update : dict):
    secret_details = aws.get_secret_details()
    get_db_connection(secret_details['mongo_database'], table_name).update_one(search_string, {"$set": record_to_update})

'''
* name : insert_record
* desc : function is specifically crafted to insert record against provided collection name and against provided specific record
* input : collection name -> string , record set -> dict(which need to insert)
'''
def insert_record(table_name : str,record_to_insert : dict):
    secret_details = aws.get_secret_details()
    record_details_json = json.loads(json_util.dumps(record_to_insert))
    get_db_connection(secret_details['mongo_database'],table_name).insert_one(record_details_json)


'''
* name : delete_record
* desc : function is specifically crafted to delete record against provided collection name and against provided specific record
* input : collection name -> string , record set -> dict(which need to delete)
'''
def delete_record(table_name : str,record_to_insert : dict):
    secret_details = aws.get_secret_details()
    record_details_json = json.loads(json_util.dumps(record_to_insert))
    get_db_connection(secret_details['mongo_database'],table_name).delete_one(record_details_json)


'''
* name : delete_many_records
* desc : function is specifically crafted to delete record against provided collection name and against provided specific record
* input : collection name -> string , record set -> dict(which need to delete)
'''
def delete_many_records(table_name : str,record_to_insert : dict):
    secret_details = aws.get_secret_details()
    record_details_json = json.loads(json_util.dumps(record_to_insert))
    get_db_connection(secret_details['mongo_database'],table_name).delete_many(record_details_json)

