#!/usr/bin/env python3
""" Updates a collection document based on a criteria"""


def update_topics(mongo_collection, name, topics):
    """Updates a document to add a topics array"""
    mongo_collection.update_many({"name": name}, { "$set":
        {"topics" : topics}})
