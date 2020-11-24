import requests
from bs4 import BeautifulSoup
import pprint
import sys


def scrape_hn(pages: int=1) -> tuple:
	'''
	scrape_hn: scrape hacker news to create list of links and subtext

	Parameters:
		pages {int}: number of pages to scroll
			Defaults to 1
	Returns {tuple}: list of links, list of subtexts

	Examples:
		links, subtexts = scrape_hn(4)
		links, subtexts = scrape_hn(int(sys.argv[1]))

	'''
	base = 'https://news.ycombinator.com/news?p='
	links = []
	subtexts = []
	for idx, _ in enumerate(range(pages)):
		res = requests.get(f'{base}{idx+1}')
		soup = BeautifulSoup(res.text, 'html.parser')
		links.extend(soup.select('.storylink'))
		subtexts.extend(soup.select('.subtext'))
	return (links, subtexts)


def create_custom_hn(links: list, subtexts: list) -> list:
	'''
	create_custom_hn: Create your custom Hacker News

	Parameters:
		links {list}: list of links
			iterable is of type BeautifulSoup.select
		subtexts {list}: list of title subtexts
			terable is of type BeautifulSoup.select
	Returns {list}: List of dictionaries
		dictionary has keys "title", "link", and "score"
	'''
	hn = []
	for idx, item in enumerate(links):
		title = item.getText()
		href = item.get('href', None)
		vote = subtexts[idx].select('.score')
		if len(vote):
			score = int(vote[0].getText().replace(' points', ''))
		else:
			score = 0
		# points = int(votes[idx].getText().replace(' points', ''))
		if score > 99:
			hn.append({'title': title, 'link': href, 'score': score})
	return sort_stories(hn)


def sort_stories(hn: list, reverse: bool=True) -> list:
	'''
	sort_stores: Sort hacker news stories by score

	Parameters:
		reverse {bool}: if true, desc
	
	Returns:
		hn {list}: sorted list

	Examples:
		sort_stories(hn)
		sort_stories(hn, False)
	'''
	return sorted(hn, key=lambda k: k['score'], reverse=reverse)


def create_news_file(hn: list) -> None:
	'''
	create_news_file: create custom news file

	Parameters: 
		hn {list}: list of dictionaries
	'''
	with open('news.txt', 'w') as f:
		for idx, line in enumerate(hn):
			f.write(f"{idx+1}.\n{line['title']} ({line['link']})\nVotes: {line['score']}\n\n")
	return None


links, subtexts = scrape_hn(int(sys.argv[1]))

custom_news = create_custom_hn(links, subtexts)

create_news_file(custom_news)
