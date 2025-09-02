import os, requests
from bs4 import BeautifulSoup

# Credentials from GitHub Secrets
USERNAME = os.getenv("PROGRESS_USER")
PASSWORD = os.getenv("PROGRESS_PASS")

LOGIN_URL = "https://v4.progresscenter.io/login"
CAMERA_URL = "https://v4.progresscenter.io/projects/21187/cameras/91000354"  # replace with your camera link

session = requests.Session()

# 1. Login
session.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})

# 2. Get camera page
r = session.get(CAMERA_URL)
r.raise_for_status()

# 3. Parse latest image URL
soup = BeautifulSoup(r.text, "html.parser")
img_tag = soup.find("img", {"class": "w-full"})
if not img_tag:
    raise RuntimeError("No progress image found!")

img_url = img_tag["src"]

# 4. Download image
img = session.get(img_url)
img.raise_for_status()

# 5. Save as /photos/today.jpg
os.makedirs("photos", exist_ok=True)
with open("photos/today.jpg", "wb") as f:
    f.write(img.content)

print("Downloaded latest photo as today.jpg")
