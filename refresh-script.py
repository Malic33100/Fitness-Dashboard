import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_refresh_token():

    client_id = os.getenv('STRAVA_CLIENT_ID')

    auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all"

    print("=" * 70)
    print("STEP 1: Visit this URL in your browser:")
    print("=" * 70)
    print(auth_url)
    print("\n")
    print("After authorizing, copy the 'code' from the URL you're redirected to")
    print("It will look like: http://localhost/?code=ABC123...")
    print("=" * 70)

    auth_code = input("\nPaste the authorization code here: ").strip()

    if not auth_code:
        print("No code provided. Exiting")
        return
    

    print("\n" + "=" * 70)
    print("STEP 2: Exchanging code for tokens...")
    print("=" * 70)

    token_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'code': auth_code,
        'grant_type': 'authorization_code'
    }


    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        tokens = response.json()

        print("\n✓ Success! Got your tokens:\n")
        print("Access Token (expires in ~6 hours):")
        print(tokens['access_token'])
        print("\nRefresh Token (use this in .env file):")
        print(tokens['refresh_token'])
        print("\n" + "=" * 70)
        print("Copy the REFRESH TOKEN above and add it to your .env file:")
        print("STRAVA_REFRESH_TOKEN=" + tokens['refresh_token'])
        print("=" * 70)

    except Exception as e:
        print(f"/nx Error: {e}")
        if hasattr(e, 'response'):
            print(e.response.text)

if __name__ == "__main__":
    get_refresh_token()
