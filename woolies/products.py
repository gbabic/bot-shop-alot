import requests
import json

from model import WooliesPageIterator
from model import WooliesURLIterator
from model import WooliesRequiredKeys


product = json.loads('{}')

final_json = WooliesRequiredKeys()


def dict_extractor(dict_value):

    for key, value in dict_value.items():
        if isinstance(value, dict):
            dict_extractor(value)
        elif isinstance(value, (list, tuple)):
            for index in range(len(value)):
                dict_extractor(value[index])
        else:
            if key in final_json.required_keys:
                product[key] = value
    return product


def main():
    total_products = 0
    product_list = []
    master_json = json.loads('{}')

    current_url = WooliesURLIterator()

    for url in current_url:
        url_page = WooliesPageIterator(url)
        for pages in url_page:
            r = requests.get(pages)

            if r.status_code != 200:
                """
                Page not found, break out of the current loop
                """
                print ("Page not found, break out of the current loop")
                break

            parsed_json = r.json()

            products_on_page = parsed_json.get('Bundles')
            print "Products on this page = {} ".format(len(products_on_page))
            total_products += len(products_on_page)

            if len(products_on_page) == 0:
                """
                Products on the page is zero, break out of the current loop
                """
                print("Products on the page is zero, break out of the current loop")
                break

            for index_num in range(len(products_on_page)):
                single_prod = dict_extractor(products_on_page[index_num])
                product_list.append(dict(single_prod))

            if isinstance(master_json, dict):
                master_json['Products'] = product_list

    f = open('master.json', 'w+')
    json.dump(master_json, f, indent=4)
    f.close()
    print "Scrapping complete, total products found = {}".format(total_products)

if __name__ == '__main__':
    main()


