# pyshow
A python library for finding which shows on various streaming services have aired new episodes

Extremely alpha

Example usage:

	>>> from pyshow import Pyshow
	>>> from pyshow import Hulu, TheCW
	>>> ps = Pyshow(config_file = 'my_config.cfg')
	>>> hulu_shows = ['family guy', 'Trial and Error']
	>>> cw_shows = ['SuPeRnAtUrAl', 'the-originals ']
	>>> stream_data = {Hulu(): hulu_shows, TheCW(): cw_shows}
	>>> ps.add_stream_data(stream_data)
	>>> ps.check_for_updates()
	True
	>>> ps.days_since_opd(Hulu.NAME, 'family-Guy')
	15
	>>> ps['Hulu']['trial and error']['thumbnail_url']
	'http://ib3.huluim.com/video/60876310?size=145x80&img=1'
	>>> ps['Hulu']['trial and error']['title']
	'The Verdict'
