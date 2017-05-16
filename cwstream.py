from streamtv import StreamTVService
import requests

class TheCW(StreamTVService):

    NAME ='The CW'
    URL = 'http://www.cwtv.com/shows/{}'

    def __init__(self):
        StreamTVService.__init__(self, TheCW.NAME, TheCW.URL.format(''))

    @staticmethod
    def _get_dom(html_text, dom_name, *, end_char):
        start = html_text.find(dom_name) + len(dom_name)
        end = html_text.find(end_char,start)
        arg = html_text[start:end]
        arg = arg.strip()
        arg = arg.strip("'")
        arg = arg.strip('"')
        return arg

    def _update_show_data(self, show):
        ret = dict()
        ret['id'] = None
        r = requests.get(self.URL.format(show))
        ret['title'] = self._get_dom(r.text, 'itemprop="name" content=', end_char='/')
        ret['thumbnail'] = self._get_dom(r.text, 'itemprop="thumbnail" content=', end_char='/')
        date = self._get_dom(r.text[:r.text.find('SHARE MENU BEGIN')], 'Original Air Date: ', end_char='<')
        date = date.split(sep='.')
        year = date.pop()
        year = '20' + year
        date.insert(0, year)
        date = [int(x) for x in date]
        ret['original_premiere_date'] = date
        return ret
