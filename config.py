import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "masmkdy2fnjSGJSCas$258748nfasuu")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "db_ikhsan")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/images")
