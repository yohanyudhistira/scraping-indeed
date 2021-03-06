import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    url = f'https://uk.indeed.com/jobs?q=python+developer&l=London,+Greater+London&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()
        try:
            salary = item.find('span', class_='salaryText').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_='summary').text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        job_list.append(job)
    return


job_list = []

for i in range(0, 40, 10):
    print(f'Getting pages.....,{i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(job_list)
print(df.head())
df.to_csv('jobs.csv', index=False)
