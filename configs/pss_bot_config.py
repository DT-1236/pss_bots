token = 'Mjc0NDU1NTg5NTY2ODA4MDc2.C2yWMw.uFEcuSxiZRJPp-UkloTvWV0z84Q'

base_stats = [
    'CharacterDesignId',
    'CharacterDesignName',
    'CharacterDesignDescription',
    '',
    'RaceType',
    'GenderType',
    'Rarity',
    '',
    'MaxCharacterLevel',
    'RunSpeed',
    'WalkingSpeed',
    'TrainingCapacity',
    'FireResistance',
    'FinalAttack',
    'FinalEngine',
    'FinalHp',
    'FinalPilot',
    'FinalRepair',
    'FinalResearch',
    'FinalScience',
    'FinalWeapon',
    'SpecialAbilityFinalArgument',
    'SpecialAbilityType',
    'EquipmentMask',
]

augmentable_stats = [
    'FinalAttack',
    'FinalEngine',
    'FinalHp',
    'FinalPilot',
    'FinalRepair',
    'FinalResearch',
    'FinalScience',
    'FinalWeapon',
    'SpecialAbilityFinalArgument',
    # SpecialAbilityType is added manually later
]

compared_stats = [
    'FinalAttack',
    'FinalEngine',
    'FinalHp',
    'FinalPilot',
    'FinalRepair',
    'FinalResearch',
    'FinalScience',
    'FinalWeapon',
    # SpecialAbilityFinalArgument information is added later since it would be comparing apples to oranges
]

equipment_mask = {
    0: 'None',
    3: 'Head and Body',
    5: 'Head and Leg',
    6: 'Body and Leg',
    8: 'Weapon',
    9: 'Head and Weapon',
    10: 'Body and Weapon',
    11: 'Body and Weapon and Head',
    12: 'Weapon and Leg',
    14: 'Body and Weapon and Leg',
    20: 'Accessory and Leg',
    24: 'Accessory and Weapon'
}

known_character_design_fields = {
    'ActionSoundFileId',
    'Attack',
    'CharacterBodyPartId',
    'CharacterDesignDescription',
    'CharacterDesignId',
    'CharacterDesignName',
    'CharacterHeadPartId',
    'CharacterLegPartId',
    'CollectionDesignId',
    'Engine',
    'EquipmentMask',
    'FinalAttack',
    'FinalEngine',
    'FinalHp',
    'FinalPilot',
    'FinalRepair',
    'FinalResearch',
    'FinalScience',
    'FinalWeapon',
    'FireResistance',
    'Flags',
    'GasCost',
    'GenderType',
    'Hp',
    'Level',
    'MaxCharacterLevel',
    'MinShipLevel',
    'MineralCost',
    'Pilot',
    'ProfileSpriteId',
    'ProgressionType',
    'RaceType',
    'Rarity',
    'Repair',
    'Research',
    'RootCharacterDesignId',
    'RunSpeed',
    'Science',
    'SpecialAbilityArgument',
    'SpecialAbilityFinalArgument',
    'SpecialAbilityType',
    'SpeechPhrases',
    'SpeechPitch',
    'SpeechRate',
    'SpeechVoice',
    'TapSoundFileId',
    'TrainingCapacity',
    'WalkingSpeed',
    'Weapon',
    'XpRequirementScale',
}

ignored_fields = {
    'SpeechVoice',
    'SpeechRate',
    'SpeechPitch',
    'SpeechPhrases',
    'TapSoundFileId',
    'ActionSoundFileId',  # SFX

    'ProfileSpriteId',
    'CharacterHeadPartId',
    'CharacterLegPartId',
    'CharacterBodyPartId',  # Visual data

    'Attack',
    'Research',
    'Engine',
    'Pilot',
    'Level',
    'GasCost',
    'Repair',
    'Weapon',
    'Hp',
    'Science',
    'SpecialAbilityArgument',  # Non-Maximum stats

    'CollectionDesignId',
    'RootCharacterDesignId',  # Redundant

    'MineralCost',
    'XpRequirementScale',
    'ProgressionType',
    'MinShipLevel',
    'Flags',  # Uninteresting
}
