from src.auth.token_manager import TokenManager


def before_all(context):
    print("🔐 Fetching token...")
    context.token = TokenManager.get_token()
