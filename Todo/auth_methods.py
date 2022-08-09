import hashlib


def convert_to_hash(hash_input):
    hash_output = hashlib.sha3_512(str(hash_input).encode('utf-8'))
    return hash_output.hexdigest()
