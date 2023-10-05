import json
with open('/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linkedin_proxycurl.json', 'r') as f:
    data = json.load(f)


def linkedin_parse(data):
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


parse_data = linkedin_parse(data)

print(parse_data)
