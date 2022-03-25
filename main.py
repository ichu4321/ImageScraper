import hashes
from scraper import Scraper


if __name__ == "__main__":
	# list of search terms
	search_terms = [
	"grass",
	"field",
	"lawn",
	"yard"
	]

	# number of images to check per term
	MAX_IMAGES_PER_TERM = 200; 
	# I wouldn't recommend increasing this, the images get unrelated very quickly after this

	# set up the scraper with the fast duplication check
	webscraper = Scraper(hashes.fastHash, save_duplicates = False);

	# scrape images
	for term in search_terms:
		webscraper.getImages(term, MAX_IMAGES_PER_TERM);
