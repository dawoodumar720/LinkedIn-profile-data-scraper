from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login_and_extract_cookies(username, password):
    # Creating a webdriver instance
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://linkedin.com/uas/login")

    # waiting for the page to load
    time.sleep(5)

    # entering username
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)

    # entering password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for the login to complete, you can adjust the wait time if needed
    time.sleep(10)

    # Extract cookies
    cookies = driver.get_cookies()

    # Close the browser
    driver.quit()

    return cookies


def extract_specific_cookies(cookies):
    # Define the names of cookies you want to extract
    desired_cookie_names = [
        'bcookie',
        'bscookie',
        '_gcl_au',
        'aam_uuid',
        'li_rm',
        'li_at',
        'liap',
        'JSESSIONID',
        'timezone',
        'li_theme',
        'li_theme_set',
        'li_sugr',
        '_guid',
        'AnalyticsSyncHistory',
        'lms_ads',
        'lms_analytics',
        'lang',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg',
        'UserMatchHistory',
        'lidc'
    ]

    # Create a new dictionary to store the desired cookies and their values
    extracted_cookies = {}

    # Iterate through the list of cookies and extract the desired ones
    for cookie in cookies:
        if cookie['name'] in desired_cookie_names:
            extracted_cookies[cookie['name']] = cookie['value']

    return extracted_cookies

# Example usage
if __name__ == "__main__":
    username = "montidevil79@gmail.com"
    password = "Link79@1257"
    cookies_data = login_and_extract_cookies(username, password)
    # print(extracted_cookies)
    extracted_cookies = extract_specific_cookies(cookies_data)
    print(extracted_cookies)
