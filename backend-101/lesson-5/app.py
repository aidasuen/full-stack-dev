import os 
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('API_KEY')
debug_mode = os.environ.get('DEBUG_MODE')

# Выводим значения переменных
print(f"API Key: {api_key}")
print(f"Debug Mode: {debug_mode}")
