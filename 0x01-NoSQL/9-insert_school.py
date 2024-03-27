#!/usr/bin/env python3
""" Inserts a new document in a school colection"""


def insert_school(mongo_collection, **kwargs):
    """ Inserts one document to a mongo collection """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
