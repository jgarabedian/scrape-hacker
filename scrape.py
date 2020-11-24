import requests
from bs4 import BeautifulSoup
import pprint
import sys

base = 'https://news.ycombinator.com/news?p='


links = []
subtexts = []

def scrape_hn(pages: int):
	for idx, _ in enumerate(range(pages)):
		print(idx+1)
		res = requests.get(f'{base}{idx+1}')
		soup = BeautifulSoup(res.text, 'html.parser')
		links.extend(soup.select('.storylink'))
		subtexts.extend(soup.select('.subtext'))

# print(votes[0])
# print(soup.select(id='score_25197890'))

def create_custom_hn(links, subtexts):
	hn = []
	for idx, item in enumerate(links):
		title = links[idx].getText()
		href = links[idx].get('href', None)
		vote = subtexts[idx].select('.score')
		if len(vote):
			score = int(vote[0].getText().replace(' points', ''))
		else:
			score = 0
		# points = int(votes[idx].getText().replace(' points', ''))
		if score > 99:
			hn.append({'title': title, 'link': href, 'score': score})
	return sort_stories(hn)

def sort_stories(hn: list, reverse: bool=True):
	return sorted(hn, key=lambda k: k['score'], reverse=reverse)

def create_news_file(hn):
	with open('news.txt', 'w') as f:
		for line in hn:
			f.write(f"{line['title']} ({line['link']})\nVotes: {line['score']}\n\n")


scrape_hn(int(sys.argv[1]))

custom_news = create_custom_hn(links, subtexts)

create_news_file(custom_news)
