"""
file		: exceptions.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Mon 16 Dec 2019 08:24:53 PM CST
last update	: 

This file defined some exceptions associated to these algorithms
"""

# Exceptions
class AlgoError(Exception):
    pass

class AlgoNoFileError(AlgoError):
    def __init__(self, message=''):
        print('no file inputed!')
        print(message)

class AlgoPartDuplicatedError(AlgoError):
    def __init__(self, message=''):
        print('duplicatedly partionning a graph!')
        print(message)

class AlgoNoNodeInPartitionsError(AlgoError):
    def __init__(self, message=''):
        print('no node in graph.partitions[0]!')
        print(message)
