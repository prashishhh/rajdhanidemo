import pytesseract
from PIL import Image

# Open JPG directly
img = Image.open("ad.jpg")

# OCR with Nepali + English
text = pytesseract.image_to_string(img, lang="nep+eng", config="--oem 1 --psm 4")
print(text)
