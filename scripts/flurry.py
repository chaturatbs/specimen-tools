# Copyright 2018 Jose Cambronero and Phillip Stanley-Marbell
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from argparse import ArgumentParser
from datetime import datetime, timedelta
import json
import os
import requests
import sys

class SpecimenDownloader:
    """
    Download monthly csv reports for specimen from flurry
    """
    # some general constants
    DUMMY_SESSION_ID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    INPUT_DATE_FORMAT = "%m/%d/%Y"
    GET_DATE_FORMAT = "%Y_%m_%d"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.auth_url = 'https://auth.flurry.com/auth/v1/session'
        self.login_url = 'https://login.flurry.com'
        self.auth_method = 'application/vnd.api+json'
        self.session = requests.Session()

    def login(self):
        """ Login in to flurry """
        opts_response = self.session.options(self.auth_url, data='')
        headers = opts_response.headers
        headers.update(
            {
                'origin': self.login_url,
                'referer': self.login_url,
                'accept': self.auth_method,
                'content-type': self.auth_method
            }
        )

        data = {'data': {'type': 'session', 'id': SpecimenDownloader.DUMMY_SESSION_ID, 'attributes': {'scopes': '', 'email': self.email, 'password': self.password, 'remember': 'false'}}}
        payload = json.dumps(data)

        login_response = self.session.post(self.auth_url, data = payload, headers = headers)
        if not login_response.ok:
            raise Exception("Unable to connect: %s" % login_response.status_code)

        old_site_response = self.session.get('https://dev.flurry.com/home.do')
        if not old_site_response.ok:
            raise Exception("Unable to reach old Flurry: %s" % login_response.status_code)

    def __download__(self, start_date, end_date, dir):
        """ Download a single file """
        # preparing data for GET request
        params = {'projectID': 687883, 'versionCut':'versionsAll', 'childProjectId': 0, 'stream': 'true', 'direction': 1, 'offset': 0}
        start_date = self.date_to_flurry(start_date)
        end_date = self.date_to_flurry(end_date)
        params['intervalCut'] = "customInterval%s-%s" % (start_date, end_date)

        print("Requesting %s-%s" % (start_date, end_date))
        download = self.session.get("https://dev.flurry.com/eventsLogCsv.do", params = params)
        if download.ok:
            file_name = os.path.join(dir, "specimen-%s-%s.csv" % (start_date, end_date))
            file = open(file_name, "w")
            file.write(download.text)
            file.close()
        else:
            raise Exception("Unable to download file for %s-%s" % (start_date, end_date))

    def __seq_dates__(self, start_date, end_date):
        """ Return list of pairs consecutive dates between start and end dates, inclusive both ends"""
        pairs = []
        if end_date < start_date:
            raise ValueError("start must be <= end: %s - %s" % (start_date.date(), end_date.date()))
        curr_date = start_date
        while curr_date <= end_date:
            next_date = curr_date + timedelta(days = 1)
            pairs.append((curr_date, next_date))
            curr_date = next_date
        return pairs

    def check_input_date(self, date):
        """ if input not a valid datetime, parse as such """
        if not isinstance(date, datetime):
            return datetime.strptime(date, SpecimenDownloader.INPUT_DATE_FORMAT)
        return date

    def date_to_flurry(self, date):
       return datetime.strftime(date, SpecimenDownloader.GET_DATE_FORMAT)

    def download(self, start_date, end_date, dir_name):
        """ Download all csv reports between start and end date and store to dir directory"""
        print("Downloading daily csv files [%s, %s] to %s" % (start_date, end_date, dir_name))
        start_date = self.check_input_date(start_date)
        end_date = self.check_input_date(end_date)
        self.login()
        dates = self.__seq_dates__(start_date, end_date)
        for start, end in dates:
            try:
                self.__download__(start, end, dir_name)
            except Exception as e:
                print(e.message)

def main(args):
    downloader = SpecimenDownloader(args.email, args.password)
    downloader.download(args.start_date, args.end_date, args.dir)


if __name__ == "__main__":
    argparser = ArgumentParser(description='Download CSVs from Specimen Flurry account (requires proper authentication)')
    argparser.add_argument('email', type=str, help='Email for Flurry account')
    argparser.add_argument('password', type=str, help='Password for Flurry account')
    argparser.add_argument('start_date', type=str, help='Start date for download (mm/dd/yyyy)')
    argparser.add_argument('end_date', type=str, help='End date for download (mm/dd/yyyy)')
    argparser.add_argument('-d', '--dir', type=str, help='Directory for download, if not provided defaults to current directory', default='.')

    args = argparser.parse_args()
    main(args)
