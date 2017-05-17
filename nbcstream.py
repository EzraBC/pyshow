from pyshow.streamtv import StreamTVService
import requests

class NBC(StreamTVService):

    NAME ='NBC'
    URL = 'http://www.nbc.com/{}'

    def __init__(self):
        StreamTVService.__init__(self, NBC.NAME, NBC.URL.format(''))

    def _update_show_data(self, show):
        ret = dict()
        r = requests.get(self.URL.format(show))
        show_url = self.URL.format(self._get_dom(r.text, 'href="/', start_str = 'ad-topbox mps-ad__content', end_char='"'))
        ret['id'] = show_url.split(sep='/')[-1]
        ret['thumbnail'] = self._get_dom(r.text, 'src=', start_str = 'card__thumbnail', end_char='?')
        r = requests.get(show_url)
        ret['title'] = self._get_dom(r.text, 'content=', start_str = 'og:title', end_char='/')
        date = self._get_dom(r.text, '>', start_str = 'video-meta__air-date', end_char='<')
        date = date.split(sep='/')
        year = date.pop()
        year = '20' + year
        date.insert(0, year)
        date = [int(x) for x in date]
        ret['original_premiere_date'] = date
        return ret
