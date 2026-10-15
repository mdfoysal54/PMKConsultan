from .models import SiteSettings

def branding(request):
    try: site=SiteSettings.objects.first()
    except Exception: site=None  # DB may not be migrated during initial setup
    return {'pmk_site':site}
