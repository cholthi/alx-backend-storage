#!/usr/bin/env python3
""" Provides a function that queries a colllection for a docment"""


def schools_by_topic(mongo_collection, topic):
    """ Returns the list of school having a specific topic"""
    schools = mongo_collection.find({"topics": {
        "$in": [topic]}})
    return schools
