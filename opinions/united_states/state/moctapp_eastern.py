from datetime import date
import mo


class Site(mo.Site):
    def __init__(self):
        super(Site, self).__init__()
        today = date.today()
        self.url = 'https://www.courts.mo.gov/page.jsp?id=12086&dist=Opinions Eastern&date=all&year=%s#all' % today.year
        self.court_id = self.__module__

    def _get_divisions(self):
        return ['Eastern Dist.'] * len(self.case_names)
