from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Optional


# example parse simple JSON
def parse_json():
    import json
    with open('content/webinars.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for webinar in data:
        print(webinar['speaker'])


# example parse downloaded HTML
def parse_html():
    with open('content/skillbox.html', 'r', encoding='utf-8') as fd:
        data = fd.read()
    parsed_data = BeautifulSoup(data)

    links = parsed_data.findAll('a')
    for link in links:
        print(link.string.strip(), link.attrs['href'])


def scrap_webinar_tag(webinar_card: Tag, tag_name: Optional[str] = None, **kwargs) -> Tag:
    data = webinar_card.findAll(tag_name, **kwargs)
    assert len(data) == 1, f'Incorrect number of lens: {data!r} for kwargs: {kwargs!r} and tag_name: {tag_name!r}'
    return data[0]


def parse_webinar_card_item(webinar_card: Tag, site_url: str) -> None:
    '''
    Попробуйте доработать последний кусок кода и распарсить также
    - Ссылку на страницу вебинара, или
    - Дату проведения вебинара, или
    - Количество просмотров
    '''
    if isinstance(webinar_card, Tag):
        href = scrap_webinar_tag(webinar_card, tag_name='a').attrs.get('href', '').strip()
        title = scrap_webinar_tag(webinar_card, class_='webinar-card__title t t--4').string.strip()
        date = scrap_webinar_tag(webinar_card, class_='webinar-card__date f f--12').string.strip()
        # string is empty for this class. it's not obvious why?
        watch = scrap_webinar_tag(
            webinar_card, class_='webinar-views webinar-card__views f f--12 webinar-views--card').text.strip()
        print(
            f'Название: {title:<40} \nДата: {date:<11} Просмотры: {watch:<8} Ссылка: {site_url + href:<40}')
    else:
        raise ValueError(f'Unexpected type for webinar_card: {type(webinar_card)}')


# example parse HTML with real GET request
def parse_real_site():
    import requests
    site_url = 'https://live.skillbox.ru'
    skill_html = requests.get(site_url)
    if skill_html.status_code == 200:
        parsed_data = BeautifulSoup(skill_html.content)
        webinars = parsed_data.findAll(class_="webinars__item")
        for webinar in webinars:
            parse_webinar_card_item(webinar, site_url)
    else:
        raise ValueError(f'Status code is: {skill_html.status_code}')


if __name__ == "__main__":
    # parse_json()
    # parse_html()
    parse_real_site()
