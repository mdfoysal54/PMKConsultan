import hashlib
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from .forms import InquiryForm
from .models import Portfolio,Service,Industry,Section

FALLBACK_SERVICES=[
 {'icon':'◇','title':'Web Engineering','short_description':'Premium corporate websites, e-commerce and high-performance digital experiences.'},
 {'icon':'▣','title':'Business Software','short_description':'Custom ERP, CRM, POS, inventory and operations platforms.'},
 {'icon':'◈','title':'Mobile Applications','short_description':'Android and iOS products with scalable backend systems.'},
 {'icon':'✳','title':'AI & Automation','short_description':'Business assistants, document workflows and intelligent operations.'},
 {'icon':'⬡','title':'Cloud & DevOps','short_description':'Deployment, cloud architecture, monitoring and resilience.'},
 {'icon':'✦','title':'Security Engineering','short_description':'Secure architecture, application testing and practical risk reduction.'},
]
FALLBACK_INDUSTRIES=['E-commerce & retail','Healthcare & clinics','Education','Professional services','Logistics & distribution','Startups & SaaS']

def base_context():
    services=list(Service.objects.filter(published=True))
    industries=list(Industry.objects.filter(published=True))
    return {'services':services or FALLBACK_SERVICES,'industries':industries or [{'name':n} for n in FALLBACK_INDUSTRIES], 'sections':{s.key:s for s in Section.objects.filter(enabled=True)}}

def home(request):
    return render(request,'website/home.html',{**base_context(),'projects':Portfolio.objects.filter(is_published=True,featured=True)[:3]})
def services(request): return render(request,'website/services.html',base_context())
def about(request): return render(request,'website/about.html',base_context())
def work(request): return render(request,'website/work.html',{'projects':Portfolio.objects.filter(is_published=True)})
@require_http_methods(['GET','POST'])
def contact(request):
    if request.method=='POST':
        # Single instance uses local memory cache; configure shared Redis for production.
        address=request.META.get('REMOTE_ADDR','unknown')
        key='pmk-inquiry-'+hashlib.sha256(address.encode()).hexdigest()
        count=cache.get(key,0)
        if count>=5:
            form=InquiryForm(request.POST)
            form.add_error(None,'Too many requests. Please try again later.')
            return render(request,'website/contact.html',{'form':form},status=429)
        form=InquiryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('website'): # honeypot: discard bot submissions
                return redirect('contact_success')
            cache.add(key,0,3600)
            cache.incr(key)
            form.save()
            return redirect('contact_success')
    else: form=InquiryForm()
    return render(request,'website/contact.html',{'form':form})
def contact_success(request): return render(request,'website/success.html')
def health(request): return HttpResponse('ok',content_type='text/plain')
