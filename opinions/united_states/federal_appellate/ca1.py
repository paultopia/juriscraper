from juriscraper.OpinionSite import OpinionSite
import re
import time
from datetime import date
from lxml import html


class Site(OpinionSite):
    def __init__(self):
        super(Site, self).__init__()
        self.url = 'http://media.ca1.uscourts.gov/opinions/opinionrss.php'
        self.court_id = self.__module__

    def _get_case_names(self):
        regex = re.compile("(\d{2}-.*?\W)(.*)")
        case_names = []
        for e in self.html.xpath('//item/title'):
            t = html.tostring(e, method='text')
            case_names.append(regex.search(t).group(2))
        return case_names

    def _get_download_urls(self):
        return [html.tostring(e, method='text') for e in
                self.html.xpath('//item/link')]

    def _get_case_dates(self):
        dates = []
        for e in self.html.xpath('//item/pubdate'):
            date_string = html.tostring(e, method='text').split()[0]
            dates.append(date.fromtimestamp(
                time.mktime(time.strptime(date_string, '%Y-%m-%d'))))
        return dates

    def _get_docket_numbers(self):
        regex = re.compile("(\d{2}-.*?\W)(.*)$")
        return [regex.search(html.tostring(e, method='text')).group(1).strip()
                for e in self.html.xpath('//item/title')]

    def _get_precedential_statuses(self):
        statuses = []
        for e in self.html.xpath("//item/category"):
            text = html.tostring(e, method='text').lower().strip()
            if "unpublished" in text:
                statuses.append("Unpublished")
            elif "published" in text:
                statuses.append("Published")
            elif "errata" in text:
                statuses.append("Errata")
            else:
                statuses.append("Unknown")
        return statuses

    def _get_lower_court_numbers(self):
        regex = re.compile("Originating Case Number:([^<]*)[<]")
        return [regex.search(html.tostring(e)).group(1).strip()
                for e in self.html.xpath('//item/description')]

    def _get_lower_courts(self):
        return [e.strip() for e in
                self.html.xpath('//item/description/b[2]/text()')]
