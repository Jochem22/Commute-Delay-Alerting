from dotenv import dotenv_values
from utils import Logger
import requests

LOGGER = Logger()
SECRET = dotenv_values()


class Alerting:
    """
    Class for setting and sending alerts regarding delay or reroute of commute

    Attributes
    ----------
    max_delay : int
        max delay in minutes set in config
    origin : str
        origin name set in config
    destination : str
        destination name set in config
    duration_realtime : int
        duration of route in real time including traffic jams
    duration_delay : int
        total delay of route in minutes in real time used to check for delay
    distance_static : int
        distance of route in km's set in config
    distance_realtime : int
        distance of route in km's in real time used to check for reroute
    route_description : int
        short description of route
    """

    def __init__(self, max_delay, origin, destination, duration_realtime, duration_delay, distance_static, distance_realtime, route_description):
        self.max_delay = max_delay
        self.origin = origin
        self.destination = destination
        self.duration_realtime = duration_realtime
        self.duration_delay = duration_delay
        self.distance_static = distance_static
        self.distance_realtime = distance_realtime
        self.route_description = route_description

    def check_delay(self) -> bool:
        """Returns True if total delay in minutes exceeds max delay in minutes set in config"""
        if self.duration_delay >= self.max_delay:
            return True
        else:
            return False

    def check_reroute(self) -> bool:
        """Returns True if distance not in range of distance set in config """
        if (self.distance_static - 1) <= self.distance_realtime <= (self.distance_static + 1):
            return False
        else:
            return True

    def set_delay(self) -> str:
        """Set message when delay is True"""
        msg = (
            f"Delay on route from {self.origin} to {self.destination} ({self.route_description}). "
            f"Current duration is {self.duration_realtime} minutes with {self.duration_delay} minutes delay. "
        )
        return msg

    def set_reroute(self) -> str:
        """Set message when reroute is True"""
        msg = (
            f"Reroute on route from {self.origin} to {self.destination} ({self.route_description}). "
            f"New duration is {self.duration_realtime} minutes. "
        )
        return msg

    def set_clearing(self) -> str:
        """Set message when delay or reroute alarms are cleared"""
        msg = (
            f"Cleared alarms for {self.origin} to {self.destination} ({self.route_description}). "
            f"Duration is {self.duration_realtime} minutes. "
        )
        return msg

    @staticmethod
    def send_alert(msg: str) -> None:
        """Send message to chat_id via Telegram"""
        token = SECRET["TOKEN"]
        chat_id = SECRET["CHATID"]
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
        try:
            request = requests.get(url).json()
            LOGGER.info(request)
        except:
            raise Exception("error sending telegram message")
