from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from users.modules.view_construct import BikeRegCall, run_date
from users.models import Profile
from datetime import datetime

#####add in opt = ON
class Command(BaseCommand):
    help = 'Executes Event Distribution'

    def handle(self, *args, **options):
        today = datetime.today()
        run_set = Profile.objects.filter(run_date__lte = today).filter(distrib=True)
        for i in run_set:
            day = int(i.dstr_day)
            cad = int(i.dstr_cad)
            i.run_date = run_date(day, cad)
            i.save()
            email = User.objects.get(username=i.user).email
            export = BikeRegCall(user = i.user, url = i.q_string, email = email)
            export.get_events()
            export.send_events()


