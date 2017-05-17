import pickle
from datetime import date
from os.path import isfile
from pyshow.streamtv import StreamTVService

class Pyshow(object):

    def __init__(self, *, config_file = 'config.cfg'):
        self.config_file = config_file
        if self.has_config():
            with open(self.config_file, 'rb') as cf:
                self.data = pickle.load(cf)
        else:
            self.data = {'last_update': date.fromtimestamp(0), 'streams': dict()}

    def __getitem__(self, item):
        return self.data['streams'][item]

    def has_config(self):
        return isfile(self.config_file)
        
    def add_stream(self, stream_object):
        if isinstance(stream_object, StreamTVService):
            self.data['streams'][stream_object.name] = stream_object
        else:
            raise TypeError('Pyshow: only streams of type StreamTVService can be added')

    def add_stream_data(self, stream_data):
        for stream_object, showlist in stream_data.items():
            self.add_stream(stream_object)
            for show in showlist:
                self[stream_object.name].add_show(show)

    def update(self):
        for stream in self.data['streams']:
            self.update_stream(stream)
        self.data['last_update'] = date.today()
        
    def update_stream(self, stream):
        if stream in self.data['streams']:
            for show in self[stream].shows:
                self[stream].update_show(show)
            self.save()
        else:
            raise KeyError('Pyshow: Stream {} has not been added to this instance'.format(stream))

    def save(self):
        with open(self.config_file, 'wb') as cf:
            pickle.dump(self.data, cf)

    def days_since_opd(self, stream, show):
        if stream in self.data['streams']:
            show = self[stream]._format_for_url(show)
            if show in self[stream].shows:
                return (date.today() - date(*self[stream][show]['original_premiere_date'])).days
            else:
                raise KeyError('Pyshow: Show {} has not been added to stream {}.'.format(show,stream))
        else:
            raise KeyError('Pyshow: Stream {} has not been added to this instance'.format(stream))
    
    def new_shows(self):
        ns = []
        self.check_for_updates()
        for stream in self.data['streams']:
            for show in self[stream].shows:
                if self.days_since_opd(stream, show) == 1:
                    ns.append(show)
        return ns

    def check_for_updates(self):
        if (date.today() - self.data['last_update']).days > 0:
            self.update()
            self.save()
            return True
        else:
            return False
