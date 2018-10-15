from lxml import etree

from savy_resources.users import Users


class Ships(Users):

    def __init__(self):
        super().__init__()

    def get_ship_xml_from_user_id(self, user_id, retry=True) -> list:
        response = self.get_ship_data_by_user_id(user_id)
        xml = etree.fromstring(response).xpath("//Ship")
        if not xml and retry:
            self.token_refresh()
            return self.get_ship_xml_from_user_id(user_id, retry=False)
        elif xml:
            return xml
        else:
            print("Token Error")
            return []
