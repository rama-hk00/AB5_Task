import re
import requests 
import socket
import sys
import json
import whois

class rapiddns:

	def __init__(self, domain): # that the user sent 
		self.domain = domain

	def getsSubDomains(self):

		URL = f"https://rapiddns.io/s/{self.domain}#result"
		RQ = requests.get(URL)
		pattern = rf'<td>.*.{self.domain}</td>'
		
		requestListSplit1 = (RQ.text).splitlines()

		##### ADD THE LINES INTO A LIST
		semi_final_list = []
		for i in requestListSplit1:
			i = re.findall(pattern, i)
			semi_final_list.append(i)


		##### REMOVE EMPTY LIST
		remove_empty_list = []
		remove_empty_list = [ele for ele in semi_final_list if ele != []]

		##### REMOVE THE TAGS
		finale_list = []
		for sublist in remove_empty_list:
			for i in sublist:
				i = i.replace('</td>', '')
				i = i.replace('<td>', '')
				finale_list.append(i)
		#print(finale_list)
		return finale_list

############################# NOT USED
class crthtml:

	def __init__(self, domain):
		self.domain = domain
	def getsSubDomains(self):
		URL = f"https://crt.sh/?q={self.domain}"
		RQ = requests.get(URL)

		pattern = rf'<TD>.*.{self.domain}</TD>'

		requestListSplit1 = (RQ.text).splitlines()

		semi_final_list = []
		for i in requestListSplit1:
			i = re.findall(pattern, i)
			semi_final_list.append(i)

		remove_empty_list = []
		remove_empty_list = [ele for ele in semi_final_list if ele != []]

		finale_list = []
		for sublist in remove_empty_list:
			for i in sublist:
				i = i.replace('</TD>', '')
				i = i.replace('<TD>', '')
				i = i.replace('<BR>', '')
				i = i.replace('</BR>', '')
				finale_list.append(i)
		return(finale_list)

	def __del__(self):
		pass

class crtjson:

	def __init__(self, domain):
		self.domain = domain
	def getsSubDomains(self):
		URL = f"https://crt.sh/?q={self.domain}&output=json"
		RQ = requests.get(URL)
		
		temp = []
		listtest = RQ.json()
		#print(listtest[0]["name_value"])
		for i in listtest:
			temp.append(i["name_value"])
		return temp


def main():
	Domain = input("Please Enter a URL: ")

	rpd = rapiddns(str(Domain))
	list1 = rpd.getsSubDomains()

	cj = crtjson(str(Domain))
	list2 = cj.getsSubDomains()


	 #remove this comment
	list3 = list1 + list2
	list3 = [item for item in list3 if "*" not in item]

	unique_list = list(set(list3))
	list_removed = []
	for i in unique_list:
		try:
			result = socket.getaddrinfo(i, None, 0, socket.SOCK_STREAM)
			#for item in result:
			#	print(f"[{i}] IP is resolvable: {item[4]}")
		except:
			#print(f"[{i}] IP is not resolvable.")
			list_removed.append(i) # to see the removed domains
			unique_list.remove(i)

	print("\n")
	print("********************************************************************************************")
	print("Domain list: ")
	print("********************************************************************************************")
	print("\n")
	for i in unique_list:
		print("\t" + i)
	'''
	print("\n")
	print("********************************************************************************************")
	print("Removed Domains: ")
	print("********************************************************************************************")
	print("\n")

	for i in list_removed:
		print(i)
	'''
	print("********************************************************************************************")
	print("whois info")
	print("********************************************************************************************")
	print("\n")


	whois_info = whois.whois(Domain)
	print("Domain Name:")
	for i in whois_info["domain_name"]:
		print("\t" + i)

	print("Name Servers:")
	for i in whois_info["name_servers"]:
		print("\t" + i)

	print("Emails:")
	for i in whois_info["emails"]:
		print("\t" + i)
	print("********************************************************************************************")



