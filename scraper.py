from sanitizer import Hasher
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import cv2
import time
import requests
import numpy as np

# scrapes images from target search line
class Scraper:
	def __init__(self, hash_method, save_duplicates = False):
		self.hash = Hasher(hash_method);
		self.save_dupes = save_duplicates;

		# set up the webdriver
		options = Options();
		options.headless = True;
		self.driver = webdriver.Chrome(executable_path = "./chromedriver", options = options);

		# fetch the base website
		base_url = "https://www.google.com/search?q=blank&hl=en&tbm=isch&sxsrf=AOaemvI9Ag6jsCZxasqEb-MWntRX1cHMMA%3A1642522578172&source=hp&biw=740&bih=760&ei=0ufmYZCYB9ykytMPwMGr4Aw&iflsig=ALs-wAMAAAAAYeb14sr4FIfmSahS9OPO6_92P7kda5Cx&ved=0ahUKEwiQybe22bv1AhVcknIEHcDgCswQ4dUDCAY&uact=5&oq=blank&gs_lcp=CgNpbWcQAzILCAAQgAQQsQMQgwEyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyBQgAEIAEMggIABCABBCxAzIICAAQgAQQsQMyBQgAEIAEMggIABCABBCxAzIICAAQgAQQsQM6CggjEO8DEOoCECc6CAgAELEDEIMBULAeWO0gYJIiaAJwAHgAgAFGiAHqAZIBATWYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img";
		self.driver.get(base_url);
		self.driver.implicitly_wait(3.0);

		# save incrementally into folder
		self.filenum = 0;

	# just quits the webdriver
	def close(self):
		self.driver.quit();

	# returns all non-duplicate images found with term
	# WARNING:
	# if max_image_limit isn't specified, this will grab as many as possible
	def getImages(self, search_term, max_image_limit = -1):
		# grab the search bar
		bars = self.driver.find_elements_by_tag_name("input");
		bar = None;
		for elem in bars:
			# check by type
			elem_type = elem.get_attribute("type");
			if elem_type is not None and elem_type == "text":
				bar = elem;

		# enter in the search term
		bar.clear();
		bar.send_keys(search_term);
		bar.send_keys(Keys.ENTER);

		# wait for page to load
		time.sleep(1.0);

		# scroll to end
		while self.scrollDown():
			time.sleep(0.15);

		# click on all images (this causes the source url to load)
		self.clickImages(max_image_limit);
		time.sleep(1.0);

	# clicks on all id'ed images on page
	def clickImages(self, max_size):
		# clickable ids
		click_id = ".bRMDJf.islir";

		# find each element with this id
		clickables = self.driver.find_elements_by_css_selector(click_id);
		if len(clickables) > max_size and max_size != -1:
			clickables = clickables[:max_size];
		print("Found " + str(len(clickables)) + " Items");

		# click on each element
		index = 1;
		for click in clickables:
			print(str(index) + " of " + str(len(clickables)));
			index += 1;
			self.retrieveImage(click);


	# attempts to scroll down
	def scrollDown(self):
		# count number of images before
		prev_count = len(self.driver.find_elements_by_tag_name("img"));

		# try to scroll
		scroll_num = 5;
		for a in range(scroll_num):
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(0.15);

		# check if the buttons have show up

		# click on the "see more" button
		self.clickButton("r0zKGf");

		# click on "show more" button
		self.clickButton("mye4qd");

		# check after count (see if there are any more images)
		post_count = len(self.driver.find_elements_by_tag_name("img"));
		return post_count != prev_count;

	# attempts to click a button with matching class name
	def clickButton(self, name):
		# set lower wait time
		self.driver.implicitly_wait(0.2);

		# get list of buttons and click on first
		buttons = self.driver.find_elements_by_class_name(name);
		if len(buttons):
			button = buttons[0];
			if button.is_displayed():
				button.click();
				time.sleep(1.0);

		# reset wait time
		self.driver.implicitly_wait(1.0);

	# click on the thumbnail to get the original image to reveal
	def retrieveImage(self, elem):
		# click on the element
		self.driver.execute_script("arguments[0].click();", elem);
		time.sleep(1.0);

		# grab the image element
		imgsrc = None;
		images = self.driver.find_elements_by_class_name("n3VNCb");
		for image in images:
			src = image.get_attribute("src");
			# print("Source: " + src[:100]); # DEBUG DEBUG DEBUG
			if src is not None and src.find("data:image") == -1 and src.find("encrypted-tbn0.gstatic") == -1:
				imgsrc = image;
		if imgsrc is None:
			print("Image Source Invalid");
			return;

		# convert to url
		url = self.getURL(imgsrc);
		if url is None:
			print("URL Invalid");
			return;

		# pull the image
		img = self.getCvImage(url);
		if img is None:
			print("Image Invalid");
			return;

		# run the image through the hasher
		if self.hash.addImage(img):
			self.saveImage(img, "Images/");
		else:
			print("Image is a duplicate");
			if self.save_dupes:
				self.saveImage(img, "Duplicates/");

	# retrieve opencv image from url
	def getCvImage(self, url):
		# get and convert image
		user = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"};
		try:
			page = requests.get(url, stream=True, timeout = 1.0, headers = user).raw;
			img = np.asarray(bytearray(page.read()), dtype = np.uint8);
			img = cv2.imdecode(img, cv2.IMREAD_COLOR);
			return img;
		except Exception as e:
			print("GET Error: " + str(e));
			return None;

	# save image
	def saveImage(self, img, folder):
		filename = str(self.filenum).zfill(6) + ".png";
		print("Saving " + filename);
		self.filenum += 1;
		cv2.imwrite(folder + filename, img);

	# converts web element into sanitized url
	def getURL(self, element):
		# set up filetype whitelist
		whitelist = [".jpeg", ".jpg", ".png"];

		# pull the url
		src = element.get_attribute("src");

		# find the filetype
		filetype = None;
		period = src.rfind(".");
		question = src.rfind("?");
		if period < question:
			filetype = src[period:question];
		else:
			filetype = src[period:];

		# check against whitelist and return
		if filetype in whitelist:
			return src;
		return None;
