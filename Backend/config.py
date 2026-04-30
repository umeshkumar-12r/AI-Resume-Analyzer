import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
SKILLS_FILE = os.path.join(BASE_DIR, "data", "skills.txt")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Flask settings
DEBUG = True
SECRET_KEY = "supersecretkey"

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf"}