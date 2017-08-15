import json
from django.core.management.base import BaseCommand
from doctor.models import Doctor, Practice


class Command(BaseCommand):
    def handle(self, *args, **options):
        source_data = open('source_data.json')
        for doctor_data in source_data:
            doctor = json.loads(doctor_data)
            doc = Doctor.objects.create(**doctor['doctor'])
            for practice in doctor['practices']:
                practice['zip_code'] = practice.pop('zip')
                Practice.objects.create(doctor=doc, **practice)
