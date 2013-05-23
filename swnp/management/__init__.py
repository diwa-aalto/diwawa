from django.db.models.signals import post_syncdb
import swnp.models

def check_company(sender, **kwargs):
    if not swnp.models.Company.objects.all().count():
        company_name = raw_input("Enter company name: ")
        company_name = company_name.strip()
        c = swnp.models.Company(name=company_name)
        c.save()
post_syncdb.connect(check_company, sender=swnp.models)