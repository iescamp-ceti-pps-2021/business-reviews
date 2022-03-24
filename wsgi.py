import os

# from app import cli  # noqa: F401
from app import create_app
from app.config import app_config

env = os.environ.get("APP_CONFIG_ENV") or "development"
app = create_app(app_config[env], instance_relative_config=True)

if __name__ == "__main__":
    app.run()
