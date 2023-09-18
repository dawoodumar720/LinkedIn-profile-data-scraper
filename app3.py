import requests
from bs4 import BeautifulSoup

# Initial GET request to LinkedIn to obtain the CSRF token
login_url = 'https://www.linkedin.com/uas/login'
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the CSRF token from the response
csrf_token = soup.find('input', {'name': 'loginCsrfParam'})['value']

# Define your LinkedIn login credentials
username = 'montidevil79@gmail.com'
password = 'Link79@1257'

# Prepare the login POST request payload with CSRF token
login_payload = {
    'session_key': username,
    'session_password': password,
    'loginCsrfParam': csrf_token,
}

# Perform the login
login_response = session.post(login_url, data=login_payload)
# print(login_response)

# Check if the login was successful (you may need to adjust this condition)
if 'Sign Out' in login_response.text:
    print("Login successful")
else:
    print("Login failed")

# URL for searching people with similar names
people_search_url = 'https://www.linkedin.com/search/results/people/?keywords=ahmed'

# Send a GET request to the people search URL
people_search_response = session.get(people_search_url)

# Parse and print the search results
people_search_soup = BeautifulSoup(people_search_response.content, 'html.parser')
results = people_search_soup.find_all('li', class_='search-result')

for result in results:
    name = result.find('span', class_='name').text.strip()
    headline = result.find('p', class_='subline-level-1').text.strip()
    print(f"Name: {name}")
    print(f"Headline: {headline}")
    print("-" * 30)
