from app_defaults import settings
from acoustid import fingerprint_file, lookup, parse_lookup_result
from chromaprint import decode_fingerprint, encode_fingerprint
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import connection, models
from json import dumps
from uuid import uuid4


PARTS = ((1, 20), (21, 100))
PART_SEARCH_SQL = """
SELECT f.*, score FROM (
    SELECT *, acoustid_compare2(fingerprint, query, %(max_offset)s) AS score
    FROM fingerprints_fingerprint, (SELECT %(fp)s::int4[] AS query) q
    WHERE duration BETWEEN INTERVAL '%(length)s seconds' - INTERVAL '%(max_length_diff)s seconds'
    AND INTERVAL '%(length)s seconds' + INTERVAL '%(max_length_diff)s seconds'
    AND subarray(acoustid_extract_query(query), %(part_start)s, %(part_length)s)
        && acoustid_extract_query(fingerprint)
) f 
WHERE f.score > %(min_score)s
ORDER BY f.score DESC
"""


def _fingerprint(path, force_fpcalc=False):
    "Get the AcoustID fingerprint for an audio track"

    duration, fp = fingerprint_file(path, force_fpcalc=force_fpcalc)
    duration = timedelta(seconds=duration)
    fingerprint, version = decode_fingerprint(fp)
    assert version == settings.FINGERPRINT_VERSION, 'Version mismatch: %s' % version
    return duration, fingerprint


class Fingerprint(models.Model):
    
    path = models.CharField(max_length=1024, unique=True)
    fingerprint = ArrayField(models.IntegerField())
    duration = models.DurationField(default=timedelta(0))

    # Clustering
    cluster = models.UUIDField(null=True, db_index=True)
    
    # AcoustID identity
    acoustid = models.JSONField(null=True)


    def __str__(self):
        "Show AcoustID artist and title if available, or otherwise the track path"

        if self.acoustid:
            for _score, _recording_id, title, artist in parse_lookup_result(self.acoustid):
                if title or artist: return '%s - %s' % (artist, title)
        return self.path


    def album(self):
        'Extract the artist + album from the path'
        return '/'.join(self.path.split('/')[-3:-1])


    def _duplicates(self, max_offset=0):
        'Search for similar fingerprints in the database'

        fp = self.fingerprint
        length = self.duration.total_seconds()
        min_score = settings.TRACK_GROUP_MERGE_THRESHOLD
        max_length_diff = settings.FINGERPRINT_MAX_LENGTH_DIFF
    
        for part_start, part_length in PARTS:
            yield from Fingerprint.objects.raw(PART_SEARCH_SQL, locals()).iterator()


    def save(self, *args, **kwargs):
        "Fingerprint an audio track and find duplicates before saving"

        if not self.fingerprint:
            self.duration, self.fingerprint = _fingerprint(self.path)
        
        super().save(*args, **kwargs)
        self._dedup()


    def _dedup(self):
        "Mark duplicates of this track with a new cluster ID"

        #  Duplicate search needed?
        if self.cluster: return

        # De-dup results from several queries
        fps = set(self._duplicates())
        if len(fps) > 1: # Mark similar fingerprints with new cluster ID
            self.cluster = uuid4()
            Fingerprint.objects.filter(path__in=[ r.path for r in fps ]).update(cluster=self.cluster)


    def lookup(self):
        "Get the artist and title for a track"

        if self.acoustid: return
        
        fp = encode_fingerprint(self.fingerprint, settings.FINGERPRINT_VERSION)
        self.acoustid = lookup(settings.ACOUSTID_API_KEY, fp, self.duration.total_seconds())
        
        # print(dumps(self.acoustid, sort_keys=True, indent=2))
        if self.acoustid['status'] == 'ok' and 'results' in self.acoustid and self.acoustid['results']:
            super().save()


    class Meta:
        ordering = ('path', )
        indexes = [ GinIndex(fields=('fingerprint',),
                fastupdate=True, gin_pending_list_limit=1000) ]
