from django import template
from django.utils.safestring import SafeString
from swnp.models import ExtendedFlatPage
register = template.Library()


@register.simple_tag
def show_ordered_flatpages_menu(flatpage_id):
    """ Prints flatpages as li items for navigation
    
        :param flatpage_id: The id of the current page
        :type flatpage_id: Integer
    
     """
    flatPages = ExtendedFlatPage.objects.all().order_by('show_after')
    myString = ""
    for myPage in flatPages:
        myString += page_li(myPage, flatpage_id == myPage.id)
    return myString

def page_li(thePage, active):
    """ Creates a li item from a flatpage 
    
        :param thePage: The FlatPage 
        :type thePage: :class:`swnp.models.ExtendedFlatPage`
        :param active: Is the page currently selected page
        :type active: Bool
    """
    return """<li %s><a href="%s" title="%s">%s</a></li>""" % (
                                                               'class="active"'
                                                               if active else '',
                                                               thePage.url,
                                                               thePage.alt_text,
                                                               thePage.title)

@register.simple_tag
def show_ordered_flatpages_content():
    """  Prints FlatPage contents as section tabs. """
    flatPages = ExtendedFlatPage.objects.all().order_by('show_after')
    myString = ""
    for myPage in flatPages:
        myString += page_content(myPage)
    return myString

def page_content(thePage):
    """ Creates a section tab for a page.
        
        :param thePage: The FlatPage
        :type thePage: :class:`swnp.models.ExtendedFlatPage`
    """
    pstring = ('<section class="frame" id="%s"><div class="page">' +
               '<div class="page-region">' +
               '<div class="page-region-content">%s</div>' +
               '</div></div></section>')
    title = thePage.title.lower()
    content = thePage.content

    return pstring % (title, content)
