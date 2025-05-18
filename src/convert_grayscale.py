from PIL import Image

img = Image.open("../images/test.png").convert("L")
img.save("../images/test_gray.png")
 