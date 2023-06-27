import dotenv


def load_env():
    """Load .env file"""
    try:
        dotenv.load_dotenv()
    except Exception as err:
        print(err)
        raise
