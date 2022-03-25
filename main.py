import hashes
from scraper import Scraper


if __name__ == "__main__":
	# list of search terms
	MAX_IMAGES_PER_TERM = 200;
	search_terms = [
	"grass",
	"field",
	"lawn",
	"yard"
	]

	# set up the scraper with the fast duplication check
	webscraper = Scraper(hashes.fastHash, save_duplicates = True);

	# scrape images
	for term in search_tersm:
		webscraper.getImages(term, MAX_IMAGES_PER_TERM);
