from src import log
from src.system.constants import IDENTIFIER_FNVTT
from src.system.fnv_tt.fields import FNVTT_ATTRIBUTES

LOGGER = log.get_logger(__name__)

system_fields = {IDENTIFIER_FNVTT: FNVTT_ATTRIBUTES}
fields_bounds = {IDENTIFIER_FNVTT: FNVTT_ATTRIBUTES}


class Charsheet:
    def __init__(self, system_name: str) -> None:
        self.system_name = system_name
        for attributes in system_fields[system_name]:
            for attribute in attributes:
                self.__dict__[attribute] = None

    def _get_var_bounds(self, field: str) -> tuple:
        bounds = fields_bounds[self.system_name]
        for section in bounds:
            if field in section:
                return bounds[section]
        raise ValueError(f"Field {field} is not on this character sheet")

    def __setattr__(self, key, value):
        if isinstance(value, (int, float)):
            lower_bound, upper_bound = self._get_var_bounds(key)
            within_bounds = lower_bound <= value <= upper_bound
            if not within_bounds:
                raise ValueError(
                    f"Value {value!r} is out of bounds for this field, must to be within [{lower_bound!r},{upper_bound!r}]"
                )
        self.__dict__[key] = value
