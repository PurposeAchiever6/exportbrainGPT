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
        if content:
            file_name = slugify(self.url) + ".html"
            temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
            with open(temp_file_path, "w") as temp_file:
                temp_file.write(content)  # pyright: ignore reportPrivateUsage=none
            
            return temp_file_path, file_name
        else:
            return None, None
    
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
        
        parse_data = self.linkedin_parse(json.loads(response.text))

        return {
            "status_code": response.status_code,
            "message": response.text,
            "parse_data": parse_data,
            "data_name": data_name
        }
    
    def linkedin_parse(self, data):
        parse_data = ""

        if data["full_name"]:
            parse_data += f"This is {data['full_name']}'s personal data"
            parse_data += f"\n\nName: {data['full_name']}"
        else:
            parse_data += f"This is {data['full_name']}'s personal data"

        if data['headline']:
            parse_data = parse_data + f"\n{data['headline']}"
        if data['summary']:
            parse_data = parse_data + f"\n{data['summary']}"

        if data['occupation']:
            parse_data = parse_data + f"\n\noccupation: {data['occupation']}"

        live = "\nLocation: "
        if data['city']:
            live += f"{data['city']}"
        if data['state']:
            live += f", {data['state']}"
        if data['country']:
            live += f", {data['country']}"
        if live != "\nLocation: ":
            parse_data += live

        if data['experiences']:
            parse_data += "\n\n\nExperience:"
            for experience in data['experiences']:
                parse_ex = "\n"
                if experience['starts_at']:
                    parse_ex += f"\nFrom {experience['starts_at']['year']}.{experience['starts_at']['month']}"
                if experience['ends_at']:
                    parse_ex += f" To {experience['ends_at']['year']}.{experience['ends_at']['month']}"

                if experience['company']:
                    parse_ex += f"\nCompany: {experience['company']}"
                if experience['title']:
                    parse_ex += f"\nTitle: {experience['title']}"
                if experience['description']:
                    parse_ex += f"\ndescription: {experience['description']}"
                if experience['location']:
                    parse_ex += f"\nlocation: {experience['location']}"

                parse_data += parse_ex

        if data['education']:
            parse_data += "\n\n\nEducation:"
            for education in data['education']:
                parse_ed = ""
                if education['starts_at']:
                    parse_ed += f"\nFrom {education['starts_at']['year']}.{education['starts_at']['month']}"
                if education['ends_at']:
                    parse_ed += f" To {education['ends_at']['year']}.{education['ends_at']['month']}"

                if education['school']:
                    parse_ed += f"\nSchool: {education['school']}"
                if education['degree_name']:
                    parse_ed += f"\nDegree: {education['degree_name']}"
                if education['grade']:
                    parse_ed += f"\nGrade: {education['grade']}"
                if education['field_of_study']:
                    parse_ed += f"\nField of study: {education['field_of_study']}"

                parse_data += parse_ed

        if data['languages']:
            parse_data += "\n\nLanguage: "
            for language in data['languages']:
                parse_data = parse_data + language + " "

        parse_data += "\n\n"
        if data['personal_emails']:
            parse_data += f"\nEmail: "
            for mail in data['personal_emails']:
                parse_data = parse_data + mail + " "
        if data['personal_numbers']:
            parse_data += f"\nPhone Number: "
            for phone in data['personal_numbers']:
                parse_data = parse_data + phone + " "

        return parse_data

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
