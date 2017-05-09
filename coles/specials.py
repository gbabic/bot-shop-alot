from requests import get
from lxml.html import html5parser
import json
import progressbar
import sys

# url = "https://shop.coles.com.au/online/COLRSHomePage?storeId=20601&catalogId=10576&langId=-1&tabType=specials&tabId=specials&personaliseSort=false&orderBy=20601_6&errorView=AjaxActionErrorResponse&requesttype=ajax&beginIndex=0"

# The base url for all requests
base_url = "https://shop.coles.com.au/online/COLRSHomePage"
# Query string parameters
params = {
    "storeId":"20601",
    "catalogId":"10576",
    "langId":"-1",
    "tabType":"specials",
    "tabId":"specials",
    "personaliseSort":"false",
    "orderBy":"20601_6",
    "errorView":"AjaxActionErrorResponse",
    "requesttype":"ajax",
    "beginIndex":"0"
}
# database product mapping
'''
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
'''

class ColesSpecials():

    def __init__(self, url, params):
        '''
        Set the base url and determine how many pages of specials we have
        '''
        # set url
        self.base_url = url
        self.params = params
        self.bar = None
        # execute until finished
        while self.next_page():
            pass

    def next_page(self):
        '''
        download the data for the current page and increment for the next page
        returns True if there are more pages to process and false if there
        are no more products to process.
        '''
        url = self.get_url()
        # request page
        page = get(url)
        # parse html markup
        html = html5parser.fragment_fromstring(page.content, True)
        divs = html.findall(".//{http://www.w3.org/1999/xhtml}div")
        json_string = ""
        # find the div that contains our catalog json file
        for i in range(0, len(divs)):
            d = divs[i]
            if d.text != None and "COLRSCatalogEntryList" in d.text:
                json_string = d.text
                break
        # parse the json
        specials_json = json.loads(json_string)
        search_info = specials_json['searchInfo']
        products = specials_json['products']
        # print json.dumps(specials_json, indent=4)
        for product in products:
            # record the product in the database
            self.record_product_special(product)
        # read params
        product_count = int(search_info['totalCount'])
        page_size = int(search_info['pageSize'])
        begin_index = int(params['beginIndex']) + page_size
        params['beginIndex'] = str(begin_index)
        
        #update the progress bar
        self.draw_progress(begin_index,product_count)
        # return True if we need to be called again to complete the proccess
        return begin_index < product_count

    def record_product_special(self, product_json):
        '''
        Register the product special to the database
        TODO
        '''
        # print json.dumps(product_json, indent=4)
        pass
    
    def draw_progress(self, current, total):
        '''
        Draw a progress bar to the console
        '''
        sys.stderr.write("\x1b[2J\x1b[H")
        if self.bar is None:
            widgets = [
                'Scraping: ', progressbar.Percentage(),
                ' ', progressbar.Bar(),
                ' ', progressbar.ETA(),
            ]
            self.bar = progressbar.ProgressBar(widgets=widgets, max_value=total).start()
        if current >= total:
            self.bar.finish()
        else:
            self.bar.update(current)

    def get_url(self):
        '''
        Construct URL from params
        '''
        query = []
        for key,value in self.params.iteritems():
            query.append("{key}={value}".format(key=key,value=value))
        return self.base_url+"?"+"&".join(query)


if __name__ == '__main__':
    ColesSpecials(url = base_url, params = params)

