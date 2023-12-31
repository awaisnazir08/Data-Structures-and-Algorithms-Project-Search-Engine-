import hashlib

text_data = "This is a sample text."
#testing
md5_checksum = hashlib.md5(text_data.encode()).hexdigest()
print("MD5 Checksum:", md5_checksum)

url_checksums_docids = [
    {"checksum": "url_checksum_1", "docID": 1},
    {"checksum": "url_checksum_2", "docID": 2}
]

url_checksum_to_find = "url_checksum_2"

# Binary search implementation to find the docID
left, right = 0, len(url_checksums_docids) - 1
while left <= right:
    mid = (left + right) // 2
    if url_checksums_docids[mid]["checksum"] == url_checksum_to_find:
        print("Found! DocID:", url_checksums_docids[mid]["docID"])
        break
    elif url_checksums_docids[mid]["checksum"] < url_checksum_to_find:
        left = mid + 1
    else:
        right = mid - 1
else:
    print("URL checksum not found in the file")

import hashlib
import sys
url = "https://21stcenturywire.com/2022/01/01/the-best-babylon-bee-sketches-of-2021/"

def generate_document_id(url):
    sha256_hash = hashlib.blake2s(url.encode()).hexdigest()
    return sha256_hash
a = 3
document_id = generate_document_id(url)
print(sys.getsizeof(url))
print(document_id)
