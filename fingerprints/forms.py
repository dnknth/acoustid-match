from app_defaults import settings
from django import forms 
from django.contrib.postgres.forms import SimpleArrayField


JQUERY = 'admin/js/vendor/jquery/jquery.js' if settings.DEBUG \
    else 'admin/js/vendor/jquery/jquery.min.js'


class FingerprintWidget(forms.Widget):
    "Graphic representation of the audio fingerprint"
    
    template_name = 'fingerprints/forms/fingerprint.html'
    
    class Media:
        js = (JQUERY,
            'fingerprints/fputils.js',
            'fingerprints/jquery.json-viewer.js',
            'admin/js/jquery.init.js' )
        css = { 'all': ('fingerprints/jquery.json-viewer.css', ) }


class FingerprintForm(forms.ModelForm):
    "Override the default Fingerprint model form to show the fingerprint as image"
    
    fingerprint = SimpleArrayField(forms.IntegerField(), widget=FingerprintWidget)
