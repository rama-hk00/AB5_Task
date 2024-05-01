import re
import requests 
import socket
import sys
import json
import whois
import queue
from bs4 import BeautifulSoup
import os

class SubDomainScan:
	def the_whole_thing(self):
		file1 = open('/root/Desktop/final_codes/domain_wordlist', 'r')
		Lines = file1.readlines()
		###########3
		count = 0 
		for line in Lines:
		    count += 1
		    print("Line{}: {}".format(count, line.strip()))
		###########3
		Domain = input("Please enter a domain: ")

		subdomains = []
		URL = []
		unique_list = []

		for i in Lines:
			subdomains.append(i.replace("\n", ""))

		for i in subdomains:
			URL.append(str(i + "." + Domain))

		for i in URL:
			try:
				result = socket.getaddrinfo(i, None, 0, socket.SOCK_STREAM)
				for item in result:
					if "92.242.129.221" not in item[4]:
						unique_list.append(i)
			except:
				pass
		return unique_list


class WebCrawling:
	def the_whole_thing(self):
		
		#Domain = input ("Please enter a URL (with the protocol (http://)): ")
		print("This code only worked for wizardcyber company :( ..")
		Domain = "https://wizardcyber.com/"
		status_code = "200"
		links = [] #not sure if ill use 
		urls = queue.Queue()
		urls.put(Domain) 
		visited_urls = []
		pattern = ""
		url = []
		final_urls = []
		tested_links = []
		flag = 0

		while not urls.empty():
			current_url = urls.get() # to fetch one url of the list 
			
			for i in tested_links:
				if current_url == i:
					flag = 1
			if flag == 1:
				continue

			tested_links.append(current_url)

			response = requests.get(current_url) # send a request to the current url
			soup = BeautifulSoup(response.content, "html.parser") #choose links
			link_elements = soup.select("a[href]") # choose links

			for link_element in link_elements: # loop around links
				url = link_element['href'] # to choose links only # has all links 

				if re.match(rf"https://(?:.*\.)?wizardcyber\.com", url): 
					urls.put(url) 
					final_urls.append(url)
		for i in final_urls:
			print (i)
		
					

def main():
	sds = SubDomainScan()
	list_subdomains = sds.the_whole_thing()
	for i in list_subdomains:
		print("\t" + i)




	print("Web crawling ")
	wc = WebCrawling()
	wc.the_whole_thing()

