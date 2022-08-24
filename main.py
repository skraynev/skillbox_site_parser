from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary


# example parse simple JSON
def parse_downloaded_json():
    """ Demonstrates simple parsing JSON file """
    import json
    with open('content/webinars.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for webinar in data:
        print(webinar['speaker'])


# example parse downloaded HTML
def parse_downloaded_html():
    """ Demonstrates simple parsing HTML file """
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
    """
    Homework #1: Попробуйте доработать последний кусок кода и распарсить также
    - Ссылку на страницу вебинара, или
    - Дату проведения вебинара, или
    - Количество просмотров
    """
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
def parse_skillbox_site_example():
    """ Example of parsing site after GET request """
    site_url = 'https://live.skillbox.ru'
    skill_html = requests.get(site_url)
    if skill_html.status_code == 200:
        parsed_data = BeautifulSoup(skill_html.content)
        webinars = parsed_data.findAll(class_="webinars__item")
        for webinar in webinars:
            parse_webinar_card_item(webinar, site_url)
    else:
        raise ValueError(f'Status code is: {skill_html.status_code}')


def parse_avto_ru_copied_fetch_case():
    """ Copy AJAX request from browser web tool and use it for getting and parsing some custom data """
    def fetch(url, params):
        headers = params['headers']
        body = params['body']
        return requests.post(url, headers=headers, data=body)

    # headers were removed, because they are outdated already.
    # Example of the AJAX request copied from browser dev tool, like:
    # copy as Node.js fetch
    response = fetch("https://auto.ru/-/ajax/desktop/listing/", {
       "headers": {
         # ...
       },
       "body": "{\"year_to\":2010,\"catalog_filter\":[{\"mark\":\"LAMBORGHINI\"}],\"section\":\"all\",\"category\":\"cars\",\"output_type\":\"list\"}",
       "method": "POST"
    })
    assert response.status_code == 200
    lambo_data = response.json()
    for offer in lambo_data['offers']:
        mark = offer['vehicle_info']['mark_info']
        model = offer['vehicle_info']['model_info']
        tech = offer['vehicle_info']['tech_param']
        print(f'{mark["name"]} {model["name"]} за {offer["price_info"]["RUR"]} руб. / {tech["human_name"]}')


def use_selenium_on_hh_site():
    """
    Use selenium for simple test scenario:
    * open site
    * find search text box and print "Python Junior"
    * find search button and click on it
    * find on the page with result the number of vacancies and print it in console
    """
    # or use directly loaded exe file
    # browser = webdriver.Chrome('./chromium_driver.exe')
    browser = webdriver.Chrome()
    browser.maximize_window()  # open window on the full screen
    browser.get("http://hh.ru")
    # search input text element by id, XPATH, css_selector
    search_input = browser.find_element(By.ID, "a11y-search-input")
    search_input.send_keys("Python Junior")  # input text
    # search button
    search_button = browser.find_element(By.CSS_SELECTOR, 'button[data-qa="search-button"]')
    search_button.click()

    # search the header with information. we have to wait the page loading!!!
    header = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"]')

    import re
    count = re.sub(r"\D", "", header.text)  # replace everything, what is not a string
    print(f'Найдено вакансий: {count}')

    time.sleep(5)
    browser.close()


def use_selenium_on_avto_ru_site():
    """
    Homework #2:  Напишите код парсера используя Selenium:
    - Зайдите на сайт auto.ru
    - Кликните по разделу “LADA”
    - Кликните по переключателю “В кредит”
    - Кликните по кнопке “Показать предложения”
    - Распарсите и выведите на экран цены на автомобили, используйте функцию find_elements

    Бонусное сложное задание:
    Выведите модель самого дешевого автомобиля
    """
    pass


if __name__ == "__main__":
    # parse_downloaded_json()
    # parse_downloaded_html()
    # parse_skillbox_site_example()
    # parse_avto_ru_copied_fetch_case()
    # use_selenium_on_hh_site()
    use_selenium_on_avto_ru_site()
