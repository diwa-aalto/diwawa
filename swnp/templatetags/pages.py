from django import template
from django.utils.safestring import SafeString
from swnp.models import ExtendedFlatPage
register = template.Library()
@register.simple_tag
def show_ordered_flatpages_menu(flatpage_id):
    flatPages = ExtendedFlatPage.objects.all().order_by('show_after')
    myString = ""
    for myPage in flatPages:
        print flatpage_id,myPage.id
        myString += page_li( myPage, flatpage_id==myPage.id )
    return myString

def page_li( thePage, active ):
    return """<li %s><a href="%s" title="%s">%s</a></li>""" % ( 'class="active"' if active else '',thePage.url, thePage.alt_text, thePage.title )

@register.simple_tag
def show_ordered_flatpages_content():
    flatPages = ExtendedFlatPage.objects.all().order_by('show_after')
    myString = ""
    for myPage in flatPages:
        myString += page_content( myPage )
    return myString

def page_content( thePage ):
    return """<section class="frame" id="%s"><div class="page"><div class="page-region"><div class="page-region-content">%s</div></div></div></section>""" % ( thePage.title.lower(),  SafeString(thePage.content) )