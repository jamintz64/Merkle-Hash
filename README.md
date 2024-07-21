# Merkle-Hash

# Project Overview
This project is a Python script that generates a Merkle tree hash for a given directory, records the hash in a file, and signs the hash with a private key. The script also includes functionality to update the hash record and signature over time.

## Functions
### calculate_hash(filepath)
Calculates the Ascon hash of a file at the given filepath.

### recursive_hash(path)
Recursively calculates the Ascon hash of a directory and its contents.

### merkle_tree_hash(directory)
Calculates the Merkle tree hash of a directory.

### check_folder_records(directory)
Checks for the latest file in a directory and returns its name.

### tweet()
NOT IMPLEMENTED Tweets a message using the Tweepy library.

## Usage
Create a directory structure with the following folders:
Snapshort (root directory)
Publish_Part_1 (record directory)
Publish_Part_2 (immutable directory)
Place the private key file private.pem in the same directory as the script.
Run the script to generate the Merkle tree hash and record it in Publish_Part_1.
The script will also sign the hash with the private key and store the signature in Publish_Part_2.
## Dependencies
ascon library for Ascon hash calculations
cryptography library for private key loading and signing
os library for file system operations
time library for timestamp generation
json library for JSON serialization
tweepy library (not implemented) for Twitter API interactions
dotenv library (not implemented) for environment variable loading
## Files
private.pem (private key file)
script.py (this script)
Publish_Part_1 (directory for hash records)
Publish_Part_2 (directory for signed hashes)
Snapshort (root directory for Merkle tree hash calculation)
