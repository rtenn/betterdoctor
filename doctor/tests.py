# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from doctor.management.commands.match import Command
from doctor.models import Doctor, Practice


class MatchTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name="test",
            last_name="doctor",
            npi="00000000000000000001"
        )
        self.practice = Practice.objects.create(
            doctor=self.doctor,
            street="1665 Haight St",
            street_2="",
            city="San Francisco",
            state="CA",
            zip_code="94117",
            lat=37.769444,
            lon=-122.449921
        )

    def test_npi_match(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched', 'name', self.doctor.npi, '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_name_match(self):
        command = Command()
        doctors = command.match_doctor([
            self.doctor.first_name,
            self.doctor.last_name,
            "55555555555555555555",
            '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_practice_match(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            self.practice.street,
            self.practice.street_2,
            self.practice.city,
            self.practice.state,
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_no_match(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 0)

    def test_name_mismatch(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            self.doctor.last_name,
            "55555555555555555555",
            '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 0)

    def test_practice_mismatch(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            "3279 Harrison St",
            self.practice.street_2,
            self.practice.city,
            self.practice.state,
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 0)

    def test_name_case_insensitive(self):
        command = Command()
        doctors = command.match_doctor([
            self.doctor.first_name.upper(),
            self.doctor.last_name.upper(),
            "55555555555555555555",
            '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

        doctors = command.match_doctor([
            self.doctor.first_name.lower(),
            self.doctor.last_name.lower(),
            "55555555555555555555",
            '', '', '', '', ''
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_address_case_insensitive(self):
        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            self.practice.street.lower(),
            self.practice.street_2.lower(),
            self.practice.city.lower(),
            self.practice.state.lower(),
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            self.practice.street.upper(),
            self.practice.street_2.upper(),
            self.practice.city.upper(),
            self.practice.state.upper(),
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_multiple_practices(self):
        new_practice = Practice.objects.create(
            doctor=self.doctor,
            street="3279 Harrison St",
            street_2="",
            city="San Francisco",
            state="CA",
            zip_code="94110",
            lat=37.745635,
            lon=-122.411322
        )

        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            self.practice.street,
            self.practice.street_2,
            self.practice.city,
            self.practice.state,
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

        command = Command()
        doctors = command.match_doctor([
            'mismatched',
            'name',
            "55555555555555555555",
            new_practice.street,
            new_practice.street_2,
            new_practice.city,
            new_practice.state,
            new_practice.zip_code
        ])
        self.assertEqual(doctors.count(), 1)
        self.assertEqual(doctors[0], self.doctor)

    def test_multiple_matches(self):
        new_doctor = Doctor.objects.create(
            first_name="Kathy",
            last_name="Garcia",
            npi="12345678901234567890"
        )
        command = Command()
        doctors = command.match_doctor([
            new_doctor.first_name,
            new_doctor.last_name,
            new_doctor.npi,
            self.practice.street,
            self.practice.street_2,
            self.practice.city,
            self.practice.state,
            self.practice.zip_code
        ])
        self.assertEqual(doctors.count(), 2)
        self.assertIn(self.doctor, doctors)
        self.assertIn(new_doctor, doctors)
