import os
import bs4
import requests
import pandas
import json

url = "https://dev.to"

crawl = requests.get(url)

soup = bs4.BeautifulSoup(crawl.content, 'html.parser')

dataOutput = {

  "blogs" : [

  ]

}

def crawContent(url):
  crawlData = requests.get(url)
  soupContent = bs4.BeautifulSoup(crawlData.content, 'html.parser')
  content = soupContent.select('div.crayons-article__main')[0]
  return content

# hotTopicArticle = soup.select("main#articles-list div.crayons-story.crayons-story--featured div.crayons-story__indention h2 a")[0].get_text().strip()

# hotTopicLink = url + soup.select("main#articles-list div.crayons-story.crayons-story--featured div.crayons-story__indention h2 a")[0]['href']

# hotTopicAuthor = soup.select("main#articles-list div.crayons-story.crayons-story--featured div.crayons-story__top div.crayons-story__meta div:nth-child(2) p a")[0].get_text().strip()

# print(hotTopicArticle, '-', hotTopicLink, 'By: ', hotTopicAuthor)

divArticles = soup.find_all("div", class_= "substories")

for divs in divArticles:
  div = divs.find_all("div", class_= "crayons-story")
  for i in range(len(div)):
    article = div[i].select('div.crayons-story__indention h2 a')[0].get_text().strip()
    link = url + div[i].select('div.crayons-story__indention h2 a')[0]["href"]
    author = div[i].select('div.crayons-story__meta div:nth-child(2) p a')[0].get_text().strip()
    content = crawContent(link)
    dataOutput["blogs"].append({
      "article" : article,
      "author"  : author,
      "link"    : link,
      "content" : str(content)
    })

# for i in source:
#   for j in range(len(i)):
#   newObject["article"] = i[j]
#   newObject["author"] = i[j+1]
#   newObject["links"] = i[j+2]
#   dataOutput["blogs"].append(newObject)
#   break;

# print(json.dumps(dataOutput, indent=4, sort_keys=True))
if os.path.exists('data.json'):
  with open('data.json', 'w') as outfile:
    json.dump(dataOutput, outfile, indent=4)

# This is the output that I want
# {
#   "blogs" : [
#     {
#       "article" : "How to code Python on windows",
#       "author"   : "Antory Ph.D",
#       "links"    : "https://abc.com"
#     },
#     {
#       "article" : "How to code Python on windows",
#       "author"   : "Antory Ph.D",
#       "links"    : "https://abc.com"
#     }
#   ]
# }