import progressbar

class Scraper():
    def draw_progress(self, current, total):
        '''
        DEPRECATED
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
