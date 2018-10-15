from lxml import etree
from collections import namedtuple

from savy_resources.savy_connection import SavyConnection
from utilities.fuzzy_logic import Fuzzy


class Users(SavyConnection, Fuzzy):

    UserMatch = namedtuple("UserMatch", ['Name', 'Id', 'Confidence'])

    def __init__(self):
        super().__init__()

    def get_user_search_xml(self, name):
        return etree.fromstring(super().search_players_by_name(name))

    def parse_user_name(self, name):
        """Returns a tuple of two items:
        1.) UserMatch object with highest match confidence and shortest matching string
        2.) List of UserMatch objects with an equal match confidence but longer matching strings or later by abc
        UserMatch objects have User @Name as Name, User @Id as Id, and the fuzzy Confidence rating"""

        xml = self.get_user_search_xml(name)

        try:
            primary, secondary = self.match_best_then_shortest(name, xml.xpath("//@Name"), user_data=True)
        except RuntimeError:
            # Usually this indicates no matches
            assert not xml.xpath("//@Name")
            return (), []

        result = Users.UserMatch(Name=primary[0],
                                 Id=xml.xpath("//User[@Name='{}']/@Id".format(primary[0])),
                                 Confidence=primary[1])
        possible = [Users.UserMatch(Name=match_tuple[0],
                                    Id=xml.xpath("//User[@Name='{}']/@Id".format(match_tuple[0])),
                                    Confidence=match_tuple[1])
                    for match_tuple in secondary if match_tuple[1] == result.Confidence]

        return result, possible
