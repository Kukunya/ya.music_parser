from bs4 import BeautifulSoup
from requests import get


def find_artists(start_page: int, stop_page: int):
    def find_link():
        for album in album_selectable:
            a_tag = album.find('a')
            artists_links.append(url+a_tag.get('href'))

    print('looking for new albums...')
    for i in range(start_page, stop_page):
        print(f'\rsave the links of artists from the {i} page...', end='')
        html = get(url + f"genre/%D0%BC%D0%B5%D1%82%D0%B0%D0%BB/albums/new?page={i}").text
        soup = BeautifulSoup(html, 'html.parser')
        album_selectable = soup.find_all('span', class_='d-artists')
        find_link()
    print()


def find_favourites():
    def check_count():
        b_button_label = d_like_theme_count.find('span', class_='d-button__label')
        if b_button_label:
            if int(b_button_label.text.replace(' ', '')) > favourites:
                suitable_artists_links.append(artist_link)

    amount_links = len(artists_links)
    for i, artist_link in enumerate(artists_links):
        print(f'\rselect suitable artists... [{i+1}/{amount_links}]', end='')
        html = get(artist_link).text
        soup = BeautifulSoup(html, 'html.parser')
        d_like_theme_count = soup.find('span', class_='d-like d-like_theme-count')
        check_count()
    print(f'\nthere were {len(suitable_artists_links)} suitable')


url = "https://music.yandex.ru/"
f_page = 7
l_page = 28
favourites = 500

artists_links = []
suitable_artists_links = []

find_artists(f_page, l_page)
find_favourites()

with open('artists.txt', 'w') as file:
    file.write('\n'.join(set(suitable_artists_links)))
