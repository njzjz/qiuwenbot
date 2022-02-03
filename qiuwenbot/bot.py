import pywikibot
from .qwfamily import QiuwenFamily as _

def login(user: str, password: str) -> pywikibot.Site:
    """Login to qiuwen.
    
    Parameters
    ----------
    user
        username of the bot
    password
        password of the bot
    
    Returns
    -------
    pywikibot.Site
        qiuwen site
    """
    site = pywikibot.Site(
        code="zh",
        fam="qiuwen",
        user=user,
    )
    pywikibot.data.api.LoginManager(site=site,user=user,password=password).login()
    return site

def get_page(title: str, site: pywikibot.Site):
    """Get the page with the specific title.
    
    Parameters
    ----------
    title : str
        title of the page
    site : pywikibot.Site
        qiuwen site
    """
    return pywikibot.Page(site, title)
