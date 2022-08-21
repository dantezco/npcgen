"""Fields description for Fallout New Vegas Tabletop"""

import math
import random

import names
from pydtmc import MarkovChain

IDENTIFIER_FNVTT = "fnv_tt"
FNVTT_NUMERIC_ATTRIBUTES = {
    "SPECIAL": ("s", "p", "e", "c", "i", "a", "l"),
    "Skills": (
        "barter",
        "energy_weapons",
        "explosives",
        "guns",
        "lockpick",
        "medicine",
        "melee_weapons",
        "repair",
        "science",
        "sneak",
        "speech",
        "survival",
        "unarmed",
    ),
}
FNVTT_BOUNDS = {
    "SPECIAL": {
        "min": 1,
        "max": 10,
    },
    "Skills": {"min": 1, "max": 99},
}


class NewVegasNPC:
    """Character sheet for FNVTT"""

    def __init__(self, class_name: str, level: int, class_information: dict) -> None:
        """"""
        self.level = level
        self.char_class = class_name
        self.name = (
            names.get_full_name()
            if class_information.get("has_name", None)
            else f"{class_name}{random.randint(1, 100)}"
        )
        self._set_base_stats(char_class=class_information)
        self.actions_per_turn = math.ceil(self.SPECIAL["a"] / 2)
        self.sequence = random.randint(1, 10) + self.SPECIAL["a"]
        self.hp = 100 + (self.SPECIAL["e"] * 20) + ((self.level - 1) * 5)
        self.carry_weigth = 150 + self.SPECIAL["s"] * 10

    def serialize(self):
        return self.__dict__

    def _determine_section_points(self, section: str, points: int, p: list) -> dict:
        labels = FNVTT_NUMERIC_ATTRIBUTES[section]
        markov = MarkovChain(p=p, states=labels)
        stats = {k: FNVTT_BOUNDS[section]["min"] for k in labels}
        state = markov.walk(1)
        while points:
            if stats[state[0]] < FNVTT_BOUNDS[section]["max"]:
                stats[state[0]] += 1
                points -= 1
            state = markov.walk(steps=1, initial_state=state[1])
        return stats

    def _set_base_stats(self, char_class: dict) -> None:
        section = "SPECIAL"
        points = 25
        p = char_class["probabilities"][section]
        d = self._determine_section_points(section=section, points=points, p=p)
        setattr(self, section, d)
        # TODO add tagged skills
        section = "Skills"
        points = (math.ceil(d["i"] / 2.0) + 10) * self.level
        p = char_class["probabilities"][section]
        d = self._determine_section_points(section=section, points=points, p=p)
        setattr(self, section, d)
