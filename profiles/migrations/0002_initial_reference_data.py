from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')

    # Creating industries
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
    for ind_name in industries_data:
        obj, _ = CatalogIndustry.objects.get_or_create(name=ind_name)
        created_industries[ind_name] = obj

    # Create company records using created industries
    if not Company.objects.exists():
        tech_corp = Company.objects.create(
            name='Tech Corp',
            description='A leading technology company',
            industry=created_industries.get('Information Technology'),
            access_key_hash=make_password("techcorp_secret")
        )
        Company.objects.create(
            name='Finance Inc',
            description='Provider of finance services',
            industry=created_industries.get('Finance'),
            access_key_hash=make_password("financeinc_secret")
        )
        Company.objects.create(
            name='MediSolutions',
            description='Healthcare software solutions',
            industry=created_industries.get('Healthcare'),
            access_key_hash=make_password("medisolutions_secret")
        )
        Company.objects.create(
            name='EduWorld',
            description='Educational platform provider',
            industry=created_industries.get('Education'),
            access_key_hash=make_password("eduworld_secret")
        )
        Company.objects.create(
            name='ECom Global',
            description='Large e-commerce aggregator',
            industry=created_industries.get('E-commerce'),
            access_key_hash=make_password("ecomglobal_secret")
        )
        Company.objects.create(
            name='GreenEnergy',
            description='Renewable energy solutions',
            industry=created_industries.get('Energy'),
            access_key_hash=make_password("greenenergy_secret")
        )
        Company.objects.create(
            name='AgroFarm',
            description='Agricultural services and technology',
            industry=created_industries.get('Agriculture'),
            access_key_hash=make_password("agrofarm_secret")
        )
        Company.objects.create(
            name='Travel Explore',
            description='Travel and tourism company',
            industry=created_industries.get('Travel'),
            access_key_hash=make_password("travelexplore_secret")
        )

    # Create records in CatalogField for each industry
    fields_data = {
        'Information Technology': [
            'Software Development',
            'Data Science',
            'Cloud Infrastructure',
            'AI/ML',
            'Cybersecurity'
        ],
        'Finance': [
            'Banking',
            'Investment',
            'Risk Management',
            'Trading',
            'Accounting'
        ],
        'Healthcare': [
            'Nursing',
            'Telemedicine',
            'Medical Devices',
            'Health Informatics'
        ],
        'Education': [
            'E-learning',
            'Curriculum Development',
            'Educational Technology'
        ],
        'E-commerce': [
            'Supply Chain Management',
            'Online Marketing',
            'Web Analytics',
            'Product Management'
        ],
        'Energy': [
            'Renewable Energy',
            'Smart Grid',
            'Energy Trading'
        ],
        'Agriculture': [
            'AgroTech',
            'Sustainability',
            'Crop Science'
        ],
        'Travel': [
            'Tour Operations',
            'Hospitality',
            'Destination Management'
        ],
        'Manufacturing': [
            'Industrial Automation',
            'Quality Control',
            'Lean Manufacturing'
        ],
        'Real Estate': [
            'Property Management',
            'Real Estate Investment',
            'Urban Planning'
        ],
    }

    created_fields = {}
    for industry_name, field_list in fields_data.items():
        industry_obj = created_industries.get(industry_name)
        if industry_obj:
            for field_name in field_list:
                field_obj, _ = CatalogField.objects.get_or_create(industry=industry_obj, name=field_name)
                # Let's save some fields for further linking of companies
                # For example, for the IT industry - let's save the first two directions
                if industry_name == 'Information Technology' and field_name in ['Software Development', 'Data Science']:
                    created_fields[field_name] = field_obj

    # Link specializations for Tech Corp
    # If the company does not already have specializations, add them from the created directions
    try:
        tech_corp = Company.objects.get(name='Tech Corp')
        if tech_corp.specializations.count() == 0:
            for spec in created_fields.values():
                tech_corp.specializations.add(spec)
    except Company.DoesNotExist:
        pass

def reverse_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')
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
