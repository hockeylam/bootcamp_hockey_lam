import sys,os

def get_key(name, default=None):
    return os.getenv(name, default)