import urllib
import os
import unittest
from lxml import html
from lxml import etree
from pprint import pprint

_URL = "http://jornaldeangola.sapo.ao"

def get_image_top_news(source):
    """Retrieve the image of the news"""
    tree = html.document_fromstring(source)
    return tree.xpath('//section[@class="top"]/figure/a/img/@src')

def get_text_top_news(source):
    """ Retrieve the complete news url, the tittle and the first paragraph of the news."""
    
    tree = html.document_fromstring(source)
    sec_wrapper = tree.xpath('//section[@class="top"]')
    for h in sec_wrapper:
        href_path = h.xpath('//section[@class="top"]/figure/a/@href')
        for href in href_path:
            full_url = _URL + href
            print "\n", full_url
            
            complete_page = urllib.urlopen(full_url).read()
            get_complete_page(complete_page)


def get_complete_page(source):
    tree_complete_page = html.document_fromstring(source)
    titles = []

    title = tree_complete_page.cssselect('h1.title-section2')[0].text_content()

    news_snippet = tree_complete_page.xpath('//*[@id="main"]/section[1]/article/div[1]/div/p//text()')

    return ([title], news_snippet)


class ImageTests(unittest.TestCase):
    def setUp(self):
        with open('./source.html') as f:
            self.fixture = f.read()

    def test_returns_correct_value(self):
        url = ['http://thumbs.sapo.pt/?pic=http%3A%2F%2Fimgs.sapo.pt%2Fjornaldeangola%2Fimg%2Fthumb1%2F20140714065343pinda_simao_lgo.jpg&W=405&H=307&errorpic=http%3A%2F%2Fimgs.sapo.pt%2Fjornaldeangola2012%2Fimg%2Fdefaultja_051113.png']
        self.assertEqual(url, get_image_top_news(self.fixture))

class TextTests(unittest.TestCase):
    def setUp(self):
        with open('./detail.html') as f:
            self.fixture = f.read()

    def test_complete_page(self):
        retval = ([u'Investir nas lideran\xe7as d\xe1 qualidade ao ensino'], 
                  [u'O ministro da Educa\xe7\xe3o esteve\xa0 no Lubango, Caluquembe e Caconda onde se  inteirou do funcionamento do sector. Pinda Sim\xe3o disse em entrevista ao', ' Jornal de Angola', u' que foi estabelecido um di\xe1logo com os directores de escolas e com o  Conselho de Ausculta\xe7\xe3o e Concerta\xe7\xe3o Social em busca de solu\xe7\xf5es para  as reivindica\xe7\xf5es apresentadas pelos professores.'])
        self.assertEqual(retval, get_complete_page(self.fixture))




    
def main():
    source = urllib.urlopen(_URL).read()
    for img in get_image_top_news(source):
        print img
    titles, snippets = get_text_top_news(source)
    for title in titles:
        print "\n", titles
    for snippet in snippets:
        print "\n", snippet

if __name__ == '__main__':
    if os.getenv("TESTING"):
        unittest.main()
    else:
        main()

