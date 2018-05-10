from __future__ import absolute_import

from sentry import http
from sentry.identity.oauth2 import OAuth2Provider


def get_user_info(url, access_token):
    session = http.build_session()
    resp = session.get(
        'https://{}/user'.format(url),
        params={'access_token': access_token},
        headers={'Accept': 'application/vnd.github.machine-man-preview+json'},
        verify=False
    )
    resp.raise_for_status()
    resp = resp.json()

    return resp


class GitHubEnterpriseIdentityProvider(OAuth2Provider):
    key = 'github-enterprise'
    name = 'GitHub Enterprise'

    oauth_scopes = ()

    def build_identity(self, data):
        data = data['data']

        user = get_user_info(data['access_token'])

        return {
            'type': 'github-enterprise',
            'id': user['id'],
            'email': user['email'],
            'scopes': [],  # GitHub apps do not have user scopes
            'data': self.get_oauth_data(data),
        }