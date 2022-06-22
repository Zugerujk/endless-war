""" A weather object. Pure flavor. """


class EwWeather:
    # The identifier for this weather pattern.
    name = ""

    str_sunrise = ""
    str_day = ""
    str_sunset = ""
    str_night_new = ""
    str_night_waxing_start = ""
    str_night_waxing_end = ""
    str_night_full = ""
    str_night_waning_start = ""
    str_night_waning_end = ""
    str_night_special = ""

    def __init__(
            self,
            name = "",
            sunrise = "",
            day = "",
            sunset = "",
            night_new = "",
            night_waxing_start = "",
            night_waxing_end = "",
            night_full = "",
            night_waning_start = "",
            night_waning_end = "",
            night_special = ""
    ):
        self.name = name
        self.str_sunrise = sunrise
        self.str_day = day
        self.str_sunset = sunset
        self.str_night_new_ = night_new
        self.str_night_waxing_start = night_waxing_start
        self.str_night_waxing_end = night_waxing_end
        self.str_night_full = night_full
        self.str_night_waning_start = night_waning_start
        self.str_night_waning_end = night_waning_end
        self.str_night_special = night_special

""" A POI Event object for flavor and necessary information. An EwWorldEvent object is used for the event itself."""


# World events that happen at a specific POI, with flavor text
class EwPoiPhenomenon:
    name = ""
    str_name = ""
    
    # Possible POIs that the event can take place in 
    pois = []

    # How long the POI event happens and if there should be a time between generation and activation, in in-game hours
    length = 0
    buffer = 0

    # Whether there is a forewarning in the POI and gangbases
    forewarning = False

    # Flavor text for on start in POI, when inspecting POI, and on end
    str_start = ""
    str_ongoing = ""
    str_end = ""

    # Flavor text for when checking weather/time
    str_check_text = ""

    # Extra needed flavor text
    str_extra_text = ""

    def __init__(
            self,
            name = "",
            str_name = "",
            pois = [],
            length = 0,
            buffer = 0,
            forewarning = False,
            str_start = "",
            str_ongoing = "",
            str_end = "",
            str_check_text = "",
            str_extra_text = ""
    ):
        self.name = name
        self.str_name = str_name
        self.pois = pois
        self.length = length
        self.buffer = buffer
        self.forewarning = forewarning
        self.str_start = str_start
        self.str_ongoing = str_ongoing
        self.str_end = str_end
        self.str_check_text = str_check_text
        self.str_extra_text = str_extra_text