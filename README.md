# ImageScraper
Scrapes full-sized images from google while filtering out duplicates

# Installing the Environment
This repo should work for all Python 3.7 or greater.
If you need to install multiple Python versions then use Anaconda3 (for Windows) or pyenv (for Linux and Mac).

Using a fresh virtual environment ("conda create" or "venv") run "pip install requirements.txt" while in the repo folder.

You will need to download a chromdriver (https://chromedriver.chromium.org/downloads) and place the executable "chromedriver.exe" into the repo folder. This repo was tested using Chrome version 99. 

# Directions for use
Edit the "search_terms" list in the main.py program and run it.

The images will be saved into the Images folder.

# Tweakable Options

This program hashes images in order to compare them quickly for duplicates. 

There are various image hashing functions in the hashes.py file to choose from and of course any function that takes an image and returns a string can be used.  

The fast hashing function that is used by main.py will suffice for most practical needs (I still haven't seen it ever disagree with the very slow, full image comparison method).
