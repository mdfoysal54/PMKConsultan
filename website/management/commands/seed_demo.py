from django.core.management.base import BaseCommand
from website.models import SiteSettings,Service,Industry,Section
class Command(BaseCommand):
    help='Load starter content without overwriting existing edits'
    def handle(self,*args,**kwargs):
        SiteSettings.objects.get_or_create(pk=1)
        for i,(title,icon,description) in enumerate([
            ('Web Engineering','◇','Beautiful, accessible, high-performance websites and e-commerce.'),
            ('Business Software','▣','ERP, CRM, POS, inventory, HR and custom platforms.'),
            ('Mobile Applications','◈','Purpose-built mobile experiences with reliable APIs.'),
            ('AI & Automation','✳','Practical automation, assistants and data workflows.'),
            ('Cloud & DevOps','⬡','Resilient deployment, infrastructure and monitoring.'),
            ('Security Engineering','✦','Secure development, assessment and architecture.')]):
            from django.utils.text import slugify
            Service.objects.get_or_create(slug=slugify(title),defaults={'title':title,'icon':icon,'short_description':description,'order':i})
        for i,name in enumerate(['E-commerce & retail','Healthcare & clinics','Education','Professional services','Logistics & distribution','Startups & SaaS']):
            from django.utils.text import slugify
            Industry.objects.get_or_create(slug=slugify(name),defaults={'name':name,'summary':'Tailored software and digital operations for '+name.lower(),'order':i})
        Section.objects.get_or_create(key='home-hero',defaults={'eyebrow':'TECHNOLOGY WITH PURPOSE','heading':'Build boldly. Scale confidently.','body':'Secure digital experiences and software built for ambitious organizations.'})
        self.stdout.write(self.style.SUCCESS('Starter content is ready.'))
