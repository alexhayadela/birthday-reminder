from supabase import create_client, Client

from src.config import Config

def supabase_client() -> Client:
    """Returns a supabase client."""
    url = os.environ["SUPABASE_URL"]
    key = os.environ
    