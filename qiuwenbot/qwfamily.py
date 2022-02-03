from pywikibot import family


class QiuwenFamily(family.Family):
    """Qiuwen faimily"""
    name = 'qiuwen'
    langs = {
        'zh': 'zhqw.qiuwen.wiki'
    }

    def scriptpath(self, code):
        return ''

    def protocol(self, code):
        return 'HTTPS'

    def isPublic(self):
        return False


family.Family._families['qiuwen'] = QiuwenFamily()
