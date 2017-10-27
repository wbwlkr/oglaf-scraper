#!/usr/bin/env python3

"""
Title : Oglaf Scraper
Author : wbwlkr.github.io
Description :
Scrap all the oglaf strips / Get an update / Get the number of stories
"""

from time import time
from bs4 import BeautifulSoup
import re, sys, os.path, requests, wget
from natsort import natsorted

# == Main Class ==

class Webcomic:
	def __init__(self):
		self.site = 'http://oglaf.com'
		self.start_uri = '/cumsprite/'
		self.scrap_folder = 'strips_oglaf'
		self.strip_counter = 1
		self.beautiful_scrap = None
		self.script_path = os.path.split(os.path.realpath(__file__))[0]
		self.scrap_path = os.path.join(self.script_path, self.scrap_folder)

	def count_stories(self):
		"""
		Count all the stories in the archive page."""

		r_page = requests.get(self.site + '/archive/')
		self.beautiful_scrap = BeautifulSoup(r_page.text, 'lxml')
		stories = self.beautiful_scrap.select('body div > div > div > a > img')

		if len(stories) > 0:
			print('There is %d stories.' % (len(stories)))
		else:
			print('Scraping impossible : the website structure has changed.')

	def scrap(self):
		"""
		Start the scrapping scenario,
		From the last downloaded strip or from the beginning."""

		if os.path.exists(self.scrap_path):
			self.from_last()
		else:
			self.from_start()

	def from_last(self):
		"""
		Scrap from the last strip downloaded in the comic_folder"""

		cleaned_dir = self.clean_folder()

		if not os.listdir(self.scrap_path):
			self.get_strip(self.start_uri)
		else:
			if cleaned_dir:
				next_uri = self.get_next_uri(cleaned_dir[-1])
				if next_uri:
					self.get_strip(next_uri)
				else:
					return False
			else:
				return False

	def clean_folder(self):
		"""
		Delete the failed downloads and return a clean list of files"""

		folder_has_been_cleaned = False
		forbidden_list = (".tmp", "(", ")")
		strips_before = sorted(os.listdir(self.scrap_path))

		for strip in strips_before:
			if any(forbidden in strip for forbidden in forbidden_list):
				os.remove(os.path.join(self.scrap_path, strip))
				folder_has_been_cleaned = True

		# list the files + sort them with the counter number in each filename
		strips_after = natsorted(os.listdir(self.scrap_path))

		if folder_has_been_cleaned and len(strips_before) == len(strips_after):
			print("Problem occured while cleaning the strips folder :")
			print("Please check", self.scrap_path)
			return False
		else:
			return strips_after

	def get_next_uri(self, last_file):
		"""
		Find the uri of the next strip from the name of the last download"""

		last_strip_uri = self.find_uri(last_file.strip('.jpg'))

		last_page = requests.get(self.site + last_strip_uri)
		self.beautiful_scrap = BeautifulSoup(last_page.text, 'lxml')

		return self.scrap_next_link()

	def find_uri(self, last_strip):
		"""
		Get an uri from the filename"""

		*counter, story_name, episode_nb = last_strip.split('_')
		self.strip_counter = int(counter[0]) + 1

		if int(episode_nb) == 1:
			episode_nb = ''

		return "/" + story_name + "/" + episode_nb

	def from_start(self):
		"""
		Scrap from the start url, the beginning of the comic"""

		# create the strips folder, where the webcomic will be download
		if os.mkdir(self.scrap_path) is None:
			self.get_strip(self.start_uri)
		else:
			print("Problem occured while creating the strips folder :")
			print(self.scrap_path)

	def get_strip(self, uri):
		"""
		Scrap the image's strip from its uri."""
		print("\n>> %s" % uri)

		# find the strip pic url
		r_page = requests.get(self.site + uri)
		self.beautiful_scrap = BeautifulSoup(r_page.text, 'lxml')

		strip_pic = self.beautiful_scrap.find("img", id="strip")
		if strip_pic:
			strip_pic_url = strip_pic.get('src')
		else:
			print("The strip's image can't be downloaded.")

		# download the strip
		try:
			if not self.download(strip_pic_url, uri.strip("/").split('/')):
				print('The download of the strip named %s has failed' % newpic_filename)
		except:
			raise

		# scrap the uri of the next link
		next_strip = self.scrap_next_link()
		# continue the scraping scenario or finish it
		if next_strip:
			return self.get_strip(next_strip)
		else:
			"That was last strip."

	def scrap_next_link(self):
		"""
		Scrap the next uri from the beautiful_scrap content"""
		try:
			return self.beautiful_scrap.find('div', id="nx").findParent('a').get('href')
		except AttributeError:
			return None

	def download(self, pic_url, story_ep):
		"""
		Download the file from a given url
		And save it with the related strip counter_story_ep.jpg name"""

		try:
			if len(story_ep) > 2:
				raise ValueError
			if len(story_ep) == 1:
				story_ep.append('1')

			story, ep = story_ep
			pic_name = '_'.join((str(self.strip_counter), story, ep)) + '.jpg'
			pic_path = os.path.join(self.scrap_path, pic_name)
			wget.download(pic_url, pic_path)

			self.strip_counter += 1
			return pic_name if os.path.exists(pic_path) else False

		except Exception as e:
				raise e

# == Functions ==

def timer(function_to_wrap):
	"""
		Display the elapsed time of the wrapped function"""
	def wrapper_func(*args,**kwargs):
		t_start = time()
		function_processed = function_to_wrap(*args,**kwargs)
		t_end = time()
		if('-t' in sys.argv):
			print("\n" + "(Time elapsed : %s sec)" % round((t_end - t_start),3))
		return function_processed
	return wrapper_func

def display_help():
	"""
		Display description of the script and all its possible commands."""
	sentence = "Oglaf Scraper"
	frameline = (len(sentence) + 4) * "-"

	print(frameline + "\n" + "| " + sentence + " |" + "\n" + frameline)
	print("Download all the comics, Get an update or Get the number of stories")

	print("\n" + 'Commands :')
	print('   -s : ' + 	Webcomic.scrap.__doc__)
	print('   -c : ' +  Webcomic.count_stories.__doc__)
	print('   -t : ' +  timer.__doc__)
	print('   -h : ' + 	display_help.__doc__ + "\n")

@timer
def main():
	oglaf = Webcomic()
	try:
		if(len(sys.argv) == 1 or '-h' in sys.argv):
			display_help()

		elif('-s' in sys.argv):
			print("Scraping started...")
			oglaf.scrap()
			print("Scraping finished.")
			print("Read the strips in %s/" % os.path.relpath(oglaf.scrap_path))

		elif('-c' in sys.argv):
			print("Counting stories...")
			oglaf.count_stories()

	except KeyboardInterrupt as e:
		print("\n\nThe scraping has been stopped")

if __name__ == '__main__':
	main()
