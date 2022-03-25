# good enough for 99.99% of images
def fastHash(img):
	# get resolution
	h,w = img.shape[:2];
	h -= 1;
	w -= 1;

	# grid hash pixels
	hashstr = "";
	for dy in range(0,100,10):
		for dx in range(0,100,10):
			y = int((dy / 100.0) * h);
			x = int((dx / 100.0) * w);
			for value in img[y,x]:
				hashstr += str(value).zfill(3);
	return hash(hashstr);

# good enough for 99.99999% of images
def fullGrayHash(img):
	# grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
	hashstr = "";
	h,w = gray.shape[:2];
	for y in range(h):
		for x in range(w):
			hashstr += str(gray[y,x]).zfill(3);
	return hash(hashstr);

# failure isn't an option and someone might be deliberately messing with you
def fullHash(img):
	# do a full, expensive, read
	hashstr = "";
	h,w = img.shape[:2];
	for y in range(h):
		for x in range(w):
			for value in img[y,x]:
				hashstr += str(value).zfill(3);
	return hash(hashstr);

