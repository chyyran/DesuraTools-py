#coding=utf-8
__author__ = 'ron975'
import re
import urllib2

from desuragame import DesuraGame


class GamesList:
    def __init__(self, desuraname):
        """
        Represents a list of games owned by a member on Desura.com
        :param desuraname: Member name
        """
        self.desuraname = desuraname
        self.pages = self._get_pages()

    def _get_pages(self):
        """
        Get the list of pages of games for a certain member
        :return: List of pages
        """
        pages = [1]
        games = urllib2.urlopen("http://www.desura.com/members/{0}/games".format(self.desuraname)).read()
        for match in re.finditer(r'<a\b href="/members/.*/games/page/[^>]*>(\d)</a>', games):
            pages.append(int(match.group(1)))
        return pages

    def get_games(self):
        """
        Parse the pages of games into DesuraGame objects
        :return: DesuraGame[]
        """
        games = []
        for page in self.pages:
            #Get the page of games
            gamespage = urllib2.urlopen("http://www.desura.com/members/{0}/games/page/{1}".
                                        format(self.desuraname, page)).read()
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
                games.append(DesuraGame(matches["shortname"][match], matches["name"][match], matches["icon"][match][0]))
        return games

if __name__ == "__main__":
    games = GamesList("ron975")
    print games.get_games()[1].install()