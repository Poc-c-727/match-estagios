import uuid

import shortuuid


def generate_uuid():
    return str(uuid.uuid4())


def generate_short_uuid():
    return shortuuid.uuid()
