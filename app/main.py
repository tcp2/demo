import os
from app.libs.pygologin.gologin import GoLogin

def start():
    gl = GoLogin(
        {
            "token": os.environ.get("TOKEN"),
            "profile_id": os.environ.get("PROFILE_ID"),
            "local": True,
            "credentials_enable_service": False,
        }
    )
    gl.start()


if __name__ == "__main__":
    start()
