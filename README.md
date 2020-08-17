# acoustid-match

This is a simplified demonstration of the [AcoustID](https://acoustid.org) algorithm, packaged as a [Django](https://www.djangoproject.com) app.

It computes fingerprints on a music collection, identifies similar tracks, and can optionally look up track artist and title via [AcoustID](https://acoustid.org).

## Prerequisites

- A [PostgreSQL database](https://www.postgresql.org/) with the [AcoustID Postgres Extension](https://github.com/acoustid/pg_acoustid.git),
- The Chromaprint `fpcalc` program. You can download it from [acoustid.org](https://acoustid.org/chromaprint).
- A working Django site running on Postgres.

To look up fingerprints against the [MusicBrainz](https://musicbrainz.org/) [database](https://musicbrainz.org/doc/MusicBrainz_Database), an API key is needed in the `ACOUSTID_API_KEY` environment variable.
See [here](https://acoustid.org/webservice) for instructions.

## Usage

Add `fingerprints` to `INSTALLED_APPS` in the Django settings. Then run `./manage.py scan path/to/your/music/collection` to add tracks. `fpcalc` is expected in the system `PATH`. Because fingerprinting might take a while for a large music collection, `scan` uses all available CPUs in parallel.

When completed, head to the Django admin site. Your music is visible under `fingerprints`, duplicates are already marked. Use the `Identify with MusicBrainz` action in the track list to look up artists and titles of unknown tracks. If successful, tracks are marked as `Identified` and the JSON data is shown in the fingerprint details.

## Credits

Kudos to [Lukáš Lalinský](https://oxygene.sk), the author of the excellent [AcoustID](https://acoustid.org) software.
