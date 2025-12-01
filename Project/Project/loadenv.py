import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    migrations_exist = os.path.exists("migrations")

    DB_INIT = os.getenv("DB_INIT")
    DB_MIGRATE = os.getenv("DB_MIGRATE")
    DB_UPGRADE = os.getenv("DB_UPGRADE")

    if not migrations_exist:
        os.system(DB_INIT)

    os.system(DB_MIGRATE)
    os.system(DB_UPGRADE)
