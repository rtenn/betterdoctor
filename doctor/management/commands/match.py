import csv
from django.core.management.base import BaseCommand
from django.db.models import Q
from doctor.models import Doctor, Practice


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('match_file.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                row += [''] * (8 - len(row))
                doctors = self.match_doctor(row)
                if doctors:
                    print "%s %s [%s] matched with %s doctors in database" % (
                        row[0], row[1], row[2], doctors.count()
                    )
                else:
                    print "No match found for %s %s [%s]" % (
                        row[0], row[1], row[2]
                    )

    def match_doctor(self, row):
        first_name, last_name, npi, street, street_2, city, state, zip_code = row

        doctor_matches = Doctor.objects.filter(
            Q(npi=npi) |
            Q(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
        )
        practice_matches = Practice.objects.filter(
            street__iexact=street,
            street_2__iexact=street_2,
            city__iexact=city,
            state__iexact=state,
            zip_code=zip_code)
        doctors = doctor_matches | Doctor.objects.filter(
            id__in=practice_matches.values_list('doctor_id')
        )
        return doctors
