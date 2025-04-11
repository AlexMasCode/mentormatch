from django.db import migrations

def create_initial_data(apps, schema_editor):
    Company = apps.get_model('profiles', 'Company')
    CatalogIndustry = apps.get_model('profiles', 'CatalogIndustry')
    CatalogField = apps.get_model('profiles', 'CatalogField')

    # Создаём записи для компаний, если их еще нет:
    if not Company.objects.exists():
        Company.objects.create(
            name='Tech Corp',
            description='A leading technology company',
            industry='Information Technology'
        )
        Company.objects.create(
            name='Finance Inc',
            description='Provider of finance services',
            industry='Finance'
        )
        Company.objects.create(
            name='MediSolutions',
            description='Healthcare software solutions',
            industry='Healthcare'
        )
        Company.objects.create(
            name='EduWorld',
            description='Educational platform provider',
            industry='Education'
        )
        Company.objects.create(
            name='ECom Global',
            description='Large e-commerce aggregator',
            industry='E-commerce'
        )
        Company.objects.create(
            name='GreenEnergy',
            description='Renewable energy solutions',
            industry='Energy'
        )
        Company.objects.create(
            name='AgroFarm',
            description='Agricultural services and technology',
            industry='Agriculture'
        )
        Company.objects.create(
            name='Travel Explore',
            description='Travel and tourism company',
            industry='Travel'
        )

    # Создаём несколько индустрий, если их нет:
    # Список индустрий с названиями
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

    # Создаём поля (CatalogField). Для каждой индустрии несколько направлений.
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

    # Заполняем CatalogField
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
        ('profiles', '0001_initial'),  # Укажите корректную зависимость от вашей первичной миграции
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
