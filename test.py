import hashes
from scraper import Scraper


if __name__ == "__main__":
	# set up the scraper with the fast duplication check
	webscraper = Scraper(hashes.fastHash, save_duplicates = True);

	# scrape images
	webscraper.getImages("rice", 120);
	# webscraper.getImages("yard", 100);

