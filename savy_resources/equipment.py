import time

from lxml import etree

from savy_resources.savy_connection import SavyConnection


def best_in_slot_dict(equipment_xpath) -> dict:
    """Dict[slot][stat]['Entries'][list(BIS items)]
    Dict[slot][stat]['Value'][float(BIS value)]"""
    results = {}
    for item in equipment_xpath:
        value = float(item.get('EnhancementValue'))
        slot = item.get('ItemSubType')
        stat = item.get('EnhancementType')
        name = item.get('ItemDesignName')
        previous_max = results.get(slot, {}).get(stat, {}).get('Value', 0)
        if value > previous_max:
            results.setdefault(slot, {})[stat] = {'Value': value, 'Entries': [name]}
        elif value == previous_max and previous_max > 0:
            results[slot][stat]['Entries'].append(name)
    return results


class Equipment(SavyConnection):

    def __init__(self):
        start = time.clock()
        super().__init__()
        self.equipment_xml = etree.fromstring(super().get_item_data())
        self.best_in_slot = best_in_slot_dict(self.equipment_xml.xpath(
            "//ItemDesign[@ItemType='Equipment'][@EnhancementType!='None'][@ItemSubType!='Module']"))
        self.equipment_stat_types = set(self.equipment_xml.xpath(
            "//ItemDesign[@EnhancementType!='None']/@EnhancementType"))
        self.equipment_slot_types = set(self.equipment_xml.xpath(
            "//ItemDesign[contains(@ItemSubType, 'Equipment')]/@ItemSubType"))
        self.equipment_names = set(self.equipment_xml.xpath("//ItemDesign/@ItemDesignName"))
        print('Equipment prepped in {0:.3f}s'.format(time.clock() - start))

    def search_items(self, name='', design_id='', stat='', slot=''):
        return self.equipment_xml.xpath("//ItemDesign"
                                        "[contains(@ItemDesignName, '{name}')]"
                                        "[contains(@ItemDesignId, '{design_id}')]"
                                        "[contains(@EnhancementType, '{stat}')]"
                                        "[contains(@ItemSubType, '{slot}')]"
                                        "".format(name=name,
                                                  design_id=design_id,
                                                  stat=stat,
                                                  slot=slot)
                                        )
