import os
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_data(apps, schema_editor):
    # Get models
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')

    # 1) Create industries
    industries_data = [
        'Information Technology',
        'Finance',
        'Healthcare',
        'Education',
        'E-commerce',
        'Energy',
        'Agriculture',
        'Travel',
        'Manufacturing',
        'Real Estate'
    ]
    created_industries = {}
    for name in industries_data:
        obj, _ = CatalogIndustry.objects.get_or_create(name=name)
        created_industries[name] = obj

    # 2) Create companies with access keys from environment
    secret_map = {
        'Tech Corp':      os.environ.get('TECHCORP_ACCESS_KEY'),
        'Finance Inc':    os.environ.get('FINANCEINC_ACCESS_KEY'),
        'MediSolutions':  os.environ.get('MEDISOLUTIONS_ACCESS_KEY'),
        'EduWorld':       os.environ.get('EDUWORLD_ACCESS_KEY'),
        'ECom Global':    os.environ.get('ECOMGLOBAL_ACCESS_KEY'),
        'GreenEnergy':    os.environ.get('GREENENERGY_ACCESS_KEY'),
        'AgroFarm':       os.environ.get('AGROFARM_ACCESS_KEY'),
        'Travel Explore': os.environ.get('TRAVELEXPLORE_ACCESS_KEY'),
    }
    industry_map = {
        'Tech Corp':      'Information Technology',
        'Finance Inc':    'Finance',
        'MediSolutions':  'Healthcare',
        'EduWorld':       'Education',
        'ECom Global':    'E-commerce',
        'GreenEnergy':    'Energy',
        'AgroFarm':       'Agriculture',
        'Travel Explore': 'Travel',
    }

    if not Company.objects.exists():
        for comp_name, key in secret_map.items():
            Company.objects.create(
                name=comp_name,
                description=f"{comp_name} description…",
                industry=created_industries[industry_map[comp_name]],
                access_key_hash=make_password(key) if key else None
            )

    # 3) Create catalog fields
    fields_data = {
        'Information Technology': [
            'Software Development', 'Data Science', 'Cloud Infrastructure', 'AI/ML', 'Cybersecurity'
        ],
        'Finance': [
            'Banking', 'Investment', 'Risk Management', 'Trading', 'Accounting'
        ],
        'Healthcare': [
            'Nursing', 'Telemedicine', 'Medical Devices', 'Health Informatics'
        ],
        'Education': [
            'E-learning', 'Curriculum Development', 'Educational Technology'
        ],
        'E-commerce': [
            'Supply Chain Management', 'Online Marketing', 'Web Analytics', 'Product Management'
        ],
        'Energy': [
            'Renewable Energy', 'Smart Grid', 'Energy Trading'
        ],
        'Agriculture': [
            'AgroTech', 'Sustainability', 'Crop Science'
        ],
        'Travel': [
            'Tour Operations', 'Hospitality', 'Destination Management'
        ],
        'Manufacturing': [
            'Industrial Automation', 'Quality Control', 'Lean Manufacturing'
        ],
        'Real Estate': [
            'Property Management', 'Real Estate Investment', 'Urban Planning'
        ],
    }
    created_fields = {}
    for industry_name, field_list in fields_data.items():
        for field_name in field_list:
            field_obj, _ = CatalogField.objects.get_or_create(
                industry=created_industries[industry_name],
                name=field_name
            )

            if industry_name == 'Information Technology' and field_name in ['Software Development', 'Data Science']:
                created_fields[field_name] = field_obj

    # 4) Link Tech Corp specializations
    try:
        tech = Company.objects.get(name='Tech Corp')
        if tech.specializations.count() == 0:
            tech.specializations.set(created_fields.values())
    except Company.DoesNotExist:
        pass


def reverse_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogField = apps.get_model('profiles', 'CatalogField')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    # Remove all created data
    Company.objects.all().delete()
    CatalogField.objects.all().delete()
    CatalogIndustry.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
