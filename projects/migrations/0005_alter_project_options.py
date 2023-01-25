
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_merge_0003_project_featured_image_0003_project_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['created']},
        ),
    ]
