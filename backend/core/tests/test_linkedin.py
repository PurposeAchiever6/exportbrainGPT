# from selenium import webdriver
# from linkedin_scraper import Person

# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless") # Ensure GUI is off
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome(options=chrome_options)
# # driver = webdriver.Chrome()
# person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)
# print(person)


# # pip install zenrows
# from zenrows import ZenRowsClient

# client = ZenRowsClient("3935a9723d4f528a9b218317734b60904cd7c593")
# url = "https://www.linkedin.com/in/andrewyng"
# params = {"js_render":"true","premium_proxy":"true"}

# response = client.get(url, params=params)

# print(response.text)


# pip install requests
import requests
from bs4 import BeautifulSoup

url = 'https://www.linkedin.com/in/andrewyng'
apikey = '3935a9723d4f528a9b218317734b60904cd7c593'
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
	'premium_proxy': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
soup = BeautifulSoup(response.content, 'html.parser')
print(response.text)


data = ""
# soup = BeautifulSoup(response.content, 'html.parser')


# with open('/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linkedin.html', "rb") as f:
#     content = f.read()
#     soup = BeautifulSoup(content, 'html.parser')

intro = soup.find('div', {'class': 'top-card-layout__entity-info'})
name_loc = intro.find("h1")
name = name_loc.get_text().strip()

description_loc = intro.find("h2")
description = description_loc.get_text().strip()

data = data + f"\nName: {name}\nDescription: {description}"

for card in soup.find_all('section', class_ = 'core-section-container'):
    try:
        card_name = card.find('h2').get_text().strip()
        
        if card_name == "Experience":
            data = data + f"\n\n\nExperience"
            for experience in card.find_all('li'):
                role = experience.find('h3').get_text().strip()
                company = experience.find('h4').get_text().strip()
                data = data + f"\n\nRole: {role}\nCompany: {company}"
                for sentence_loc in experience.find_all('p'):
                    if sentence_loc.get('class')[0] != 'show-more-less-text__text--less':
                        sentence = sentence_loc.get_text().strip().replace('.\n', '').replace('\n', '').replace('Show less', '')
                        data = data + f"\n{sentence}"
        
        elif card_name == "Education":
            data = data + f"\n\n\nEducation"
            for education in card.find_all('li'):
                name = education.find('h3').get_text().strip()
                degree = education.find('h4').get_text().strip()
                data = data + f"\n\n{name}\n{degree}"
                for sentence_loc in education.find_all('p'):
                    sentence = sentence_loc.get_text().strip().replace('.\n', '').replace('\n', '')
                    data = data + f"\n{sentence}"

    except:
        continue

print(str(data))





# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import time

# # Creating an instance
# driver = webdriver.Chrome("Enter-Location-Of-Your-Web-Driver")

# # Logging into LinkedIn
# driver.get("https://linkedin.com/uas/login")
# time.sleep(5)

# username = driver.find_element(By.ID, "username")
# username.send_keys("") # Enter Your Email Address

# pword = driver.find_element(By.ID, "password")
# pword.send_keys("")	 # Enter Your Password

# driver.find_element(By.XPATH, "//button[@type='submit']").click()

# # Opening Kunal's Profile
# # paste the URL of Kunal's profile here
# profile_url = "https://www.linkedin.com/in/kunalshah1/"

# driver.get(profile_url)	 # this will open the link
