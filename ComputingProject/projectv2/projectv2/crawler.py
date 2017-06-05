from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import re


# the purpose of this method is to prepare the beautiful soup object to parse
def parse(query):
    # The structure of the query URL is 'https://en.wikipedia.org/wiki/' + name
    BASE_URL = 'https://en.wikipedia.org/wiki/'
    # Replace the space in the input by _
    newquery = str(query).replace(' ', '_')
    # The query URL
    URL = BASE_URL + newquery
    # Get the response and extract html document from the URL
    response = requests.get(URL)
    html_doc = response.text

    soup = BeautifulSoup(html_doc, "html5lib")
    return parse_soup(soup)


# the purpose of this method is to parse the infobox
def parse_soup(soup):
    # The regular expression of infobox
    regex = re.compile("^infobox")
    # list of attributes, extract from <th> tags
    title_list = list()
    # list of contents, extract from <td> tags
    content_list = list()
    # dictionary of item, extract from <tr> tags, contain attribute and content of all the items
    item_dict = dict()
    # i and j are counter which map the attributes to content
    # in case that some <tr> tag does not have <th> tag or <td> tag
    i = 0
    j = 0
    # get the infobox table
    table = soup.find("table", class_=regex)
    if not (table is None):
        # find all <tr> tag in the infobox
        for item in table.find_all('tr'):
            if has_children(item):
                # initial title
                title = ''
                # get the <th> tag in the <tr> tag
                if not (item.th is None):
                    th = item.th
                    # If the title is in the simple form
                    if isinstance(th, NavigableString):
                        title_from_string = th.string
                        if title_from_string is not None:
                            # eliminate the "\xa0" in title string
                            title = title_from_string.replace(u'\xa0', u' ')
                    # If the <th> has children
                    else:
                        # use recursive method
                        title_from_tag = get_title(th)
                        # eliminate the "\xa0" and space in title string
                        title = title_from_tag.replace(u'\xa0', u' ')
                    title_result = title.replace(u'\n', u' ')
                    title_list.append(title_result)
                    # counter plus one due to the <tr> tag has <th> tag
                    i += 1
                else:
                    # if the <tr> tag does not have a <th> tag but has <td> tag
                    if not (item.td is None) and i > 0:
                        # get the tag
                        td = item.td
                        # use the recursive method to get the string and append to the content in the previous <td> tag
                        new_string = ' '.join(content_list[j-1]) + ' ' + ' '.join(recu_children(td))
                        # yield a new content list which contains content from two <td> tags
                        new_list = [new_string]
                        # add to content list
                        content_list[j-1] = new_list
                        # add to item dictionary
                        item_dict[title_list[i-1]] = new_list
                # if the <tr> tag contains both <th> tag and <td> tag
                if i == j+1:
                    if not (item.td is None):
                        # get content in <td> tag
                        td = item.td
                        td_list = recu_children(td)
                        content_list.append(td_list)
                        item_dict[title_list[j]] = td_list
                    else:
                        # no information in tag
                        item_dict[title_list[j]] = ' '
                        content_list.append(' ')
                    j += 1
            # print("\n")
    print(title_list)
    print(item_dict)
    result_list = {}
    # save all the item as string
    for key in item_dict:
        item = ' '.join(item_dict[key])
        result_list[key] = str(item)
    return result_list


# the purpose of this method is to check whether the tag has a children tag
def has_children(tag):
    return tag.children is not None


# the purpose of this method is to check whether the tag contains object
def has_contents(tag):
    return not len(tag.contents) == 1


# the purpose of this method is to get the attribute recursively
def get_title(tag):
    subtitle_list = []
    if not isinstance(tag, NavigableString):
        for child in tag.descendants:
            if isinstance(child, NavigableString):
                subtitle_list.append(child)
    newtitle = ''.join(subtitle_list)
    return newtitle


# the purpose of this method is to get the content recursively
def recu_children(tag):
    child_list = list()
    regex = re.compile(r'^\[\d+\]$')
    if not isinstance(tag, NavigableString):
        # if has_contents(tag):
            for child in tag.descendants:
                # eliminate <sup> tags
                if child is not None and not child.name == 'sup' and not child.parent.name == 'sup':
                    if isinstance(child, NavigableString):
                        # extract raw string
                        raw_string = child
                        if raw_string is not None:
                            # replace space and using regular expression to eliminate "[]"
                            raw_string_new = raw_string.replace(u'\n', u' ')
                            child_string = raw_string_new.replace(u'\xa0', u' ')
                            match = re.match(regex, child_string)
                            # eliminate annotation and symbol
                            if not child_string == '\n' and not child_string == '(' and not child_string == ')' and \
                                    not child_string == ', ' and not child_string == ' ' and not child_string == ' (' and \
                               not match:
                                child_list.append(child_string)
    return child_list


