from app_defaults import settings
from acoustid import fingerprint_file
from chromaprint import decode_fingerprint
from django.db import connection
from django.test import TestCase
from pathlib import Path

from fingerprints.models import *


class FingerprintTests(TestCase):

    AUDIO_TRACK1 = Path.home() / 'Music/TangoTunes/04 Naranjo en flor.m4a'
    AUDIO_TRACK2 = Path.home() / 'Music/iTunes/iTunes Music/Music/Pedro Laurenz/Pedro B Laurenz y su Orquesta Típica 1937-1953/1-15 Naranjo en flor.mp3'


    def setUp(self):
        "Install required Postgres extensions, add audio fingerprints"

        with connection.cursor() as cur:
            cur.execute('CREATE EXTENSION IF NOT EXISTS intarray')
            cur.execute('CREATE EXTENSION IF NOT EXISTS acoustid')
            
        self.fp1, _created = Fingerprint.objects.get_or_create(path=self.AUDIO_TRACK1)
        self.fp2, _created = Fingerprint.objects.get_or_create(path=self.AUDIO_TRACK2)
        

    def test_fingerprints(self):
        "Verify that tracks have fingerprints"
        
        self.assertIsNotNone(self.fp1.fingerprint)
        self.assertIsNotNone(self.fp2.fingerprint)
        

    def test_fingerprinting_methods(self):
        "Verify that fpcalc and acoustid produce identical fingerprints"
        
        duration, fp = fingerprint_file(self.AUDIO_TRACK1, force_fpcalc=True)
        fp, version = decode_fingerprint(fp)
        self.assertEqual(version, settings.FINGERPRINT_VERSION)

        self.assertEqual(int(self.fp1.duration.total_seconds()), duration)
        self.assertSequenceEqual(self.fp1.fingerprint, fp)


    def test_clustering(self):
        "Check that similar tracks are clustered"

        # fp1 can be None if this test runs first
        # fp2 was created last => it determines the cluster ID
        self.assertIsNotNone(self.fp2.cluster)

        self.assertEqual(2, Fingerprint.objects.filter(cluster=self.fp2.cluster).count())
        

    def test_lookup(self):
        "Test whether similar tracks get the same AcoustID result"
        
        self.fp1.lookup()
        self.assertIsNotNone(self.fp1.acoustid)

        self.fp2.lookup()
        self.assertIsNotNone(self.fp2.acoustid)

        self.assertEqual(self.fp1.acoustid['results'][0]['id'],
                          self.fp2.acoustid['results'][0]['id'])


    def test_duplicates(self):
        "Check duplicates"

        dups = set(self.fp1._duplicates())
        self.assertEqual(2, len(dups))

        dups.update(self.fp1._duplicates())
        self.assertEqual(2, len(dups))

        dups.update(self.fp2._duplicates())
        self.assertEqual(2, len(dups))

        self.assertEqual(2, len(set(self.fp2._duplicates())))
