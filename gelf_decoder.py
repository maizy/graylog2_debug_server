# _*_ coding: utf-8 _*_
from __future__ import unicode_literals, absolute_import

import zlib
import json

# GELF spec: http://graylog2.org/gelf#specs

MAGIC = b'\x1e\x0f'


def decompress(compressed_data):
    try:
        result = zlib.decompress(compressed_data)
    except ValueError:
        result = None  # TODO: error handling
    return result

# TODO
# def decode_chunks(chunks):
#     for compressed_data in chunks:
#         data = decompress(compressed_data)
#         print(data)
#         # print(''.join('\\x{0:x}'.format(i if isinstance(i, int) else ord(i)) for i in data))
#         assert data[0:2] == MAGIC


def decode_full(compressed_data):
    try:
        return json.loads(decompress(compressed_data).decode('utf-8'))
    except ValueError:  # TODO: error handling
        return None
