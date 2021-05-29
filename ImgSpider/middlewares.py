import random

class RandomUserAgentMiddleware(object):

    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # 在settings.py文件中加载MY_USER_AGENTS的值
        s = cls(user_agents=crawler.settings.get('MY_USER_AGENTS'))
        return s

    def process_request(self, request, spider):
        # 随机设置User-Agent的值
        agent = random.choice(self.user_agents)
        # 将其赋给Request
        request.headers['User-Agent'] = agent
        # proxy = random.choice(self.proxy)
        # request.meta['proxy'] = proxy
        return None
