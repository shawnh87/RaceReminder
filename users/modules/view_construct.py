from datetime import datetime, timedelta
from requests import get
from json import loads
from re import search
from users.models import Zip, Region, EventType, State
from django.core.mail import send_mail
from br_email.models import Event
from requests.exceptions import RequestException, MissingSchema
from django.utils import timezone


def get_location(zip_cd):
    """Map zip to lat + long"""
    try:
        curr_zip = Zip.objects.get(zip=zip_cd)
        location = str(curr_zip.lat) + '|' + str(curr_zip.lng)
    except Zip.DoesNotExist:
        location = ''
    return location


def run_date(day, cad):
    """calc nex run date"""
    today = datetime.today()
    return today + timedelta(days=(cad-(today.weekday() - day)))


def get_dates(cadence):
    """helper to build out start and end dates"""
    delta = int(cadence) if cadence else 31
    today = datetime.today()
    start = today + timedelta(days=1)
    end = today + timedelta(days=delta)
    return [start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')]


class BikeRegCall:

    def __init__(self, user, form=None, url=None, events = None, email = None, cadence = 14):
        self.user = user
        self.form = form        
        self.url = url
        self.events = events
        self.email = email
        self.cadence = cadence

    def get_q_string_dat(self):
        """given a form, get q string data; returns params for q string
        start date and end date appended on run in get_events method"""

        state_pk = [i for i in self.form.cleaned_data['states'] if i != '1']  # pk=1 is blank
        states = State.objects.filter(pk__in=state_pk).values()
        states_out = str([i['state'] for i in states]).replace(" ", '').replace("'", '').strip('[]')

        region_pk = [i for i in self.form.cleaned_data['region'] if i != '1']  # pk=1 is blank
        regions = Region.objects.filter(pk__in=region_pk).values()
        regions_out = str([i['region'] for i in regions]).replace(" ", '').replace("'", '').strip('[]')

        event_pk = self.form.cleaned_data['event']
        events = EventType.objects.filter(pk__in=event_pk).values()
        events_out = str([i['event'].replace(' ', '%20') for i in events]).replace(" ", '').replace("'", '').strip('[]')

        distance_out = self.form.cleaned_data['distance']
        zip_cd = self.form.cleaned_data.get('zip')
        location_out = str(get_location(zip_cd))

        self.cadence = int(self.form.cleaned_data.get('dstr_cad'))

        return {'states_out': states_out, 'regions_out': regions_out, 'events_out': events_out,
                'location_out': location_out, 'distance_out': distance_out}


    def build_q_string(self, params):
        """"Builds out q string from params"""

        base = 'http://www.BikeReg.com/api/search?'

        if params['states_out'] != '':
            states = f"states={params['states_out']}"
        else:
            states = None

        if params['regions_out'] != '':
            regions = f"region={params['regions_out']}"
        else:
            regions = None

        if params['distance_out'] and params['location_out'] != '':
            location = f"loc={params['location_out']}&distance={params['distance_out']}"
        else:
            location = None

        events = f"eventtype={params['events_out']}"

        q_string = [events, location, states, regions]#, dates]
        q_string_out = '&'.join([i for i in q_string if i])
        self.url = base+q_string_out


    def get_events(self):
        """Removes all present Events from user account.
        Appends end and run dates to q string.
        Makes call to breg api. Returns events for dist and populates db. 
        On fail notification sent out."""

        Event.objects.filter(user=self.user).delete()
        dates = get_dates(self.cadence)
        call_string = self.url + f"&startDate={dates[0]}&endDate={dates[1]}"
        try:
            d = get(call_string, timeout=30)
            dat = loads(d.text)
            events = []
            for event in dat['MatchingEvents']:
                vals = ['EventCity', 'EventName', 'EventState', 'EventUrl',
                        'Latitude', 'Longitude', 'RegCloseDate', 'EventDate', 'EventTypes']

                race = {key: value for key, value in event.items() if key in vals}
                close = int(search('(?<=\()(.*)(?=\-)', race['RegCloseDate']).group())/1000
                event = int(search('(?<=\()(.*)(?=\-)', race['EventDate']).group())/1000

                reg_close_date = datetime.fromtimestamp(close)
                reg_close_date_aware = timezone.make_aware(reg_close_date, timezone.get_current_timezone())

                event_date = datetime.fromtimestamp(event)
                event_date_aware = timezone.make_aware(event_date, timezone.get_current_timezone())

                race['RegCloseDate'] = reg_close_date_aware
                race['EventDate'] = event_date_aware
                race['EventTypes'] = str(race['EventTypes']).replace("'", '').strip('[]')

                event = Event(user=self.user, **race)
                event.save()

                events.append({'name': race['EventName'], 'url': race['EventUrl'], 
                'date': race['EventDate'].strftime('%m-%d-%Y'), 'city': race['EventCity'],
                             'state': race['EventState'], 'event_type':  race['EventTypes']} )

            split = '____________________________________________'
            out = [
                    f"\n{i['name']}\n{i['date']}\n{i['city']}-{i['state']}\n{i['event_type'].replace(',', ';')}\n{i['url']}\n{split}" 
                    for i in events
                    ]
            self.events = ', '.join(out).replace(", ", '')

        
        except (ValueError, RequestException, MissingSchema,AttributeError) as e:
            send_mail(
                    'CONNECTION ERROR',str(e),
                    'race.reminders@gmail.com',
                    ['race.reminders@gmail.com'],
                    fail_silently=True,
                    )

    def send_events(self):
        """distribution method"""

        if self.events:
            head = "Hi,\n\nHere are the events from Bike Reg you requested!\n\n"
            footer = "\n\nThanks,\nRaceReminder\n\n\n\nTo unsubribe, please visit: http://localhost:8000/profile/"

            send_mail(
                'RaceReminder: Your Events',
                head+self.events+footer,
                'race.reminders@gmail.com',
                [self.email],
                fail_silently=True,
            )



            