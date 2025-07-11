from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import string
import re
from typing import List, Pattern

URL_first = 'https://ru.wikipedia.org/wiki/' \
'%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' \
'%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D' \
'0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
URL_next_pages = 'https://ru.wikipedia.org'

cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
cyrillic_letters = cyrillic_lower_letters + cyrillic_lower_letters.upper()

latin_letters = string.ascii_lowercase + string.ascii_uppercase

# словарь для подсчета кол-ва животных на каждую букву
alphabet = dict.fromkeys(cyrillic_letters + latin_letters, 0)

# получить частичный адрес следующей страницы пагинации
def get_next(doc: BeautifulSoup):
	try:
		title = doc.find(name='a', string="Следующая страница").get('href')
	except AttributeError as e:
		return None
	return title

# получить bs4-объект
def get_html(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	except URLError as e:
		return None
	doc = BeautifulSoup(html, 'html.parser')
	return doc


def get_count_animals(doc: BeautifulSoup):
	page = doc.find(string='Страницы в категории «Животные по алфавиту»')
	pages_div = page.find_parent('div', id='mw-pages')
	letters = pages_div.find_all(name='h3')
	#animals = pages_div.find(name='div', class_='mw-category-group')
	# словарь, где ключ - буква алфавита, значение - кол-во животных
	count_animals = {}
	for letter in letters:
		letter_pattern: Pattern[str] = re.compile(fr'<h3>{letter.contents[0]}</h3>')
		letter_matches: BeautifulSoup = pages_div.find(
			name='div',
			class_='mw-category-group',
			#string=letter_pattern
		)
		count = 0
		animals = pages_div.find(name='div',
			class_='mw-category-group',
			)
			#string=lambda text: text and text.startswith(f'<h3>{letter.contents[0]}</h3>'))
		count_animals[letter.contents[0]] = 0
	
	return count_animals

def main():
	first_page = get_html(URL_first)
	if first_page == None:
		print('Page was not found')
		return
	
	next_page_link = get_next(first_page)
	print(next_page_link)
	get_count_animals(first_page)
	return

main()