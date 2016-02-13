# Clean
import datetime as dt
import time
import datetime
from utils import *

def is_present(date_text): return date_text.upper() == 'NOW'
def get_current(): return dt.datetime.now().date()

def clean_datetime(date_text):
    if not isinstance(date_text, basestring):
        return None

    # Parse from text
    date_text = date_text.strip()

    # Replace &nbsp;
    date_text = date_text.replace('&nbsp;', ' ').replace('&ndash;', '-').rstrip('-')
    date_text = date_text.replace('Sept ', 'Sep ').replace('Febr ', 'Feb ').replace('Sept ', 'Sep ').replace('Octo ', 'Oct ')
    date_text = date_text.strip()
    if not date_text: return None

    # Current or present
    if is_present(date_text): return get_current()

    _date = date_text
    for dateformat in dateFormats:
        try:
            _date = dt.datetime.strptime(date_text, dateformat)
            break
        except ValueError as err:
            pass

    try:
        _date = _date.date()
    except AttributeError as err:
        return None
    return _date