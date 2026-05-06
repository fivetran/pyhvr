"""Module docstring text"""
__version__ = "6.1.0.3"
from pyhvr.pyhvr_client import Client


def client(username, password, uri):
    return Client(username=username, password=password, uri=uri, setup_mode=False)


def client_setup_mode(uri):
    return Client(uri=uri, setup_mode=True)
