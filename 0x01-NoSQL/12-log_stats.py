#!/usr/bin/env python3
"""provides a funcion  that prints nginx logs in ginx collection"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    logs_count = len(list(nginx_collection.find()))
    get_count = len(list(nginx_collection.find({"method": "GET"})))
    post_count = len(list(nginx_collection.find({"method": "POST"})))
    put_count = len(list(nginx_collection.find({"method": "PUT"})))
    patch_count = len(list(nginx_collection.find({"method": "PATCH"})))
    delete_count = len(list(nginx_collection.find({"method": "DELETE"})))
    status_count = len(list(nginx_collection.find({"path": "/status"})))

    print(f"{logs_count} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_count}")
    print(f"\tmethod POST: {post_count}")
    print(f"\tmethod PUT: {put_count}")
    print(f"\tmethod PATCH: {patch_count}")
    print(f"\tmethod DELETE: {delete_count}")
    print(f"{status_count} status check")
