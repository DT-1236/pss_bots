from re import sub

from requests import get, post
from lxml import etree

try:
    from configs.council_bot_config import deviceKey, checksum
except ModuleNotFoundError:
    deviceKey, checksum = '', ''


class SavyConnection:

    def __init__(self):
        self.server_check_url = r'http://api.pixelstarships.com/settingservice/getproductionserver'
        server_check = get(self.server_check_url)
        if "2" in server_check:
            self.server = '2'
        else:
            self.server = ''

        self.crew_data_url = r"https://api{}.pixelstarships.com/CharacterService" \
                             r"/ListAllCharacterDesigns2?languageKey=en".format(self.server)
        self.item_data_url = r"http://api{}.pixelstarships.com/ItemService/ListItemDesigns2?languageKey=en".format(
            self.server)

        #  urls with inputs must be modified later with the input strings
        self.token_url = r"http://api{}.pixelstarships.com/UserService/DeviceLogin5?deviceKey={}&advertisingKey=" \
                         r"&isJailBroken=false&checksum={}&deviceType=DeviceTypeIPhone"
        self.player_data_url = r"http://api{}.pixelstarships.com/UserService/SearchUsers?searchString={}"
        self.ship_data_url = r"http://api{}.pixelstarships.com//ShipService/InspectShip?userId={}&accessToken={}"
        self.crew_action_url = r"https://api{}.pixelstarships.com/CharacterService/ListCharacterActionsByShipId?" \
                               r"shipId={}&accessToken={}"
        self.room_action_url = r"https://api{}.pixelstarships.com/RoomService/ListAllRoomActionsOfShip?" \
                               r"shipId={}&accessToken={}"
        self.battle_replay_url = r"https://api{}.pixelstarships.com/BattleService/GetBattle2?" \
                                 r"battleId={}&accessToken={}"
        self.token = ''

    def get_crew_data(self):
        """Returns decoded response for the crew_data_url"""
        return get(self.crew_data_url).content.decode('utf-8')

    def get_item_data(self):
        """Returns decoded response for the item_data_url"""
        return get(self.item_data_url).content.decode('utf-8')

    def search_players_by_name(self, name):
        """Returns decoded response for up to 10 results for a search by player_name"""
        return get(self.player_data_url.format(self.server, sub(' ', '%20', name))).content.decode('utf-8')

    def get_ship_data_by_user_id(self, user_id):
        """Returns decoded response for ship data from user_id"""
        return get(self.ship_data_url.format(self.server, user_id, self.token)).content.decode('utf-8')

    def token_refresh(self):
        if deviceKey and checksum:
            response = post(self.token_url.format(self.server, deviceKey, checksum))
            self.token = etree.fromstring(response.content.decode('utf-8')).xpath("//@accessToken")[0]
