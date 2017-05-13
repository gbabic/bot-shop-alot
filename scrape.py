import os
import sys
import json
import progressbar
from coles.products import get_coles_product_iterator

class Scraper():
    def __init__(self):
        self.bar = None
        self.products = get_coles_product_iterator()
        # set up output directory
        self.output_path = "./data/coles/"
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def __call__(self):
        for product in self.products:
            product_id = product['u']
            file_name = product_id
            file_path = self._get_unique_filename(file_name, 'txt')
            if not os.path.exists(file_path):
                fout = open(file_path, 'w+')
                json.dump(product,fout,indent=4)
            self.draw_progress(self.products.current, self.products.total)

    def _get_unique_filename(self, file_name, file_ext):
        file_path = os.path.join(self.output_path, file_name+'.'+file_ext)
        # count = 2
        # while os.path.exists(file_path):
        #     file_path = os.path.join(self.output_path,file_name+'_'+str(count)+'.'+file_ext)
        return file_path

    def draw_progress(self, current, total):
        '''
        DEPRECATED
        Draw a progress bar to the console
        '''
        sys.stdout.write("\x1b[2J\x1b[H")
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

if __name__=="__main__":
    scraper = Scraper()
    scraper()

