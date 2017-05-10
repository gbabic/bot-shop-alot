import json
import sys

from requests import get, exceptions
from lxml.html import html5parser

# url = "https://shop.coles.com.au/online/COLRSHomePage?storeId=20601&catalogId=10576&langId=-1&tabType=specials&tabId=specials&personaliseSort=false&orderBy=20601_6&errorView=AjaxActionErrorResponse&requesttype=ajax&beginIndex=0"

# The base url for all requests
base_url = "https://shop.coles.com.au/online/COLRSHomePage"
# Query string parameters
params_specials_only = {
    "storeId":"20601",
    "catalogId":"10576",
    "langId":"-1",
    "tabType":"specials",                   # specials, everything
    "tabId":"specials",                     # specials, everything
    "personaliseSort":"false",
    "orderBy":"20601_6",
    "errorView":"AjaxActionErrorResponse",
    "requesttype":"ajax",
    "beginIndex":"0"
}
params_everything = {
    "storeId":"20601",
    "catalogId":"10576",
    "langId":"-1",
    "tabType":"everything",                   # specials, everything
    "tabId":"everything",                     # specials, everything
    "personaliseSort":"false",
    "orderBy":"20601_6",
    "errorView":"AjaxActionErrorResponse",
    "requesttype":"ajax",
    "beginIndex":"0"
}
# database product mapping
"""
Below is the json representation of one product:
{
    'a': {
        'A4': ['1 .0'],
        'L2': ['false'],
        'O3': ['150g'],                                               // Product weight
        'P8': ['Pantry'],
        'T1': ['false'],
        'W1': ['false']
    },
    'm': 'Parkers',                                                   // Product Brand
    'n': 'Original Pretzels 6 pack',                                  // Product Name
    'p': '9283061P',
    'p1': {
        'o': '3.52'                                                   // Original Price
    },
    'pd': '2 for $5',                                                 // Deal
    'pi': '10139507',
    'pl': '12',                                                       // Total Item Qty.
    'pq': '2',                                                        // Package Qty.
    'pr': '2.50000',                                                  // Unit Price
    'pt': 'MultibuyMultiSk',                                          // Deal Type
    's': 'parkers-pretzels-original',
    's9': '166217',
    't': '/wcsstore/Coles-CAS/images/9/2/8/9283061-th.jpg',           // Product Image
    't1': 'M',
    '': '107116',                                                     // Unique ID
    'u2': '$2.35 per 100G'
}
"""

class ColesProductIterator():

    def __init__(self, url, params):
        """
        Set the base url and determine how many pages of specials we have
        """
        self.base_url = url         # base url for request building
        self.params = params        # dictionary of key values for the query string
        self.search_data = None     # json data describing last page result search
        self.product_data = None    # json data containing product information from last page
        # get initial set of data
            

        
    def __iter__(self):
        """
        Make this class iterable by returning our generator function
        """
        return self._product_generator()

    def _update_search_info(self):
        """
        parse the search info json and update the params
        """
        product_count = int(self.search_data['totalCount'])
        page_size = int(self.search_data['pageSize'])
        begin_index = int(self.params['beginIndex']) + page_size
        self.params['beginIndex'] = str(begin_index)

    def _product_generator(self):
        """
        Generator function
        yield each product until we run out
        """
        while self._has_next_page():
            self._get_data()
            self._update_search_info()
            for product in self.products_data:
                # record the product in the database
                yield product

    def _get_data(self):
        """
        pull down the data per the current params
        """
        url = self._get_url()
        # request page
        page = get(url)
        # raise an error
        # page.raise_for_status()
        # parse html markup
        html = html5parser.fragment_fromstring(page.content, True)
        divs = html.findall(".//{http://www.w3.org/1999/xhtml}div")
        json_string = ""
        # find the div that contains our catalog json file
        # TODO: everything request seems to have diffent html structure then specials find a method that works for both of them
        for i in range(0, len(divs)):
            d = divs[i]
            if d.text != None and "COLRSCatalogEntryList" in d.text:
                json_string = d.text
                break
        # parse the json
        try:
            data_json = json.loads(json_string)
        except ValueError:
            return False

        self.search_data = data_json['searchInfo']
        self.products_data = data_json['products']
        # we return true on success
        return True

    def _has_next_page(self):
        """
        parses the current search_data to determine if there are more
        pages to be parsed
        """
        if self.search_data is None:
            return True
        begin_index = int(self.params['beginIndex'])
        product_count = int(self.search_data['totalCount'])
        page_size = int(self.search_data['pageSize'])
        # return True if there are more products to parse
        return begin_index < product_count

    def _get_url(self):
        """
        Construct URL from params
        """
        query = []
        for key,value in self.params.iteritems():
            query.append("{key}={value}".format(key=key,value=value))
        return self.base_url+"?"+"&".join(query)

"""
Helper methods for import that will return the corresponding product iterator
"""
def get_coles_specials_iterator():
    return ColesProductIterator(url = base_url, params = params_specials_only)

def get_coles_everything_iterator():
    return ColesProductIterator(url = base_url, params = params_everything)

# if this python file is run directly then we will run the demo
if __name__ == '__main__':
    # list out all products
    # all_products = get_coles_everything_iterator()
    # for p in all_products:
    #     print json.dumps(p, indent=4)
    # list out all products on special
    products_on_special = get_coles_specials_iterator()
    for p in products_on_special:
        print json.dumps(p, indent=4)


