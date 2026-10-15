from django.db import models
from django.core.validators import FileExtensionValidator

class SiteSettings(models.Model):
    company_name=models.CharField(max_length=120,default='PMK Consultancy')
    tagline=models.CharField(max_length=180,default='Engineering trust. Building tomorrow.')
    hero_title=models.CharField(max_length=220,default='Digital products that move businesses forward.')
    hero_description=models.TextField(max_length=600,default='We design and engineer modern websites, applications and business systems with security at the foundation.')
    primary_color=models.CharField(max_length=7,default='#386df3',help_text='Hex color, e.g. #386df3')
    contact_email=models.EmailField(default='hello@example.com')
    facebook_url=models.URLField(blank=True)
    logo=models.ImageField(upload_to='branding/',blank=True,null=True)
    favicon=models.ImageField(upload_to='branding/',blank=True,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return 'Corporate site configuration'
    def save(self,*args,**kwargs):
        self.pk=1
        super().save(*args,**kwargs)

class Section(models.Model):
    key=models.SlugField(unique=True,help_text='Example: home-hero, services-hero, about-hero')
    eyebrow=models.CharField(max_length=100,blank=True)
    heading=models.CharField(max_length=200)
    body=models.TextField(blank=True)
    background=models.ImageField(upload_to='sections/',blank=True,null=True)
    enabled=models.BooleanField(default=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.key

class Service(models.Model):
    title=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    short_description=models.TextField(max_length=420)
    icon=models.CharField(max_length=24,default='✦')
    order=models.PositiveSmallIntegerField(default=0)
    published=models.BooleanField(default=True)
    def __str__(self): return self.title
    class Meta: ordering=['order','title']

class Industry(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    summary=models.TextField(max_length=320)
    order=models.PositiveSmallIntegerField(default=0)
    published=models.BooleanField(default=True)
    class Meta: ordering=['order','name']
    def __str__(self): return self.name

class Inquiry(models.Model):
    SERVICE_CHOICES=[('website','Website / E-commerce'),('software','Custom Software / ERP'),('mobile','Mobile Application'),('security','Security / Cloud'),('ai','AI / Automation'),('other','Other / Not sure')]
    STATUS=[('new','New'),('qualified','Qualified'),('proposal','Proposal sent'),('won','Won'),('lost','Lost'),('spam','Spam')]
    name=models.CharField(max_length=120)
    email=models.EmailField()
    company=models.CharField(max_length=160,blank=True)
    service=models.CharField(max_length=30,choices=SERVICE_CHOICES)
    budget=models.CharField(max_length=60,blank=True)
    details=models.TextField(max_length=4000)
    created_at=models.DateTimeField(auto_now_add=True,db_index=True)
    status=models.CharField(max_length=20,choices=STATUS,default='new')
    internal_notes=models.TextField(blank=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.name} — {self.get_service_display()}'

class Portfolio(models.Model):
    title=models.CharField(max_length=150)
    category=models.CharField(max_length=90)
    summary=models.TextField(max_length=450)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to='portfolio/',blank=True,null=True)
    demo_url=models.URLField(blank=True)
    is_published=models.BooleanField(default=False)
    is_demo=models.BooleanField(default=True,help_text='Concepts must be labeled as demos')
    featured=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return self.title

class AuditEvent(models.Model):
    actor=models.CharField(max_length=150)
    action=models.CharField(max_length=20)
    model=models.CharField(max_length=120)
    object_id=models.CharField(max_length=120)
    summary=models.CharField(max_length=250)
    timestamp=models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta: ordering=['-timestamp']
    def __str__(self): return f'{self.timestamp}: {self.actor} {self.action} {self.model}'
