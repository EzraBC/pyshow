class StreamTVService(object):

    SHOW_KEYS = ['title', 'original_premiere_date', 'id', 'thumbnail_url']
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.shows = dict()

    def __getitem__(self, item):
        return self.shows[self._format_for_url(item)]

    def _format_for_url(self, name):
        name = name.strip()
        name = name.lower()
        name = name.replace(' ', '-')
        name = name.replace(':', '')
        name = name.replace("'", '')
        name = name.replace('"', '')
        return name

    @staticmethod
    def _get_dom(html_text, dom_name, *, end_char, start_str = None):
        if not start_str == None:
            html_text = html_text[html_text.find(start_str):]
        start = html_text.find(dom_name) + len(dom_name)
        end = html_text.find(end_char,start)
        arg = html_text[start:end]
        arg = arg.strip()
        arg = arg.strip("'")
        arg = arg.strip('"')
        return arg

    @classmethod
    def _update_show_data(cls, show):
        raise NotImplementedError('{cls.NAME}\'s update_show is not yet implemented')

    def add_show(self, show):
        show = self._format_for_url(show)
        if show in self.shows:
            return False
        else:
            self.shows[show] = dict()
            return True

    def get_show(self, show):
        show = self._format_for_url(show)
        if show not in self.shows:
            IndexError('StreamTVServiceError:Show has not been added!')
        else:
            return self.shows[show]
            
    def update_show(self, show):
        show = self._format_for_url(show)
        if show not in self.shows:
            IndexError('StreamTVServiceError:Show has not been added!')
        else:
            self.shows[show] = self._update_show_data(show)
