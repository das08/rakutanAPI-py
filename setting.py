import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_ip = os.environ.get("db_ip")
db_username = os.environ.get("db_username")
db_pass = os.environ.get("db_pass")
db_name = os.environ.get("db_name")
db_collection = os.environ.get("db_collection")
line_admin_uid = os.environ.get("line_admin_uid")
line_access_token = os.environ.get("line_access_token")
line_secret_token = os.environ.get("line_secret_token")
