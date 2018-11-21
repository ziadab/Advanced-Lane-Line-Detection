import os
from PIL import Image

i = 0
for root, dirs, files in os.walk("C:\\Users\\Ziad\\Desktop\\Projects\\MyOwnLineDetection\\Cheseboard"):
	for file in files:
		full_path = os.path.abspath(os.path.join(root,file))
		img = Image.open(full_path)
		img = img.resize((2000,1000), Image.ANTIALIAS)
		img.save("compressed"+str(i)+".jpg", optimize=True, quality=95)
		i+=1