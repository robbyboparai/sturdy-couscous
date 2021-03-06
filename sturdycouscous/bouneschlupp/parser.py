from logging import ERROR
from bs4 import BeautifulSoup
import requests
from sturdycouscous.bouneschlupp import errors
import logging as log
class Parser:
    """ Prases an HTML page and extracts data such a child-links
    
    Attributes:
        url -- the target page to parse
        links -- list of all the <a> tags and attributes each list element has 
                a dictionnary of attributes/values (element.attrs)
                a text content (element.text) 
    """


    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.links = BeautifulSoup(response.content, 'lxml').find_all('a')
            else:
                raise errors.BadResponseError(response.status_code)
        except BaseException :
            self.links = set()
            

    
    def get_links(self):
        children = set()
        for link in self.links:
            children.add(link.attrs['href'])
        return children

    def get_links_from_child_pages(self):
        children = self.get_links()
        grand_children = set()
        for child in children:
            log.debug("creating child parser for ", child)
            child_page = Parser(child)
            grand_children = grand_children.union(child_page.get_links())
            log.debug("grand children now contain: ", grand_children)
        return children.union(grand_children)

    def get_link_from_descendent(self, depth):
        my_links = self.get_links()
        if depth < 0 :
            raise ValueError("depth of descendent should be greater than 1")
        elif depth == 0:
            return my_links
        elif depth == 1:
            return self.get_links_from_child_pages()
        else:
            descendents = set()
            for link in my_links:
                descendents = descendents.union(self.get_link_from_descendent(depth - 1))
            return descendents




    
        # first_generation = self.get_links()
        # if depth == 1:
        #     return first_generation
        # #recursive call to get the whole family tree  
        # grand_children = set()
        # for child in first_generation:
        #     child_page = Parser(child)
        #     grand_children = grand_children.union(child_page.get_links_from_descendent(depth-1))
        # return first_generation.union(grand_children)
        


