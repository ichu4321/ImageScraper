

# keeps a hashed list of images that it has seen
class Hasher:
	def __init__(self, method):
		self.hashes = {};
		self.hash_func = method;

	# checks image and adds to hash list
	def addImage(self, img):
		# get hash
		hashval = self.hash_func(img);
		if hashval is None:
			print("Hashval is None");
			return False;

		# check
		if hashval in self.hashes:
			return False;
		self.hashes[hashval] = 0;
		return True;

