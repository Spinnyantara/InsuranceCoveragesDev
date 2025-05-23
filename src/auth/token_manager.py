import requests
import os
import json


class TokenManager:
    TOKEN_FILE = "token.json"
    BASE_URL = "https://api-dev.spinnyinsurance.com/sp-insurance-platform/api/v1/accounts"

    @classmethod
    def get_token(cls):
        if os.path.exists(cls.TOKEN_FILE):
            with open(cls.TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                return token_data.get("access_token")

        # Login and save token if file not found
        return cls.login_and_save_token()

    @classmethod
    def login_and_save_token(cls):
        phone = "7620954854"

        # ✅ SEND OTP FIRST
        print(f"📨 Sending OTP to {phone}...")
        send_resp = requests.post(
            f"{cls.BASE_URL}/otp-request/",
            json={"phone_number": phone},
            headers={"Content-Type": "application/json"}
        )
        send_resp.raise_for_status()
        print("✅ OTP request successful.")

        input("⏳ Check your phone. Press Enter once you've received the OTP.")
        otp = input("🔐 Enter the OTP: ")

        # ✅ VERIFY OTP
        verify_resp = requests.post(
            f"{cls.BASE_URL}/verify-otp/",
            json={"phone_number": phone, "otp": otp},
            headers={"Content-Type": "application/json"}
        )
        verify_resp.raise_for_status()

        token = verify_resp.json().get("access_token")

        with open(cls.TOKEN_FILE, "w") as file:
            json.dump({"access_token": token}, file)

        print("✅ Token saved to token.json.")
        return token


