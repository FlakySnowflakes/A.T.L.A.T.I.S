from bs4 import BeautifulSoup
import requests
import os

results = []
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
headers = {'User-Agent': user_agent}


class ParseTripAdvisor:
    def __init__(self, x):
        self.hotel_name = ''
        self.limit_reviews = x
        self.num_reviews = 0
        self.reviewer_name = ''
        self.review_body = ''
        self.address = ''
        self.info = {}
        self.r = None
        self.check = bool

    def ifHotel_Exist(self):
        PATH = './' + self.hotel_name + '.csv'
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            print("File ", self.hotel_name, " exists and is readable for update")
            return self.check = True
        else:
            print("The file does not exist...\n", 'Creating new file...')
            return self.check = False

    def get_soup(self, url):
        s = requests.Session()
        self.r = s.get(url, headers=headers)
        if self.r.status_code != 200:
            print('status code:', self.r.status_code)
        else:
            soup = BeautifulSoup(self.r.text, 'html.parser')
            return soup

    def parse(self, url, response):
        self.check_response(url, response)
        # Get hotel name
        self.hotel_name = response.find('h1', id='HEADING').text
        # Get hotel address
        self.address = response.find('span', {
                                     'class': 'public-business-listing-ContactInfo__ui_link--1_7Zp public-business-listing-ContactInfo__level_4--3JgmI'}).text
        if self.check == True:
            return
        else:
            pass
        get number of reviews
        self.num_reviews = self.get_num_reviews(response)
        # Limit number of reviews to output
        self.limit_num_reviews()
        # print(self.limit_reviews, ' ', self.num_reviews, '\n')
        # create template for urls to pages with reviews
        url = url.replace('.html', '-or{}.html')
        # load pages with reviews
        for offset in range(0, self.limit_reviews, 5):
            # print('url:', url.format(offset))
            url_ = url.format(offset)
            self.parse_reviews(url_, self.get_soup(url_))
            # return  # for test only - to stop after first page
        return

    def get_num_reviews(self, response):
        nr = response.find_all(
            'span', {'class': 'location-review-review-list-parts-LanguageFilter__paren_count--2vk3f'})[1].text
        nr = nr[1:-1]  # remove `( )`
        nr = nr.replace(',', '')  # remove `,`
        nr = int(nr)
        # print('num_reviews:', nr, type(nr))
        return nr

    def limit_num_reviews(self):
        if self.num_reviews < self.limit_reviews:  # Limit the number of reviews to output
            self.limit_reviews = self.num_reviews
        else:
            pass
        # return limit_reviews

    def check_response(self, url, response):
        if not response:
            print('no response:', url)
            return

    def parse_reviews(self, url, response):
        self.check_response(url, response)
        # get every review
        for idx, review in enumerate(response.find_all('div', {'data-test-target': 'HR_CC_CARD'})):
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

            self.info = {
                'hotel': self.hotel_name,
                'reviewer': self.reviewer_name,
                # 'review_title': review_title,
                'review': self.review_body,
                'address': self.address,
                # 'city': self.city,
                # 'state': self.state,
                # 'country': self.country
            }

            results.append(self.info)
            # return # for test only - to stop after first review
