from bs4 import BeautifulSoup
import requests
import os
import re

results = []
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
headers = {'User-Agent': user_agent}


class ParseTripAdvisor:
    def __init__(self, x, city):
        self.hotelName = ''
        self.limit_reviews = x
        self.num_reviews = 0
        self.reviewer_name = ''
        self.review_body = ''
        self.city = city
        self.address = ''
        self.info = {}
        self.r = None

    def HotelExist(self):
        PATH = 'csvFiles/' + self.hotelName + '.csv'
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            return True
        else:
            return False

    def get_soup(self, url):
        s = requests.Session()
        self.r = s.get(url, headers=headers)
        if self.r.status_code != 200:
            print('status code:', self.r.status_code)
        else:
            self.soup = BeautifulSoup(self.r.text, 'html.parser')

    def parse(self, url):
        self.check_response(url)
        # Get hotel name
        self.hotelName = self.soup.find('h1', id='HEADING').text
        if self.HotelExist() == True:
            return
        else:
            pass
        # get number of reviews
        self.get_num_reviews()
        # get hotel address
        self.get_address()
        # Limit number of reviews to output
        self.limit_num_reviews()
        # create template for urls to pages with reviews
        url = url.replace('Reviews', 'Reviews-or{}')
        # load pages with reviews
        for offset in range(0, self.limit_reviews, 5):
            url_ = url.format(offset)
            self.get_soup(url_)
            self.parse_reviews(url_)
            # print('url: ' + url + '\n')
            # return  # for test only - to stop after first page

    def get_address(self):
        self.address = self.soup.find_all('span', {
                                          'class': 'public-business-listing-ContactInfo__ui_link--1_7Zp public-business-listing-ContactInfo__level_4--3JgmI'})[1].text

    def get_num_reviews(self):
        self.num_reviews = self.soup.find_all(
            'span', {'class': 'location-review-review-list-parts-LanguageFilter__paren_count--2vk3f'})[1].text
        self.num_reviews = self.num_reviews[1:-1]  # remove `( )`
        self.num_reviews = self.num_reviews.replace(',', '')  # remove `,`
        self.num_reviews = int(self.num_reviews)

    def limit_num_reviews(self):
        if self.num_reviews < self.limit_reviews:  # Limit the number of reviews to output
            self.limit_reviews = self.num_reviews
        else:
            pass
        # return limit_reviews

    def check_response(self, url):
        if not self.soup:
            print('no response:', url)
            return

    def parse_reviews(self, url):
        self.check_response(url)
        # get every review
        for idx, review in enumerate(self.soup.find_all('div', {'data-test-target': 'HR_CC_CARD'})):
            # Get reviewer name
            self.reviewer_name = review.find(
                'a', {'class': 'ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC'}).text
            # Get the body content of user review without clicking 'read more'
            p = review.find('div', {'class': 'cPQsENeY'}).find('q')
            self.review_body = ''
            for child in p.children:
                if child.name == "span":
                    self.review_body += child.text
                elif child.name == 'None':
                    self.review_body += child.string.rstrip("\"\n ").lstrip("\"\n ")
            # Use regex
            self.review_body = self.correct(self.review_body)
            # Place data in dictionary
            self.info = {
                'hotel': self.hotelName,
                'reviewer': self.reviewer_name,
                'review': self.review_body,
                'city': self.city,
            }

            results.append(self.info)
            # return # for test only - to stop after first review

    def correct(self, s):
        r = re.sub(r'\.(?! )', '. ', re.sub(r' +', ' ', s))
        r = re.sub(r'\. \. \. (?! )', '. ', r)
        r = re.sub(r'\•(?! )', '', s)
        return r
