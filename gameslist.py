#coding=utf-8
__author__ = 'ron975'
import re
import urllib2
import htmlentitydefs

from desuragame import DesuraGame


class GamesList:
    def __init__(self, profileid):
        """
        Represents a list of games owned by a member on Desura.com
        :param profileid: Profile ID
        """
        self.profileid = profileid
        self._test_account()
        self.pages = self._get_pages()

    def _test_account(self):
        try:
            desura = urllib2.urlopen("http://www.desura.com/members/{0}/".format(self.profileid)).read()
            if re.search(r'The member you are trying to view has set their account to private', desura) is not None:
                raise PrivateProfileError("Private Desura Profiles are not supported", self.profileid)
        except urllib2.HTTPError:
            raise NoSuchProfileError("No such profile exists")

    def _get_pages(self):
        """
        Get the list of pages of games for a certain member
        :return: List of pages
        """
        try:
            pages = [1]
            games = urllib2.urlopen("http://www.desura.com/members/{0}/games".format(self.profileid)).read()
            for match in re.finditer(r'<a\b href="/members/.*/games/page/[^>]*>(\d)</a>', games):
                pages.append(int(match.group(1)))
            return pages
        except AttributeError:
            raise InvalidDesuraProfileError("No games associated with account")

    def get_games(self):
        """
        Parse the pages of games into DesuraGame objects
        :return: DesuraGame[]
        """
        try:
            games = []
            for page in self.pages:
                #Get the page of games
                gamespage = urllib2.urlopen("http://www.desura.com/members/{0}/games/page/{1}".
                                            format(self.profileid, page)).read()
                #We want only our games, remove the "Popular Games" that mess with our search
                gamespage = gamespage.replace(re.search(
                    r'(?=<span class="heading">Popular Games</span>).*', gamespage, re.DOTALL).group(), "")

                #Create a dict of matches. The indexes are identical across games
                matches = {
                    'shortname': re.findall(r'(?<=a href="/games/)([\w\d-]+)(?="\sclass="image")', gamespage),
                    'name': re.findall(r'(?<=alt=").+(?="\sclass="icon")', gamespage),
                    'icon': re.findall(r'(http://media.desura.com/images/games/\d+/\d+/\d+/.+'
                                       r'(png|PNG|jpg|JPG|bmp|BMP|jpeg|JPEG|gif|GIF))', gamespage)
                }
                #Iterate over all the games and group together information for a game
                for match in range(len(matches["shortname"])):
                    games.append(DesuraGame(matches["shortname"][match], unescape(matches["name"][match]),
                                            matches["icon"][match][0]))
            return games
        except AttributeError:
            raise InvalidDesuraProfileError("No games associated with account")


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def username_from_profile_id(profileid):
    try:
        desura = urllib2.urlopen("http://www.desura.com/members/{0}/".format(profileid)).read()
    except urllib2.HTTPError:
        raise NoSuchProfileError("Profile {0} not found".format(profileid))
    username = re.search(r'(?<=<h1>)(.*)(?=</h1>)', desura).group(0)
    return username


class InvalidDesuraProfileError(Exception):
    pass


class PrivateProfileError(InvalidDesuraProfileError):
    pass


class NoSuchProfileError(InvalidDesuraProfileError):
    pass
