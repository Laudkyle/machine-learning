from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://porngeek.com/").text
count = 1
site_list = []
line = "--------------------------------------------------------------------------------------------------------"
soup = BeautifulSoup(html_text, "lxml")
sites = soup.find_all("li", class_="item-list__row")
for site in sites:
    site = site.find("a")
    print(f"""
  {count}.  Site : {site['href']}
    """)
    count += 1
    site = site["href"]
    site_list.append(site)
    print(line)

print(site_list)