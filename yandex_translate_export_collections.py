import os, time, random
import pdfkit
from selenium import webdriver
from jinja2 import Template

SELENIUM_WEBDRIVER_PATH = os.path.abspath(os.getcwd()) + '/chromedriver'
COLLECTION_TEMPLATE_HTML = os.path.abspath(os.getcwd()) + '/collection_template.html'


class YandexTranslateCollection:

    def __init__(self, url):

        driver = webdriver.Chrome(SELENIUM_WEBDRIVER_PATH)
        driver.get(url)

        self.title = driver.find_element_by_class_name('collection-header_name').text
        self.words = list(zip([el.text for el in driver.find_elements_by_css_selector('li.record-item .record-item_text')]
                              , [el.text for el in driver.find_elements_by_css_selector('li.record-item .record-item_translation')]))
        time.sleep(random.uniform(0, 5))
        driver.quit()

    def __str__(self):
        return 'Title: ' + str(self.title) + ' words: ' + str(self.words)

    def render_html_page(self):
        with open(COLLECTION_TEMPLATE_HTML, "r") as filein, open(str(self.title)+'.html', "w") as fileout:
            fileout.write(Template(filein.read()).render(title=self.title, collection_elements=self.words))

    def export_to_pdf(self):
        pdfkit.from_file(str(self.title)+'.html', str(self.title) + '.pdf')


if __name__ == '__main__':
    url = input('URL: ')
    ytc = YandexTranslateCollection(url)
    ytc.render_html_page()
    ytc.export_to_pdf()
