import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""Add a write csv function to add profile data into csv file"""

def write_to_csv(data, csv_filename):
    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
        # Define the CSV header if the file is empty
        is_empty = csv_file.tell() == 0
        fieldnames = ["User Name", "Job Title", "Location", "Profile URL", "Profile Image URL"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if is_empty:
            writer.writeheader()
        
        # Write the data to the CSV file
        writer.writerow(data)

def login_and_extract_users_data(username, password, search_query):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    
    try:
        # Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        
        # Enter username and password
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        
        # Submit login form
        driver.find_element(By.TAG_NAME, "button").click()
        
        # Wait for login to complete
        WebDriverWait(driver, 10).until(EC.url_contains("https://www.linkedin.com/feed/"))
        
        # Perform a search
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}"
        driver.get(search_url)
        
        # Wait for search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__entity-result-list")))
        
        # # Scroll to load more profiles (you can adjust the number of scrolls)
        # for _ in range(10):  # Adjust the number of scrolls as needed
        #     scroll_to_bottom(driver)
        
        for _ in range(5):
            # Get the page source using Selenium
            page_source = driver.page_source
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all the <li> elements containing user data
            profiles = soup.find_all("li", class_="reusable-search__result-container")
            
            # Iterate through the profiles to extract the data
            for profile in profiles:
                user_name_element = soup.find("span", class_="entity-result__title-text t-16")
                job_title = profile.find("div", class_="entity-result__primary-subtitle")
                job_title = job_title.text.strip() if job_title else ""
                location = profile.find("div", class_="entity-result__secondary-subtitle")
                location = location.text.strip() if location else ""
                profile_url = profile.find("a", class_="app-aware-link")["href"]
                profile_image = profile.find("img", class_="presence-entity__image")
                profile_image_url = profile_image["src"] if profile_image else ""
                
                if user_name_element:
                    user_name = user_name_element.get_text(strip=True).split('View')[0].strip()
                    print("User Name:", user_name)
                else:
                    print("User name not found in the HTML data.")
                print("Job Title:", job_title)
                print("Location:", location)
                print("Profile URL:", profile_url)
                print("Profile Image URL:", profile_image_url)
                print("\n")

                # Prepare the data as a dictionary
                data = {
                    "User Name": user_name,
                    "Job Title": job_title,
                    "Location": location,
                    "Profile URL": profile_url,
                    "Profile Image URL": profile_image_url
                }
                
                # Write the data to the CSV file
                write_to_csv(data, "linkedin_profiles.csv")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    username = "montidevil79@gmail.com"
    password = "Link79@1257"
    search_query = "ahmed ali"
    login_and_extract_users_data(username, password, search_query)
