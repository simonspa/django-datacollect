from django.core.management.base import BaseCommand, CommandError
from survey.models import Record
from fuzzywuzzy import fuzz

class Command(BaseCommand):
    help = 'Finds fuzzy name matches and allows to alter their relation'

    def add_arguments(self, parser):
        parser.add_argument('start', nargs='?', type=int, default=0)

    def handle(self, *args, **options):
        rx = Record.objects.all()
        all = rx.count()
        cnt = 0
        print "Iterating over " + str(all) + " database records, starting at " + str(options['start'])
        for i,r1 in enumerate(rx):
            # Obey start position argument
            if i < options['start']: continue
            for j,r2 in enumerate(rx):
                if j <= i: continue

                ratio = fuzz.ratio(r1.name,r2.name)
                if ratio < 75:
                    continue
                if r1.person_id == r2.person_id:
                    continue
                if r1.country != r2.country:
                    continue
                if r1.gender != r2.gender:
                    continue
                # Print leftovers:
                print ""
                print u"Score: {0:3d}         {1:30}{2}".format(ratio,r1.name,r2.name)
                print u"Follow-up:         {0!r:<30}{1}".format(r1.follow_up_case,r2.follow_up_case)
                print u"Date intervention: {0:30}{1}".format(str(r1.date_intervention),str(r2.date_intervention))
                print u"Issue area:        {0:30}{1}".format(r1.issue_area,r2.issue_area)
                print u"Activities:        {0:30}{1}".format(r1.relevant_activities,r2.relevant_activities)
                if Record.objects.filter(pk=r1.pk, follow_ups__pk=r2.pk).exists():
                    print u"Relation exists?       ************** YES ****************"
                else:
                    print u"Relation exists?       ..............  NO ................"
                while True:
                    data = str(raw_input("(a)dd, (r)emove relation, (s)kip or (p)ause: "))
                    if data.lower() not in ('a', 'r', 's', 'p'):
                        print("Not an appropriate choice.")
                    else:
                        break
                if data == "a":
                    r1.follow_ups.add(r2)
                    r1.save()
                elif data == "r":
                    r1.follow_ups.remove(r2)
                    r1.save()
                elif data == "s":
                    continue;
                elif data == "p":
                    print "Restart with argument: " + str(i)
                    self.stdout.write(self.style.SUCCESS('Paused at %i' % i))
                    return
                cnt += 1
                print "Status: {:2.1f}".format((100.0*i)/all)

        self.stdout.write(self.style.SUCCESS('Successfully edited all fuzzy relations'))
