import cx_Oracle
import datetime

class DataHandler:

    cursor = None
    title = ''

    def __init__(self, title):
        self.title = title

    def store(self, filename, info, skills):
        name, email, phone, address, website, page = info
        exact_match, partial_match, num_keyword = skills







