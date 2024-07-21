import os
import ascon
import time
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# import tweepy
# from dotenv import load_dotenv
# load_dotenv()

root_directory = "Snapshort"
record_directory = "Publish_Part_1"
immutable_directory = "Publish_Part_2"

# Load the private key
with open("private.pem", "rb") as key_file:
    private_key_pem = key_file.read()

private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

# def tweet():
#     consumer_key = ""
#     consumer_secret = ""
#     access_token = ""
#     access_token_secret = ""
#     auth = tweepy.OAuth1UserHandler(
#         consumer_key, consumer_secret, access_token, access_token_secret
#     )
#     api = tweepy.API(auth)
#     api.update_status(data)


def calculate_hash(filepath):
    data_bytes = bytearray()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)  
            if not data:
                break
            data_bytes.extend(data)
        
    return ascon.ascon_hash(message=data_bytes,variant="Ascon-Hash", hashlength=32)

def recursive_hash(path):
        print("Current Path : ",path)
        if os.path.isfile(path):
            return calculate_hash(path)
        elif os.path.isdir(path):
            hashes = [recursive_hash(os.path.join(path, child)) for child in sorted(os.listdir(path))]
            return ascon.ascon_hash(message=(b"".join(hashes)),variant="Ascon-Hash", hashlength=32)
        else:
            raise ValueError(f"Invalid path: {path}")

def merkle_tree_hash(directory):
    if not os.path.isdir(directory):
        raise ValueError("Invalid directory path.")
    root_hash = recursive_hash(directory)
    return root_hash

def check_folder_records(directory):
    files_list = [entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    if files_list:
        return sorted(files_list, reverse=True)[0]
    else:
        return False

root_hash = merkle_tree_hash(root_directory)
print(f"Merkle Tree Hash of {root_directory}: {root_hash}")
unix_timestamp = int(time.time())
if check_folder_records(record_directory) is not False:
    file = check_folder_records(record_directory)
    filepath = os.path.join(record_directory,file )
    data = None
    with open(filepath, 'rb') as f:
        data = f.read()
    f.close()
    print("Existing Latest File :",file)
    print("Existing Latest Hash :",data)
    ascon_hash = ascon.ascon_hash(message=(root_hash+data),variant="Ascon-Hash", hashlength=32)
    print(str(ascon_hash))
    file_with_ext = file.split(".")[0]
    next_file = int(file_with_ext.split("_")[1]) + 1
    filepath = os.path.join(record_directory, "H_"+str(next_file)+".txt")
    with open(filepath, 'w') as f:
        f.write(str(ascon_hash))
    f.close()
    
    ###### Part 2 ###########
    data_to_sign = f"{ascon_hash}{unix_timestamp}".encode('utf-8')
    signature = private_key.sign(
        data_to_sign,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("=== Signature === ") 
    print(signature.hex()) 
    filepath = os.path.join(immutable_directory,"H_"+str(next_file)+".txt" )
    with open(filepath, 'w') as f:
        f.write(json.dumps({"time":unix_timestamp,"signature":signature.hex()}))
    f.close()
    
else:
    H_initial = bytes.fromhex("0"*64)
    ascon_hash = ascon.ascon_hash(message=(root_hash+H_initial),variant="Ascon-Hash", hashlength=32)
    print("Initial Hash - H1")
    ## Insert Hash Record 
    print(str(ascon_hash))
    filepath = os.path.join(record_directory,'H_1.txt' )
    with open(filepath, 'w') as f:
        f.write(str(ascon_hash))
    f.close()
    
    ###### Part 2 ###########
    data_to_sign = f"{ascon_hash}{unix_timestamp}".encode('utf-8')
    signature = private_key.sign(
        data_to_sign,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("=== Signature === ") 
    print(signature.hex())
    filepath = os.path.join(immutable_directory,'H_1.txt' )
    with open(filepath, 'w') as f:
        f.write(json.dumps({"time":unix_timestamp,"signature":signature.hex()}))
    f.close()