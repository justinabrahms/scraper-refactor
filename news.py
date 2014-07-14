import urllib
from lxml import html
from lxml import etree
from pprint import pprint

_URL = "http://jornaldeangola.sapo.ao"

def get_image_top_news(url):
    """Retrieve the image of the news"""
    
    source = urllib.urlopen(url).read()
    tree = html.document_fromstring(source)
    sec_wrapper = tree.xpath('//section[@class="top"]')
    for img in sec_wrapper:
        image = img.xpath('//section[@class="top"]/figure/a/img/@src')
        for src in image:
            print src

def get_text_top_news(url):
    """ Retrieve the complete news url, the tittle and the first paragraph of the news."""
    
    source = urllib.urlopen(url).read()
    tree = html.document_fromstring(source)
    sec_wrapper = tree.xpath('//section[@class="top"]')
    for h in sec_wrapper:
        href_path = h.xpath('//section[@class="top"]/figure/a/@href')
        for href in href_path:
            full_url = _URL + href
            print "\n", full_url
            
            complete_page = urllib.urlopen(full_url).read()
            tree_complete_page = html.document_fromstring(complete_page)
            for title in tree_complete_page.cssselect('h1.title-section2'):
                print "\n", title.text_content()

            news_snippet = tree_complete_page.xpath('//*[@id="main"]/section[1]/article/div[1]/div/p//text()')
            for p in news_snippet:
                print "\n", p

    

if __name__ == '__main__':
    get_image_top_news(_URL)
    get_text_top_news(_URL)
