import json
from products import get_coles_product_iterator

def draw_progress(self, current, total):
    '''
    DEPRECATED
    Draw a progress bar to the console
    '''
    sys.stderr.write("\x1b[2J\x1b[H")
    if self.bar is None_product_data
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
if __name__ == "__main__":
    print("Running...")
    all_products = get_coles_product_iterator()
    master_json = json.loads('{}')
    for product_json in all_products:
        # compare all keys
        for key, value in product_json.items():
            if key not in master_json:
                master_json[key] = value
            if isinstance(value,dict):
                for k, v in value.items():
                    if k not in master_json[key]:
                        master_json[key][k] = v
    f = open('master.json', 'w+')
    json.dump(master_json, f, indent=4)
    f.close()
    print("Analisys complete, file written to master.json")
