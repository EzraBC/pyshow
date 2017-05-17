from pyshow.streamtv import StreamTVService
import requests

class TheCW(StreamTVService):

    NAME ='The CW'
    URL = 'http://www.cwtv.com/shows/{}'

    def __init__(self):
        StreamTVService.__init__(self, TheCW.NAME, TheCW.URL.format(''))

    def _update_show_data(self, show):
        ret = dict()
        ret['id'] = None
        r = requests.get(self.URL.format(show))
        ret['title'] = self._get_dom(r.text, 'content=', start_str='itemprop="name"', end_char='/>')
        ret['thumbnail'] = self._get_dom(r.text, 'content=', start_str='itemprop="thumbnail"', end_char='/>')
        date = self._get_dom(r.text, 'Original Air Date:', start_str = 'SHARE MENU BEGIN', end_char='<')
        date = date.split(sep='.')
        year = date.pop()
        year = '20' + year
        date.insert(0, year)
        date = [int(x) for x in date]
        ret['original_premiere_date'] = date
        return ret
