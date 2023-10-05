import os
import re
import json
import tempfile
import unicodedata

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class CrawlWebsite(BaseModel):
    url: str
    js: bool = False
    depth: int = 1
    max_pages: int = 100
    max_time: int = 60

    def _crawl(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def process(self):
        content = self._crawl(self.url)

        # Create a file
        file_name = slugify(self.url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(content)  # pyright: ignore reportPrivateUsage=none
            # Process the file

        if content:
            return temp_file_path, file_name
        else:
            return None
    
    def process_linkedin(self, apikey):
        data_name = slugify(self.url) + ".html"
        # Zenrows
        """
        params = {
            'url': self.url,
            'apikey': apikey,
            'js_render': 'true',
            'premium_proxy': 'true',
        }
        response = requests.get('https://api.zenrows.com/v1/', params=params)
        # TODO: Exception process
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = ""

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
        return data
        """
        
        # ProxyCurl
        headers = {'Authorization': 'Bearer ' + apikey}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': self.url,
            'fallback_to_cache': 'on-error',
            'use_cache': 'if-present',
            'skills': 'include',
            'inferred_salary': 'include',
            'personal_email': 'include',
            'personal_contact_number': 'include',
            'twitter_profile_id': 'include',
            'facebook_profile_id': 'include',
            'github_profile_id': 'include',
            'extra': 'include',
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)
        json_string = json.dumps(json.loads(response.text), indent=4)
        return {
            "status_code": response.status_code,
            "message": response.text,
            "json_string": json_string,
            "data_name": data_name
        }

        # Test
        # with open('/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linkedin_proxycurl.txt', 'r') as f:
        #     response_text = f.read()
        # return response_text
        # response_parse = json.load(response_text)

    def checkGithub(self):
        if "github.com" in self.url:
            return True
        else:
            return False

    def checkLinkedIn(self):
        if "linkedin.com" in self.url:
            return True
        else:
            return False


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode(
        "ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text
