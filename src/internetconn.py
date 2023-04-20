# importing requests module
import requests

# initializing URL
url = "https://www.geeksforgeeks.org"
timeout = 10
try:
	# requesting URL
	request = requests.get(url,
						timeout=timeout)
	print("Internet is on")

# catching exception
except (requests.ConnectionError,
		requests.Timeout) as exception:
	print("Internet is off")
