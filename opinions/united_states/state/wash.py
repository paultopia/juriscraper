from juriscraper.OpinionSite import OpinionSite
from datetime import datetime, timedelta, date
from dateutil.rrule import rrule, MONTHLY


class Site(OpinionSite):
    def __init__(self):
        super(Site, self).__init__()
        self.court_id = self.__module__
        self.start = date.today() - timedelta(days=60)
        self.end = date.today()
        self.url = 'http://www.courts.wa.gov/opinions/index.cfm?fa=opinions.processSearch'
        self.method = 'POST'

        self.courtLevel = 'S'
        self.pubStatus = 'All'
        self._set_parameters()
        self.base = "//tr[../tr/td/strong[contains(., 'File Date')]]"
        self.back_scrape_iterable = [i.date() for i in rrule(
            MONTHLY,
            dtstart=date(2014, 02, 01),
            until=date.today(),
        )]

    def _set_parameters(self):
        self.parameters = {
            'courtLevel': self.courtLevel,
            'pubStatus': self.pubStatus,
            'beginDate': self.start.strftime('%m/%d/%Y'),
            'endDate': self.end.strftime('%m/%d/%Y'),
            'SType': 'Phrase',
            'SValue': ''
        }

    def _get_case_names(self):
        path = "{base}/td[3]/text()".format(base=self.base)
        return list(self.html.xpath(path))

    def _get_docket_numbers(self):
        path = "{base}/td[2]/a/text()".format(base=self.base)
        return list(self.html.xpath(path))

    def _get_case_dates(self):
        path = "{base}/td[1]/text()".format(base=self.base)
        dates = []
        for date_string in self.html.xpath(path):
            dates.append(datetime.strptime(date_string.strip(), '%b. %d, %Y').date())
        return dates

    def _get_download_urls(self):
        path = "{base}/td[2]/a[2]/@href".format(base=self.base)
        return list(self.html.xpath(path))

    def _get_precedential_statuses(self):
        return ["Published"] * len(self.case_names)

    def _download_backwards(self, d):
        self.start = d
        self.end = d + timedelta(days=32)
        self._set_parameters()
        self.html = self._download()



