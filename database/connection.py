import streamlit as st
import os

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and return Supabase client using Streamlit Secrets."""
    try:
        # First check Streamlit secrets
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["URL"]
            key = st.secrets["supabase"]["KEY"]
        else:
            # Fallback to environment variables for potential local dev outside Streamlit
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
        if not url or not key:
            raise ValueError("Supabase credentials not found in secrets.toml or environment variables.")
            
        return create_client(url, key)
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return None
