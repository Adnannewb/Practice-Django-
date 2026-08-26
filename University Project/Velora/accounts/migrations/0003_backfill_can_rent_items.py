"""Back-fill can_rent_items based on the user's existing role.

Sellers (lender-only) default to False so they can't book rentals.
Customers default to True so they can rent.
"""
from django.db import migrations


def forwards(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(role="seller").update(can_rent_items=False)
    User.objects.filter(role="customer").update(can_rent_items=True)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_can_rent_items"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]