from pyshow.streamtv import StreamTVService
import requests

class Hulu(StreamTVService):

    NAME ='Hulu'
    URL = 'https://www.hulu.com/{}'
    
    JSON_URL_TEMPLATE = 'https://mozart.hulu.com/v1.h2o/shows/{}/episodes?sort=recent&access_token={}'

    def __init__(self):
        StreamTVService.__init__(self, Hulu.NAME, Hulu.URL.format(''))

    def _update_show_data(self, show):
        r = requests.get(self.URL.format(show))
        at = self._get_dom(r.text, 'API_DONUT = ', end_char=';')
        show_id = self._get_dom(r.text, '"id":', start_str='rawData', end_char=',')
        json_url = Hulu.JSON_URL_TEMPLATE.format(show_id, at)
        r = requests.get(json_url)
        recent_ep_info = r.json()['data'][0]['video']
        ret = dict()
        for key in Hulu.SHOW_KEYS:
            ret[key] = recent_ep_info[key]
        date = ret['original_premiere_date']
        date = [int(x) for x in date[:date.find('T')].split(sep='-')]
        ret['original_premiere_date'] = date
        return ret

    
