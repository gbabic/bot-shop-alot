# List of URL's
import re

FRUIT_VEG_URL = ("https://www.woolworths.com.au/apis/ui/browse?aisle=fruit-veg&category=fresh-fruit&formatObject=%7B%22name%22:%22fresh+fruit%22%7D&isMobile=false&pageNumber=1&pageSize=24&richRelevanceId=VSC_156&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Ffruit-veg%2Ffresh-fruit", )
MEAT_SEAFOOD_DELI_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_D5A2236&formatObject=%7B%22name%22:%22Meat,+Seafood+%26+Deli%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fmeat-seafood-deli", )
BAKERY_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_DEB537E&formatObject=%7B%22name%22:%22Bakery%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fbakery", )
DAIRY_EGG_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_6E4F4E4&formatObject=%7B%22name%22:%22Dairy,+Eggs+%26+Fridge%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fdairy-eggs-fridge", )
PANTRY_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_39FD49C&formatObject=%7B%22name%22:%22Pantry%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fpantry", )
FREEZER_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_ACA2FC2&formatObject=%7B%22name%22:%22Freezer%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Ffreezer", )
DRINKS_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_5AF3A0A&formatObject=%7B%22name%22:%22Drinks%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fdrinks", )
LIQUOR_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_C8BFD01&formatObject=%7B%22name%22:%22Liquor%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fliquor", )
PET_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_61D6FEB&formatObject=%7B%22name%22:%22Pet%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fpet", )
BABY_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_717A94B&formatObject=%7B%22name%22:%22Baby%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fbaby", )
BEAUTY_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_894D0A8&formatObject=%7B%22name%22:%22Health+%26+Beauty%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fhealth-beauty", )
HOUSEHOLD_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_2432B58&formatObject=%7B%22name%22:%22Household%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Fhousehold", )
LUNCHBOX_URL = ("https://www.woolworths.com.au/apis/ui/browse/category?categoryId=1_9E92C35&formatObject=%7B%22name%22:%22Lunch+Box%22%7D&isBundle=false&isMobile=false&isSpecial=false&pageNumber=1&pageSize=24&sortType=TraderRelevance&url=%2FShop%2FBrowse%2Flunch-box", )

ALL_PRODUCTS = (FRUIT_VEG_URL, MEAT_SEAFOOD_DELI_URL, BAKERY_URL, DAIRY_EGG_URL, PANTRY_URL, FREEZER_URL, DRINKS_URL, LIQUOR_URL, PET_URL, BABY_URL, BEAUTY_URL, HOUSEHOLD_URL, LUNCHBOX_URL)
# ALL_PRODUCTS = (FRUIT_VEG_URL, )

REQUIRED_KEYS = ('FullDescription', 'WasPrice', 'IsAvailable', 'Description', 'PackageSize', 'SmallFormatDescription', 'Name', 'Stockcode', 'Brand', 'Price', 'SavingsAmount', 'Unit', 'SmallImageFile');


class WooliesRequiredKeys:
    """
    Required Keys from Woolies JSON
    """

    def __init__(self):
        self.required_keys = REQUIRED_KEYS


class WooliesPageIterator:
    """
    Page Iterator
    """
    page_number = 0

    def __init__(self, page):
        self.page_number = 0
        self.page = page

    def __iter__(self):
        return self

    def next(self):
        self.page_number += 1
        return re.sub('pageNumber=[0-9]', "pageNumber="+str(self.page_number), self.page[0], 1)


class WooliesURLIterator:
    """
    URL Iterator
    """
    index = 0

    def __init__(self):
        self.url = ALL_PRODUCTS
        WooliesURLIterator.index = 0

    def __iter__(self):
        return self

    def next(self):
        WooliesURLIterator.index += 1
        if WooliesURLIterator.index > len(self.url):
            raise StopIteration
        return self.url[WooliesURLIterator.index - 1]









