from bs4 import BeautifulSoup
import requests
from scrapy.linkextractors import LinkExtractor
from crawler.items import BotItem
from scrapy.spiders import CrawlSpider, Rule


# the purpose of this class is to crawl possible list on Wikipedia and extract list of peoole
class Wikispider(CrawlSpider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    cached_results = {}
    current = ''

    def __init__(self):
        # get initial list
        people_list = self.fetch_lists("https://en.wikipedia.org/wiki/Lists_of_people_by_occupation")
        self.start_urls = []
        # append list url to start list
        for key in people_list:
            self.start_urls.append('https://en.wikipedia.org'+people_list[key])
        # set rules for different url form
        page_lx = LinkExtractor(allow=('https://en.wikipedia.org/wiki/List_of_'), )
        profile_page_lx = LinkExtractor(allow=(r'https://en.wikipedia.org/wiki/Lists_of'), )
        self.rules = (
            # if list, get people on the list
            Rule(page_lx, callback='parse_profile', follow=False),
            # if list of list, get lists on the list
            Rule(profile_page_lx, follow=True),
        )
        super(Wikispider, self).__init__()

    # the purpose of the method is to get all the list from the start page
    def fetch_lists(self, entry_url):
        response = requests.get(entry_url)
        text = response.text
        soup = BeautifulSoup(text, "html5lib")
        list_ul = soup.find(id='mw-content-text').ul
        list_links = {}
        # get list in tag <li>
        for li in list_ul.find_all('li'):
            a = li.a
            if not a:
                continue
            list_link = a.get('href')
            if list_link.startswith('/wiki/'):
                list_links[self.get_list_name(list_link)] = list_link
        return list_links

    # the purpose of the method is to get the name of the list according to the url
    def get_list_name(self, url):
        wiki_free = url.split('/wiki/').pop()
        list_free = wiki_free.split('List_of_').pop()
        lists_free = list_free.split('Lists_of_').pop()
        anchor_free = lists_free.split('#')[0]
        return anchor_free.lower()

    # the purpose of the method is to parse the current response
    def parse_profile(self, response):
        # get item
        item = BotItem()
        item['name'] = []
        item['address'] = []
        item['fromlist'] = self.get_list(response)
        people = self.get_people_from_page(response)
        # store list in item
        for key in people:
            item['name'].append(key)
            item['address'].append(people[key])
        yield item

    # the purpose of the method is to get name of the list
    def get_list(self,response):
        page_soup = self.get_soup(response)
        name = page_soup.head.title.string
        return name

    # the purpose of the method is to get people from list of people
    def get_people_from_page(self, response):
        page_soup = self.get_soup(response)
        if page_soup is None:
            # another chance
            print('error'),
            return {}
        # eliminate irrelevant tags
        self.remove_irrelevant_tags(page_soup)
        people = self.get_people(page_soup)
        return people

    # possible class name of irrelevant tags
    def remove_irrelevant_tags(self, page_soup):
        irrelevant_tag_classes = [
            'thumb',
            'dablink',
            'plainlinks',
            'noprint',
            'tright',
            'portal',
            'rellink',
            'boilerplate',
            'seealso'
        ]
        for tag_class in irrelevant_tag_classes:
            self.remove_tags_by_class(page_soup, tag_class)

    # method to remove tags according to class
    def remove_tags_by_class(self, page_soup, class_name):
        [s.extract() for s in page_soup.find_all(class_=class_name)]

    # method to remove get soup object
    def get_soup(self, response):
        text = response.text
        return BeautifulSoup(text, "html5lib")

    # method not used yet!!
    def get_sibling_list_after_element_with_id(self, page_soup, element_id):
        element = page_soup.find(id=element_id)
        people = {}
        if element:
            people_ul = element.parent.find_next_sibling()
            if people_ul:
                for li in people_ul.find_all('li'):
                    try:
                        people[li.a.text] = 'http://en.wikipedia.org' + li.a.get('href')
                    except AttributeError:
                        pass
        return people

    # iterate different kinds of tag combination
    def get_people(self, page_soup):
        result = self.get_people_from_tag(page_soup, 'ul', 'li')
        result.update(self.get_people_from_tag(page_soup, 'ol', 'li'))
        result.update(self.get_people_from_tag(page_soup, 'dl', 'dd'))
        result.update(self.get_people_from_tag(page_soup, 'table', 'li'))
        result.update(self.get_people_from_tag(page_soup, 'table', 'tr'))
        return result

    # get item from certain list_tag and item_tag
    def get_people_from_tag(self, page_soup, list_tag, item_tag):
        # get the section which have the list
        all_lists = page_soup.find(id='mw-content-text').find_all(list_tag)
        people = {}
        # check every list_tag
        for list_tag in all_lists:
            # get the previous sibling
            header = list_tag.find_previous_sibling()
            if not header:
                # get the parent tag's previous sibling
                header = list_tag.parent.find_previous_sibling()
            # check the name of the previous sibling to eliminate interference
            if header and not header.name in ['h2', 'h3', 'p', 'dl']:
                continue
            # check the class of the previous sibling to eliminate interference
            if header and not header.find(id='External_links') and not header.find(id='References'):
                for li in list_tag.find_all(item_tag):
                    try:
                        # get the candidate link
                        [s.extract() for s in li.find_all('span')]
                        candidate_link = li.a.get('href')
                        # check the form of the candidate link
                        if not '/wiki/' in candidate_link:
                            continue
                        is_another_list = 'List_of' in candidate_link or 'Lists_of' in candidate_link
                        # insert the data
                        if not is_another_list and not header.find(id='See_also'):
                            people[li.a.text] = 'http://en.wikipedia.org' + candidate_link
                        # elif not candidate_link in self.list_links.items() + list(self.visited_links):
                        # elif not candidate_link in self.start_urls:
                        #     self.start_urls.append(candidate_link)
                            # self.visited_links.add(candidate_link)
                    except AttributeError:
                        pass
        return people







