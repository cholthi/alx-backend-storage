#!/usr/bin/env python3
""" Lists documents in mongodb collection"""


def list_all(mongo_collection):
    """ retrives all document in a collection"""
    return mongo_collection.find()
