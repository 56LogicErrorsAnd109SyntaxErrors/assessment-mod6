import json
import os
from dotenv import load_dotenv

class ToDoList:
    def __init__(self):
        LAMBDA_API_URL = os.getenv("LAMBDA_API_URL")

    