import re

from savy_resources.crew import Crew
from configs import pss_bot_config


class PSSBot(Crew):

    def __init__(self):
        super().__init__()

    @staticmethod
    def prepare_user_input(raw_input) -> list:
        """Turns raw user input into discrete arguments. Items enclosed in double quotes are considered single items"""
        stripped_input = re.sub('\s+', ' ', raw_input).strip()
        inputs = [x for x in stripped_input.split('"') if x.strip()]
        if len(inputs) == 1 and '"' not in raw_input:
            inputs = inputs[0].split(' ')
        if len(inputs) not in (1, 2):
            return []
        else:
            return inputs

    @staticmethod
    def base_stat_output(xml):
        stat_lookup_results = ["{}: {}".format(value.replace("Final", ''), xml.get(value)) if value else ''
                               for value in pss_bot_config.base_stats]
        mask = int(xml.get('EquipmentMask'))
        stat_lookup_results.append("EquipmentSlots: {}".format(pss_bot_config.equipment_mask[mask]))
        return "```" + '\r\n'.join(stat_lookup_results) + "```"

    @staticmethod
    def base_stat_comparison(xml1, xml2):
        message = "Stat comparison for:\n{} vs. {}".format(
            xml1.get('CharacterDesignName'), xml2.get('CharacterDesignName'))

        stat_lookup_results = ["{}: {:.2f}".format(value.replace("Final", ''),
                                                   float(xml1.get(value)) - float(xml2.get(value)))
                               for value in pss_bot_config.compared_stats]
        stat_lookup_results.append("{}({}) vs. {}({})".format(
            xml1.get('SpecialAbilityType'), xml1.get('SpecialAbilityFinalArgument'),
            xml2.get('SpecialAbilityType'), xml2.get('SpecialAbilityFinalArgument')))

        return message + "```" + '\r\n'.join(stat_lookup_results) + "```"

    def max_stat_output(self, xml):
        message = "With {}% Training and best in slot gear:".format(self.training)
        stat_lookup_results = ""
        slots = self.get_crew_equipment_slots(xml)

        for stat in sorted(list(pss_bot_config.augmentable_stats)):
            value, modifiers = self.get_augmented_stat_value(xml, stat, slots)
            stat_lookup_results += "{}: {:.2f}, {}\n".format(stat.replace("Final", ""), value, modifiers)
        stat_lookup_results += "{}: {}".format('SpecialAbilityType', xml.get('SpecialAbilityType'))
        return message + "```" + stat_lookup_results + "```"

    def max_stat_comparison(self, xml1, xml2):
        message = "With {}% Training and best in slot gear:".format(self.training)
        stat_lookup_results = ""
        slots1, slots2 = self.get_crew_equipment_slots(xml1), self.get_crew_equipment_slots(xml2)

        for stat in pss_bot_config.compared_stats:
            value = float(self.get_augmented_stat_value(xml1, stat, slots1)[0]) \
                    - float(self.get_augmented_stat_value(xml2, stat, slots2)[0])
            stat_lookup_results += "{}: {:.2f}\n".format(stat.replace("Final", ""), value)
        return message + "```" + stat_lookup_results + "```"

# self = PSSBot()
# xmls = self.get_crew_xml_from_user_input(['Dark', 'Wolf'])[0]
# xml1, xml2 = xmls[0], xmls[1]
