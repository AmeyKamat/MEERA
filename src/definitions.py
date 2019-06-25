import os

IP_ADDR = "0.0.0.0"
PORT = 8000

PROJECT_DIR = os.getcwd()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = 'nlp/models'
ABS_MODELS_DIR = os.path.join(ROOT_DIR, MODELS_DIR)

PLUGINS_DIR = 'plugins'
ABS_PLUGINS_DIR = os.path.join(ROOT_DIR, PLUGINS_DIR)
