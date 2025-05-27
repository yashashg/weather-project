import getpass
import os
try:
    # load environment variables from .env file (requires `python-dotenv`)
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

os.environ["LANGSMITH_TRACING"] = "true"
if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
        prompt="Enter your LangSmith API key (optional): "
    )
else:
   LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
   
if "LANGSMITH_PROJECT" not in os.environ:
    os.environ["LANGSMITH_PROJECT"] = getpass.getpass(
        prompt='Enter your LangSmith Project Name (default = "default"): '
    )
    if not os.environ.get("LANGSMITH_PROJECT"):
        os.environ["LANGSMITH_PROJECT"] = "default"
else:
   LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT")


if not os.environ.get("MISTRAL_API_KEY"):
  os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")
else:
   MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")


if not os.environ.get("WEATHER_API"):
  os.environ["WEATHER_API"] = getpass.getpass("Enter API key for WEATHER_API : ")
else:
   WEATHER_API = os.environ.get("WEATHER_API")
if not os.environ.get("WEATHER_API_URL"):
  os.environ["WEATHER_API_URL"] = getpass.getpass("Enter WEATHER_API_URL : ")
else:
   WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
