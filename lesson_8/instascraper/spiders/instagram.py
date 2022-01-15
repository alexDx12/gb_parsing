import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instascraper.items import InstascraperItem
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'av_dunaev@mail.ru'
    inst_pwd = '**************'
    users_parse = ['python.learning', 'machinelearning', 'artificialintelligence_ai']
    inst_friends_link = 'https://i.instagram.com/api/v1/friendships/'
    users_type = ['followers', 'following']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for user in self.users_parse:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_parse,
                    cb_kwargs={'username': user})

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        for u_type in self.users_type:
            url_friends = f'{self.inst_friends_link}{user_id}/{u_type}/?count=12'
            yield response.follow(url_friends,
                                  callback=self.user_friends_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'u_type': u_type})

    def user_friends_parse(self, response: HtmlResponse, username, user_id, u_type):
        j_data = response.json()
        max_id = j_data.get('next_max_id')
        if max_id:
            url_friends = f'{self.inst_friends_link}{user_id}/{u_type}/?count=12&max_id={max_id}&search_surface=follow_list_page'
            yield response.follow(
                url_friends,
                callback=self.user_friends_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'u_type': u_type})

        friends = j_data.get('users')
        for friend in friends:
            item = InstascraperItem(
                u_type=u_type,
                username=username,
                friend_id=friend.get('pk'),
                friend_name=friend.get('username'),
                full_name=friend.get('full_name'))
            yield item

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
