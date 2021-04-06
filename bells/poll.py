import requests


class Poll:
    def __init__(self):
        self.token = '5f1c2baf5f1c2baf5f1c2baf995f6b69b455f1c5f1c2baf3f708d23efda03adc95d1b31'
        self.__version = '5.92'
        self.__domain = 'bells996'

    def get_method_response(self, method):
        response = requests.get(f'https://api.vk.com/method/{method}',
                                params={
                                    'access_token': self.token,
                                    'v': self.__version,
                                    'domain': self.__domain
                                })
        return response.json()

    def get_poll_results(self, post_id=None):
        response = self.get_method_response('wall.get')['response']
        poll_results = response['items'][0]
        if post_id is not None:
            for item in response['items']:
                if item['id'] == post_id:
                    poll_results = item
                    break
        else:
            for item in response['items']:
                if 'attachments' in item:
                    if item['attachments'][0]['type'] == 'poll':
                        poll_results = item
                        break

        votes_amount = poll_results['attachments'][0]['poll']['votes']
        answers = sorted(poll_results['attachments'][0]['poll']['answers'], key=lambda answer: answer['rate'])
        print(f"Победила песня {answers[-1]['text']}")
        return answers[-1]['text']
