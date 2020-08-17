from app_defaults import settings
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

from fingerprints.models import _fingerprint, Fingerprint
from itertools import islice
from time import time
import os, re
import concurrent.futures


SEEN = {}


def walk(base):
    if os.path.isdir(base):
        for dirpath, dirnames, filenames in os.walk(base):
            for name in filenames:
                path = os.path.join(dirpath, name)
                root, format = os.path.splitext(name)
                format = format[1:].lower()

                if format not in settings.AUDIO_FORMATS:
                    if format != '': print('?', path) # Omit hidden files
                elif path.lower() not in SEEN:
                    yield path

    elif base.lower() not in SEEN:
        yield base


def fingerprint(path):
    duration, fp = _fingerprint(path, force_fpcalc=True)
    print('+', path)
    return Fingerprint(path=path, duration=duration, fingerprint=fp)
    

def cluster(fp):
    fp._dedup()
    print('X', fp.path)


class Command(BaseCommand):

    help = 'Scan music files and fingerprint them'
    batch_size = 100

    def add_arguments(self, parser):
        parser.add_argument('base', help='File or directory to scan')

            
    def handle(self, *args, **options):
        
        for fp in Fingerprint.objects.iterator():
            SEEN[ fp.path.lower()] = fp

        # Delete absent files from DB
        removed = set()
        for path in list(SEEN):
            if not os.path.isfile(path):
                print('-', path)
                SEEN.pop(path).delete()
        
        paths = walk(options['base'])
        with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as pool:
            n = 0
            t = time()
            while True:
                batch = list(islice(paths, self.batch_size))
                if not batch: break
                
                # Compute fingerprints for new files concurrently on all CPUs
                batch = list(pool.map(fingerprint, batch))

                # Batch-insert fingerprints, this is faster than one-by-one
                Fingerprint.objects.bulk_create(batch)

                # bulk_create does not call Fingerprint.save().
                # Reload new fingerprints from the DB and find duplicates
                ids = [ fp.pk for fp in batch ]
                for album in set(map(lambda fp: fp.album(), batch)):
                    list(pool.map(cluster, Fingerprint.objects.filter(
                        path__contains=album, pk__in=ids).iterator()))

                n += len(batch)
                delta = time() - t
                print ('%d fingerprints, %.2f / sec' % (n, n / delta))
