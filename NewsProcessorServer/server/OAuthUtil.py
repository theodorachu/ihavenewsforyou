from rauth import OAuth2Service
from flask import current_app, url_for, request, redirect, session

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def authorize_callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

    def getFriends(self):
        pass

    def getProfilePic(self):
        pass

class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',           
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )
        self.oauth_session = None

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email, user_friends',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def authorize_callback(self):
        if 'code' not in request.args:
            return None, None, None
        self.oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )

        me = self.oauth_session.get('me').json()
        return (
            me['id'],
            me['name']
        )

    def getFriends(self):
        if self.oauth_session:
            r = self.oauth_session.get('me/friends', params={'metadata': 1})
            return r.json()
        return []

    def getProfilePic(self, user_id, height=250, width=250):
        if self.oauth_session:
            r = self.oauth_session.get(user_id + '/picture', params={'height': 250, 'width': 250, 'redirect': False})
            return r.json()
        return None


# class Tester(object):

#     provider = None

#     def __init__(self):
#         pass

#     @classmethod
#     def getProvider(self):
#         if self.provider is None:
#             self.provider = littleTester()
#         return self.provider

#     def setService(self):
#         pass

# class littleTester(Tester):

#     def __init__(self):
#         self.service = None

#     def setService(self):
#         self.service = "service"
#         return self.service










# oauth_session = None

# class FBObject(object):

#     def __init__(self):
#         credentials = current_app.config['OAUTH_CREDENTIALS']['facebook']
#         self.consumer_id = credentials['id']
#         self.consumer_secret = credentials['secret']

#         self.service = OAuth2Service(
#             name='facebook',
#             client_id=self.consumer_id,
#             client_secret=self.consumer_secret,
#             authorize_url='https://graph.facebook.com/oauth/authorize',           
#             access_token_url='https://graph.facebook.com/oauth/access_token',
#             base_url='https://graph.facebook.com/'
#         )

#     def get_callback_url(self):
#         return url_for('oauth_callback', provider='facebook',
#                         _external=True)

#     def authorize(self):
#         return redirect(self.service.get_authorize_url(
#             scope='email, user_friends',
#             response_type='code',
#             redirect_uri= self.get_callback_url()))

#     def authorize_callback(self):
#         if 'code' not in request.args:
#             return None, None, None
#         oauth_session = self.service.get_auth_session(
#             data={'code': request.args['code'],
#                   'grant_type': 'authorization_code',
#                   'redirect_uri': self.get_callback_url()}
#         )

#         me = oauth_session.get('me').json()
#         return (
#             'facebook$' + me['id'],
#             me['name']
#         )

#     def getFriends(self):
#         oauth_session = self.service.get_auth_session(
#             data={'code': request.args['code'],
#                   'grant_type': 'authorization_code',
#                   'redirect_uri': self.get_callback_url()}
#         )
#         r = oauth_session.get('me/friends', params={'metadata': 1})
#         return r.json()

    # def getProfilePic(self):
        # r = oauth_session.get('me/picture', params={'height': 250, 'width': 250})
        # return r.content
        # with open('temp.png', 'w') as f:
            # f.write(r.content)





