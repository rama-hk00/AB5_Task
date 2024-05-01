import re
import requests 
import socket
import sys
from bs4 import BeautifulSoup
import os
import time


class Azure_Account:
	def __init__(self, domain):
		self.domain = domain

	def permutations_wordlist(self):
		permutations_wordlist = open('/root/Desktop/final_codes/AzureCodeFiles/permutations.txt', 'r').read().splitlines()
		return permutations_wordlist

	def containers_wordlist(self):
		containers_wordlist = open('/root/Desktop/final_codes/AzureCodeFiles/containers.txt', 'r').read().splitlines()
		return containers_wordlist

	def bruteforce_wordlist(self): 
		protocol = "https://"
		service_name = ".blob.core.windows.net"
		permWords = self.permutations_wordlist()

		file = open('/root/Desktop/final_codes/AzureCodeFiles/bruteforceWordlist.txt', 'w')
		file.write(protocol + str(self.domain) + service_name + "\n")
		file.close()

		file = open('/root/Desktop/final_codes/AzureCodeFiles/bruteforceWordlist.txt', 'a')
		for p in permWords:
			file.write(protocol + p + str(self.domain) + service_name + "\n")
		for p in permWords:
			file.write(protocol + p + str(self.domain) + p + service_name + "\n")
		for p in permWords:
			file.write(protocol + str(self.domain) + p + service_name + "\n")
		for p in permWords:
			file.write(protocol + p + p + str(self.domain) + service_name + "\n")
		for p in permWords:
			file.write(protocol + str(self.domain) + p + p + service_name + "\n")
		file.close()

	def SABF(self):
		#prepare the wordlist for bruteforcing
		self.bruteforce_wordlist()
		SABF_wordlist = open('/root/Desktop/final_codes/AzureCodeFiles/bruteforceWordlist.txt', 'r').read().splitlines()

		VASA = [] # wordlist of valid urls
		for url in SABF_wordlist:
			try:
				response = requests.get(url, timeout = 0.5)
			except Exception as e:
				if "Caused by ConnectTimeoutError" in str(e):
					continue
			VASA.append(url)
		with open('/root/Desktop/final_codes/AzureCodeFiles/storage_accounts.txt', 'w') as storage_file:
			for account in VASA:
				storage_file.write(account + '\n')

		for v in VASA:
			print(f"account: {v}")

	def CNBF(self):
		storage_accounts = open('/root/Desktop/final_codes/AzureCodeFiles/storage_accounts.txt', 'r').read().splitlines()
		cntWords = self.containers_wordlist()
		parameters = "?restype=container&comp=list"

		CNTs = [] #wordlist for valid containers
		for st in storage_accounts:
			for cnw in cntWords:
				url = st + "/" + cnw + parameters
				try:
					response = requests.get(url, timeout = 0.5)
					if "200" in str(response.status_code):
						CNTs.append(url)
				except Exception as e:
					if "Read timed out." in str(e):
						continue
			with open('/root/Desktop/final_codes/AzureCodeFiles/containers_found.txt', 'w') as storage_file:
				for account in CNTs:
					storage_file.write(account + '\n')

			for c in CNTs:
				print(f"containers: {c}")

	def parsing_urls(self):
		containers = open('/root/Desktop/final_codes/AzureCodeFiles/containers_found.txt', 'r').read().splitlines()
		matched_urls = []
		urls_list = [] # to save URLS without the ? 
		for url in containers:
			url_parts = url.split('?')
			urls_list.append(url_parts[0])
		for url, base_url in zip(containers, urls_list):
			pattern = rf"<Url>\s*({base_url}/[^\s]+)\s*</Url>" 
			try:
				response = requests.get(url)
				matches = re.findall(pattern, response.text)
				
			except:
				print("error ...")
			for i in matches:
				print ('\t' + str(i))

class AWS_Account:
	def __init__(self, domain):
		self.domain = domain

	def permutations_wordlist(self):
		permutations_wordlist = open('/root/Desktop/final_codes/AWSCodeFiles/permutations.txt', 'r').read().splitlines()
		return permutations_wordlist

	def bruteforce_wordlist(self): 
		subdomain = ".s3.amazonaws.com"
		protocol = "https://"

		permWords = self.permutations_wordlist()
		file = open('/root/Desktop/final_codes/AWSCodeFiles/bruteforceWordlist.txt', 'w')
		file.write(protocol + str(self.domain) + subdomain + "\n")
		file.close()

		file = open('/root/Desktop/final_codes/AWSCodeFiles/bruteforceWordlist.txt', 'a')

		for p in permWords:
			file.write(protocol + p + str(self.domain) + subdomain + "\n")
			file.write(protocol + p + p + str(self.domain) + subdomain + "\n")
			file.write(protocol + str(self.domain) + p + subdomain + "\n")
			file.write(protocol + str(self.domain) + p + p + subdomain + "\n")
		file.close()

	def SABF(self):
		self.bruteforce_wordlist()
		SABF_wordlist = open('/root/Desktop/final_codes/AWSCodeFiles/bruteforceWordlist.txt', 'r').read().splitlines()
		accounts = []
		for url in SABF_wordlist:
			try:
				response = requests.get(url, timeout = 0.5)
				if "200" in str(response.status_code):
					print("200 response from url: " + str(url))
					accounts.append(url)

			except Exception as e:
				continue

		with open("/root/Desktop/final_codes/AWSCodeFiles/storage_accounts.txt", "w") as storage_file:
			for ac in accounts:
				storage_file.write(ac + '\n')
		for a in accounts:
			print(f"account: {a}")

	def parsing_urls(self):
		urls_list = open('/root/Desktop/final_codes/AWSCodeFiles/storage_accounts.txt', 'r').read().splitlines()
		final_urls = []
		urls = []
		for url in urls_list:
			try:
				response1 = requests.get(url)
				response2 = response1.text
				soup = BeautifulSoup(response2, 'xml')
				urls = soup.find_all('Key')

			except:
				print("error")

		for i in urls:
			i = str(i).replace("<Key>", "")
			i = str(i).replace("</Key>", "")
			final_urls.append(i)
			print("\t" + str(i))




def main():
	Domain = input("Please enter a domain: ")
	az = Azure_Account(Domain)
	az.SABF()
	az.CNBF()
	az.parsing_urls()

	aws = AWS_Account(Domain)
	aws.SABF()
	aws.parsing_urls()
	gcp = GCP_Account(Domain)