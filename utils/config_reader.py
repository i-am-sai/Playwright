import json # reads json file
import os   # reads env variables
from dotenv import load_dotenv # Loads variables from .env file

load_dotenv() # run once when this file is imported and it loads .env file so every other file can access them

class ConfigReader:
    def __init__(self, path="config/config.json"): # Constructor and runfs config = ConfigReader() automatically when creating and give location of congif file.
        with open(path, encoding="utf-8") as file: #encoding="utf-8" is a good practice for consistent file reading.
            self._config = json.load(file) # converts json to python dict
           # Prefix internal variables with _ (e.g., _config) to indicate they're for internal use.

    def get(self, key): # defining get method to get information from config file
        return self._config[key] # self._config[key] raises an error if the key is missing, which helps catch configuration mistakes early.
    

    @property
    def username(self):
        return os.getenv("TEST_USERNAME")
    
    @property
    def password(self):
        return os.getenv("TEST_PASSWORD")



# Best Practices
# ✅ Call load_dotenv() once at the top.
# ✅ Keep secrets only in .env.
# ✅ Use one ConfigReader for the whole framework.












# import json
# import os
# from dotenv import load_dotenv

# load_dotenv()   # reads .env file and injects its contents into os.environ

# class ConfigReader:
#     def __init__(self, path="config/config.json"):
#         with open(path, "r") as file:
#             self.config = json.load(file)

#     def get(self, key):
#         return self.config.get(key)

#     @property
#     def username(self):
#         return os.environ.get("TEST_USERNAME")

#     @property
#     def password(self):
#         return os.environ.get("TEST_PASSWORD")