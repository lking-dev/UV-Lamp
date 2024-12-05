# Written by Landry M. King, 2024
# Config: handles loading the server and credential configuration JSON files

import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))

        with open(self.path + "\\config\\config.json") as config_file:
            self.config_data = json.load(config_file)

        with open(self.path + "\\config\\credentials.json") as credentials_file:
            self.credentials_data = json.load(credentials_file)

    def getDatabasePath(self):
        return self.path + "\\" + self.config_data["database_file"]
    
    def getHost(self):
        return self.config_data["server_host"]
    
    def getPort(self):
        return self.config_data["server_port"]
    
    def getSendgridCreds(self):
        return (self.credentials_data["sendgrid"]["email"], self.credentials_data["sendgrid"]["api_key"])
    
    def getGoogleCreds(self):
        return self.credentials_data["google"]["api_key"]
    
    def getUATCreds(self):
        return (
            self.credentials_data["uat5"]["username"],
            self.credentials_data["uat5"]["password"],
            self.credentials_data["uat5"]["orodb"],
            self.credentials_data["uat5"]["host"],
            self.credentials_data["uat5"]["port"])