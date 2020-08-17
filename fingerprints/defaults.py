import os

# auto discovery
DEFAULT_SETTINGS_MODULE = True

#: API key for AcoustID lookups
ACOUSTID_API_KEY = os.environ.get('ACOUSTID_API_KEY')

#: Supported audio formats
AUDIO_FORMATS = ('aac', 'aif', 'flac', 'm4a', 'mp3', 'wav')

#: AcoustID fingerprint version
FINGERPRINT_VERSION = 1

#: Minimum similarity with the worst matching fingerprint
TRACK_GROUP_MERGE_THRESHOLD = 0.4

#: Maximum alignment differences of fingerprints in a track
TRACK_MAX_OFFSET = 80

#: Maximum allowed difference of track lengths,
#: tracks with longer length difference will never match 
FINGERPRINT_MAX_LENGTH_DIFF = 7
