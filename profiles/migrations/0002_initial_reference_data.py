from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')

    # Create company records if they don't already exist
    if not Company.objects.exists():
        Company.objects.create(
            name='Tech Corp',
            description='A leading technology company',
            industry='Information Technology',
            access_key_hash=make_password("techcorp_secret")
        )
        Company.objects.create(
            name='Finance Inc',
            description='Provider of finance services',
            industry='Finance',
            access_key_hash=make_password("financeinc_secret")
        )
        Company.objects.create(
            name='MediSolutions',
            description='Healthcare software solutions',
            industry='Healthcare',
            access_key_hash=make_password("medisolutions_secret")
        )
        Company.objects.create(
            name='EduWorld',
            description='Educational platform provider',
            industry='Education',
            access_key_hash=make_password("eduworld_secret")
        )
        Company.objects.create(
            name='ECom Global',
            description='Large e-commerce aggregator',
            industry='E-commerce',
            access_key_hash=make_password("ecomglobal_secret")
        )
        Company.objects.create(
            name='GreenEnergy',
            description='Renewable energy solutions',
            industry='Energy',
            access_key_hash=make_password("greenenergy_secret")
        )
        Company.objects.create(
            name='AgroFarm',
            description='Agricultural services and technology',
            industry='Agriculture',
            access_key_hash=make_password("agrofarm_secret")
        )
        Company.objects.create(
            name='Travel Explore',
            description='Travel and tourism company',
            industry='Travel',
            access_key_hash=make_password("travelexplore_secret")
        )

    # Create several industries if they don't already exist
    # List of industry names
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
        obj, created = CatalogIndustry.objects.get_or_create(name=ind_name)
        created_industries[ind_name] = obj

    # Create fields (CatalogField). For each industry, multiple focus areas
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

    # Populate CatalogField
    for industry_name, field_list in fields_data.items():
        industry_obj = created_industries[industry_name]
        for field_name in field_list:
            CatalogField.objects.get_or_create(industry=industry_obj, name=field_name)


def reverse_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')
    Company.objects.all().delete()
    CatalogField.objects.all().delete()
    CatalogIndustry.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),  # Specify the correct dependency on your initial migration
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
