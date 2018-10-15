import time
from collections import namedtuple

from lxml import etree

from configs import pss_bot_config
from savy_resources.equipment import Equipment
from utilities.fuzzy_logic import Fuzzy


class Crew(Equipment, Fuzzy):
    """normal flow is as follows:
    1.) Receive user_input_string
    2.) Pass into parse_crew_name, return result(string), possible(list)
    3.) If possible is populated, Bot will send message
    4.) Bot will pass result.Id into get_crew_xml_from_id, return crew_xml
    5.) crew_xml will be passed into get_crew_values_from_xml and returned to Bot
    6.) get_crew_equipment_slots will be called when the bot is preparing the output string"""

    # Remove the nullstrings added for formatting
    base_stats = [x for x in pss_bot_config.base_stats if x]
    CrewValues = namedtuple('CrewValues', base_stats)
    CrewMatch = namedtuple('CrewMatch', ['Name', 'Id', 'Confidence'])

    def __init__(self):
        super().__init__()
        start = time.clock()

        self.crew_xml = etree.fromstring(super().get_crew_data())
        self.crew_names = set(self.crew_xml.xpath("//CharacterDesign/@CharacterDesignName"))
        self.crew_rarities = set(self.crew_xml.xpath("//CharacterDesign/@Rarity"))
        self.crew_design_fields = set(self.crew_xml.xpath("//CharacterDesign[1]")[0].keys())
        self.crew_equipment_masks = set(self.crew_xml.xpath("//CharacterDesign/@EquipmentMask"))
        self.unexpected_fields = self.crew_design_fields - pss_bot_config.known_character_design_fields
        self.training = 50

        if self.unexpected_fields:
            print("The following fields were unexpected:\n\n{}\n\n"
                  "Inform the developer as soon as you are able\n\n".format(', '.join(self.unexpected_fields)))
        print("Crew prepped in {:.3f}s".format(time.clock() - start))

    def parse_crew_name(self, name) -> (str, list):
        """Returns a tuple of two items:
        1.) CrewMatch object with highest match confidence and shortest matching string
        2.) List of CrewMatch objects with an equal match confidence but longer matching strings or later by abc
        CrewMatch objects have CharacterDesignName as Name, CharacterDesignId as Id, and the fuzzy Confidence rating"""

        primary, secondary = self.match_best_then_shortest(name, self.crew_names)

        result = Crew.CrewMatch(Name=primary[0],
                                Id=self.get_crew_id_from_matched_name(primary[0]),
                                Confidence=primary[1])
        possible = [Crew.CrewMatch(Name=match_tuple[0],
                                   Id=self.get_crew_id_from_matched_name(match_tuple[0]),
                                   Confidence=match_tuple[1])
                    for match_tuple in secondary if match_tuple[1] == result.Confidence]

        return result, possible

    @staticmethod
    def handle_multiple_results(results, messages, message):
        if len(results) > 1:
            print(message)
            messages.append(message)
        return messages

    def get_crew_id_from_matched_name(self, name) -> str:
        """input name must be selected from self.crew_names
        assumes there are no duplicate name entries"""
        results = self.crew_xml.xpath("//CharacterDesign[@CharacterDesignName='{}']/@CharacterDesignId".format(name))
        return results[0]

    def get_crew_xml_from_id(self, character_id, messages):
        results = self.crew_xml.xpath("//CharacterDesign[@CharacterDesignId='{}']".format(character_id))
        messages = self.handle_multiple_results(
            results, messages, "ID: {} has multiple CharacterDesign matches".format(character_id))
        return results[0], messages

    def get_crew_xml_from_user_input(self, user_input):
        messages = []
        matched_xmls = []

        for entry in user_input:
            if entry.isdigit():
                matched_xmls, messages = self.get_crew_xml_from_id(entry, messages)

            else:
                match = self.parse_crew_name(entry)
                messages.append("```{} -> {}, {}% Match```".format(entry, match[0].Name, match[0].Confidence))

                if match[1]:
                    messages.append(
                        "Enclose names with multiple parts in \"\". e.g. \"Dr Dong\""
                        "```Other possible entries for: {}\n\n{}```".format(entry, [x.Name for x in match[1]]))

                matched_xml, messages = self.get_crew_xml_from_id(match[0].Id, messages)
                matched_xmls.append(matched_xml)
        return matched_xmls, messages

    def get_augmented_stat_value(self, xml, stat, slots):
        value = float(xml.get(stat))
        modifiers = ""
        if stat in pss_bot_config.augmentable_stats:
            value *= self.training/100 + 1
            modifiers += " + {}% Training".format(self.training)
        for slot in slots:
            enhancement = float(self.best_in_slot.get(slot, {}).get(stat.replace("Final", ""), {}).get('Value', 0))
            if enhancement:
                value += enhancement
                modifiers += " + {}".format(self.best_in_slot[slot][stat.replace("Final", "")]['Entries'])
        return value, modifiers

    @staticmethod
    def get_crew_values_from_xml(crew_xml):
        return Crew.CrewValues(**{value: crew_xml.get(value) for value in Crew.base_stats})

    @staticmethod
    def get_crew_equipment_slots(crew_xml):
        description = pss_bot_config.equipment_mask[int(crew_xml.xpath('@EquipmentMask')[0])]
        if description == 'None':
            return []
        else:
            return ["Equipment" + x for x in description.split(' and ')]

    # Test functions

    def get_crew_names_with_equipment_mask(self, mask):
        return self.crew_xml.xpath("//CharacterDesign[@EquipmentMask='{}']/@CharacterDesignName".format(mask))
