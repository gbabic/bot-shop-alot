import json
import sys
import locale
import time

from requests import get, exceptions
from lxml import etree
from lxml.html import html5parser

# The base url for all requests
base_url = "https://shop.coles.com.au/online/a-national"
# Query string parameters
base_params = {
    "storeId":"20601",
    "catalogId":"10576",
    "langId":"-1",
    "tabType":"everything",
    "tabId":"everything",
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
    'pl': '12',                                                       // Total Item Qty. per pkg
    'pq': '2',                                                        // Package Qty.
    'pr': '2.50000',                                                  // Reduced Price 
    'pt': 'MultibuyMultiSk',                                          // Deal Type
    's': 'parkers-pretzels-original',
    's9': '166217',
    't': '/wcsstore/Coles-CAS/images/9/2/8/9283061-th.jpg',           // Product Image
    't1': 'M',
    '': '107116',                                                     // Unique ID
    'u2': '$2.35 per 100G'
}
"""

class ColesCategoryIterator():

    def __init__(self,url):
        """
        Set base url and load the page ready
        """
        self.base_url = url
        content = self._get_page_content()
        json_data = self._get_data_json(content)
        self._categories = self._get_categories(json_data)

    def _get_categories(self, json_data):
        categories = []
        for c1 in json_data['catalogGroupView']:
            level_one = c1['seo_token']
            for c2 in c1['catalogGroupView']:
                level_two = c2['seo_token']
                category = "{}/{}".format(level_one,level_two)
                categories.append(category)
        return categories

    def __iter__(self):
        return self._categories.__iter__()

    def __len__(self):
        return len(self._categories)

    def _get_page_content(self):
        r = get(self.base_url)
        r.raise_for_status()
        return r.content

    def _get_data_json(self, content):
        tree = etree.HTML(content)
        # currently the json is stored in the first div of the body
        elem = tree.xpath('./body/div')[0]
        return json.loads(elem.text)


class ColesProductIterator():

    def __init__(self, url, params):
        """
        Set the base url and determine how many pages of specials we have
        """
        self._base_url = url
        self._params = params
        self._search_data = None
        self._product_data = None
        self.total = 0
        self.current = 0
        
    def __iter__(self):
        """
        Make this class iterable by returning our generator function
        """
        return self._product_generator()

    def __len__(self):
        return self.total

    def _update_search_info(self):
        """
        parse the search info json and update the params
        """
        page_size = int(self._search_data['pageSize'])
        begin_index = int(self._params['beginIndex']) + page_size
        self._params['beginIndex'] = str(begin_index)

    def _product_generator(self):
        """
        Generator function
        yield each product until we run out
        """
        categories = ColesCategoryIterator(self._base_url)
        self.total = len(categories)
        for category in categories:
            # print("Searching Category: {}".format(category))
            # print self._get_url(category)
            self._params['beginIndex'] = "0"
            while self._has_next_page():
                self._get_data(category)
                self._update_search_info()
                for product in self._product_data:
                    # record the product in the database
                    yield product
            self.current += 1

    def _get_data(self, category):
        """
        pull down the data per the current params
        """
        url = self._get_url(category)
        # request page
        page = get(url)
        # print page.content
        # exit()
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
        # print "json string is:\n{}".format(json_string)
        data_json = json.loads(json_string)
        self._search_data = data_json['searchInfo']
        self._product_data = data_json['products']
        # we return true on success
        return True

    def _has_next_page(self):
        """
        parses the current search_data to determine if there are more
        pages to be parsed
        """
        if self._search_data is None:
            return True
        begin_index = int(self._params['beginIndex'])
        product_count = int(self._search_data['totalCount'])
        page_size = int(self._search_data['pageSize'])
        # return True if there are more products to parse
        return begin_index < product_count

    def _get_url(self, category):
        """
        Construct URL from params
        """
        query = []
        for key,value in self._params.iteritems():
            query.append("{key}={value}".format(key=key,value=value))
        return "{base}/{category}?{query}".format(base = self._base_url, category = category, query = "&".join(query))

"""
Helper methods for import that will return the corresponding product iterator
"""
def get_coles_product_iterator():
    return ColesProductIterator(url = base_url, params = base_params)

# if this python file is run directly then we will run the demo
if __name__ == '__main__':
    # print demo notice
    notice = "DEMO: one product every half second."
    print("-"*len(notice))
    print(notice)
    print("-"*len(notice))
    time.sleep(1)
    # set the locale for currency
    locale.setlocale(locale.LC_ALL, '')
    # list out all products
    all_products = get_coles_product_iterator()
    for p in all_products:
        # print json.dumps(p, indent=4)
        print("{} {}: {}".format(p['m'], p['n'], locale.currency(float(p['p1']['o']))))
        time.sleep(.5)

    #l list out all categories
    # all_categories = ColesCategoryIterator(base_url)
    # for category in all_categories:
    #     print category


