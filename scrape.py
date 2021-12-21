from bs4 import BeautifulSoup as bs
import requests

html_text = requests.get("https://www.jobstreet.com.my/en/job-search/python-jobs/").text
soup = bs(html_text, "lxml")
job_title = soup.find('div', class_ ="sx2jih0 _2j8fZ_0 sIMFL_0 _1JtWu_0").text
job_company = soup.find_all('span', class_ = "sx2jih0 zcydq82q zcydq810 iwjz4h0")
print(job_title)
print(job_company)