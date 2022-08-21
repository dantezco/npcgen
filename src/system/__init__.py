"""Changes the dataset being treated based on system type"""

from src.system.fnv_tt.charsheet import (
    FNVTT_NUMERIC_ATTRIBUTES,
    IDENTIFIER_FNVTT,
    NewVegasNPC,
)

SYSTEMS_ATTRIBUTES = {IDENTIFIER_FNVTT: FNVTT_NUMERIC_ATTRIBUTES}

NPC_TEMPLATE = {
    IDENTIFIER_FNVTT: NewVegasNPC,
}
