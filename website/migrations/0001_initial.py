from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='SiteSettings', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('company_name',models.CharField(default='PMK Consultancy',max_length=120)),
            ('tagline',models.CharField(default='Engineering trust. Building tomorrow.',max_length=180)),
            ('hero_title',models.CharField(default='Digital products that move businesses forward.',max_length=220)),
            ('hero_description',models.TextField(default='We design and engineer modern websites, applications and business systems with security at the foundation.',max_length=600)),
            ('primary_color',models.CharField(default='#386df3',help_text='Hex color, e.g. #386df3',max_length=7)),
            ('contact_email',models.EmailField(default='hello@example.com',max_length=254)),
            ('facebook_url',models.URLField(blank=True)),
            ('logo',models.ImageField(blank=True,null=True,upload_to='branding/')),
            ('favicon',models.ImageField(blank=True,null=True,upload_to='branding/')),
            ('updated_at',models.DateTimeField(auto_now=True))]),
        migrations.CreateModel(name='Section',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('key',models.SlugField(help_text='Example: home-hero, services-hero, about-hero',unique=True)),
            ('eyebrow',models.CharField(blank=True,max_length=100)),
            ('heading',models.CharField(max_length=200)),('body',models.TextField(blank=True)),
            ('background',models.ImageField(blank=True,null=True,upload_to='sections/')),
            ('enabled',models.BooleanField(default=True)),('updated_at',models.DateTimeField(auto_now=True))]),
        migrations.CreateModel(name='Service',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('title',models.CharField(max_length=120)),('slug',models.SlugField(unique=True)),
            ('short_description',models.TextField(max_length=420)),('icon',models.CharField(default='✦',max_length=24)),
            ('order',models.PositiveSmallIntegerField(default=0)),('published',models.BooleanField(default=True))],
            options={'ordering':['order','title']}),
        migrations.CreateModel(name='Industry',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('name',models.CharField(max_length=100)),('slug',models.SlugField(unique=True)),
            ('summary',models.TextField(max_length=320)),('order',models.PositiveSmallIntegerField(default=0)),
            ('published',models.BooleanField(default=True))],options={'ordering':['order','name']}),
        migrations.CreateModel(name='Inquiry',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('name',models.CharField(max_length=120)),('email',models.EmailField(max_length=254)),
            ('company',models.CharField(blank=True,max_length=160)),
            ('service',models.CharField(choices=[('website','Website / E-commerce'),('software','Custom Software / ERP'),('mobile','Mobile Application'),('security','Security / Cloud'),('ai','AI / Automation'),('other','Other / Not sure')],max_length=30)),
            ('budget',models.CharField(blank=True,max_length=60)),('details',models.TextField(max_length=4000)),
            ('created_at',models.DateTimeField(auto_now_add=True,db_index=True)),
            ('status',models.CharField(choices=[('new','New'),('qualified','Qualified'),('proposal','Proposal sent'),('won','Won'),('lost','Lost'),('spam','Spam')],default='new',max_length=20)),
            ('internal_notes',models.TextField(blank=True))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='Portfolio',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('title',models.CharField(max_length=150)),('category',models.CharField(max_length=90)),
            ('summary',models.TextField(max_length=450)),('slug',models.SlugField(unique=True)),
            ('image',models.ImageField(blank=True,null=True,upload_to='portfolio/')),
            ('demo_url',models.URLField(blank=True)),('is_published',models.BooleanField(default=False)),
            ('is_demo',models.BooleanField(default=True,help_text='Concepts must be labeled as demos')),
            ('featured',models.BooleanField(default=False)),('created_at',models.DateTimeField(auto_now_add=True))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='AuditEvent',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('actor',models.CharField(max_length=150)),('action',models.CharField(max_length=20)),
            ('model',models.CharField(max_length=120)),('object_id',models.CharField(max_length=120)),
            ('summary',models.CharField(max_length=250)),('timestamp',models.DateTimeField(auto_now_add=True,db_index=True))],options={'ordering':['-timestamp']}),
    ]
