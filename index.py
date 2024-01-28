import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

languages = [
    "Python", "JavaScript", "Java", "C#", "C++", "Ruby", "Go", "Swift", 
    "PHP", "TypeScript", "Kotlin", "Objective-C", "Scala", "Perl",
    ".NET", "Rust", "Dart", "Lua", "Groovy", "Haskell", "Backend", "Frontend",
    "Full Stack", "DevOps", "React", "Angular", "Vue", "Docker",
    "Kubernetes", "AWS", "Azure", "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Oracle", "AI", "Blockchain", "Node.js", "Express.js",
    "Spring", "Django", "Flask", "Laravel", "Bootstrap", "TensorFlow", "PyTorch",
    "Git", "SVN", "JIRA", "Agile", "Scrum", "Linux", "Unix", "Windows", "API",
    "REST", "GraphQL", "HTML", "CSS", "Sass", "LESS", "Webpack", "Babel",
    "npm", "yarn", "Jenkins", "CI/CD", "Selenium", "Testing", "TDD", "BDD",
    "JUnit", "Mocha", "Chai", "Jest", "Cypress", "Azure DevOps", "Firebase",
    "GCP", "IBM Cloud", "Red Hat", "Ansible", "Puppet", "Chef", "Nagios",
    "Prometheus", "ELK", "Splunk", "Data Science", "R", "Matlab", "Tableau",
    "Power BI", "SAS", "SPSS", "Excel", "Big Data", "Hadoop", "Spark", "Flink",
    "Cassandra", "Redis", "Elasticsearch", "Solr", "GraphQL", "Apollo", "Redux",
    "MobX", "RxJS", "Next.js", "Nuxt.js", "Gatsby", "Jekyll", "Electron", 
    "Cordova", "React Native", "Flutter", "Ionic", "Xamarin", "Unity", "Unreal Engine"
]

case_mapping = {language.lower(): language for language in languages}


def count_languages(text, languages):
    language_count = Counter()
    for language in languages:
        if re.search(r'\b' + re.escape(language) + r'\b', text, re.IGNORECASE):
            language_count[language] += 1
    return language_count

def scrape_job_postings(base_url):
    total_language_count = Counter()
    page = 1
    while True:
        url = f"{base_url}it/systemudvikling?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        postings = soup.find_all("div", class_="PaidJob")
        if not postings:
            break

        for post in postings:
            text = post.get_text()
            text = text.lower()
            language_count = count_languages(text, languages)
            total_language_count.update(language_count)

        page += 1

    return total_language_count

base_url = "https://www.jobindex.dk/jobsoegning/"
language_mentions = scrape_job_postings(base_url)

import csv

with open('language_mentions.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Technology', 'Mentions']) 
    for tech, count in language_mentions.items():
        writer.writerow([tech, count])

print("Data saved to language_mentions.csv")


print(language_mentions)
