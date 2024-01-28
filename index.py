import time
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import matplotlib.pyplot as plt

languages = [
    "JavaScript", "Python", "Java", "C#", "PHP", "TypeScript", "C++", "Ruby",
    "Go", "Swift", "Kotlin", "Rust", "Scala", "Perl", "Dart", "Lua", "Haskell",
    "Objective-C", "Groovy", ".NET Framework", "Node.js", "React", "Angular", "Vue.js",
    "Spring Framework", "Django", "Flask", "Ruby on Rails", "ASP.NET", "Laravel",
    "Bootstrap", "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy", "Git", "Docker",
    "Kubernetes", "AWS", "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
    "Apache Kafka", "Elasticsearch", "GraphQL", "Vue"
]


case_mapping = {language.lower(): language for language in languages}


def count_languages(text, languages):
    language_count = Counter()
    for language in languages:
        if re.search(r'\b' + re.escape(language) + r'\b', text, re.IGNORECASE):
            language_count[language] += 1
    return language_count

def scrape_job_postings(urls):
    num = 1
    total_language_count = Counter()
    for url in urls:
        page = 1
        while True:
            full_url = f"{url}?page={page}"
            response = requests.get(full_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            postings = soup.find_all("div", class_="PaidJob")
            if not postings:
                break

            for post in postings:
                print(f"Scraping {num}")
                text = post.get_text().lower()
                language_count = count_languages(text, languages)
                total_language_count.update(language_count)
                num += 1
                print(text)

            page += 1
    return total_language_count

urls = [
    "https://www.jobindex.dk/jobsoegning/it/systemudvikling/danmark",
    # "https://www.jobindex.dk/jobsoegning/it/itdrift/danmark",
    "https://www.jobindex.dk/jobsoegning/it/virksomhedssystemer/danmark",
    # "https://www.jobindex.dk/jobsoegning/it/itledelse/danmark",
    "https://www.jobindex.dk/jobsoegning/it/internet/danmark",
    # "https://www.jobindex.dk/jobsoegning/it/telekom/danmark",
    # "https://www.jobindex.dk/jobsoegning/it/database/danmark"
]

language_mentions = scrape_job_postings(urls)

import csv

with open('language_mentions.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Technology', 'Mentions']) 
    for tech, count in language_mentions.items():
        writer.writerow([tech, count])

print(language_mentions)
print("Data saved to language_mentions.csv")

top_languages = language_mentions.most_common(15)
languages, counts = zip(*top_languages)

plt.figure(figsize=(10, 6))
plt.bar(languages, counts, color='skyblue')
plt.xlabel('Sprog')
plt.ylabel('Nævnte gange')
plt.title('Top 15')
plt.xticks(rotation=45)
plt.show()
