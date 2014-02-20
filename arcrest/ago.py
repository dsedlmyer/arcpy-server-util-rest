"""Represents the ArcGIS online REST APIs"""

from arcrest import server
import urlparse


__all__ = ['AGORoot', 'Community', 'Content', 'Portals']

class AGORoot(server.RestURL):
    def __init__(self, url, username=None, password=None,
                 token=None, generate_token=True,
                 expiration=60):
        """If a username/password is provided, AUTH and AUTH_DIGEST
           authentication will be handled automatically. If using
           token based authentication, either 1. Pass a token in the token
           argument or 2. Set generate_token and a token will be generated."""
        if username is not None and password is not None:
            self._pwdmgr.add_password(None,
                                      url,
                                      username,
                                      password)
        url_ = list(urlparse.urlsplit(url))
        if not url_[2].endswith('/'):
            url_[2] += "/"
        if token is not None:
            self.__token__ = token
        elif generate_token:
            new_url = urlparse.urlunsplit(url_)
            gentoken = server.GenerateToken(url, username, password, expiration)
            self._referer = gentoken._referer
            self.__token__ = gentoken.token
        super(AGORoot, self).__init__(url)
    def search(self, q=None, bbox=None, start=None, num=None,
               sortField=None, sortOrder=None):
        return self._get_subfolder("./search", 
                                          server.JsonPostResult,
                                          {'q': q,
                                           'bbox': bbox,
                                           'start': start,
                                           'num': num,
                                           'sortField': sortField,
                                           'sortOrder': sortOrder})
    @property
    def currentVersion(self):
        return self._json_struct["currentVersion"]
    
    @property
    def community(self):
        return self._get_subfolder("./community/", Community)
    @property
    def content(self):
        return self._get_subfolder("./content/", Content)
    @property
    def portals(self):
        return self._get_subfolder("./portals/", Portals)

class Community(server.RestURL):
    __cache_request__ = False

    def __init__(self, url, file_data=None):
        if not isinstance(url, (tuple, list)):
            url_ = list(urlparse.urlsplit(url))
        else:
            url_ = url
        if not url_[2].endswith('/'):
            url_[2] += "/"
        super(Community, self).__init__(url_, file_data)
    
    @property
    def Self(self):
        return self._get_subfolder("./self", CommunitySelf)

class CommunitySelf(server.RestURL):
    __cache_request__ = True
    
    def __init__(self, url, file_data=None):
        if not isinstance(url, (tuple, list)):
            url_ = list(urlparse.urlsplit(url))
        else:
            url_ = url
        if not url_[2].endswith('/'):
            url_[2] += "/"
        super(CommunitySelf, self).__init__(url_, file_data)
    
    def __getattr__(self, attr):
        return self._json_struct[attr]
    
    def __getitem__(self, attr):
        return self._json_struct[attr]
        

class Content(server.RestURL):
    pass

class Portals(server.RestURL):
    pass
