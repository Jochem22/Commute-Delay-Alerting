#! /usr/bin/env python3
from utils import Logger
from calculateroute import CalculateRoute
from alerting import Alerting
import datetime
import time
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)
LOGGER = Logger()


def main():
    """
    Check commute for delays or reroute
    """
    reroute_notified = False
    delay_notified = False
    clear_notified = False
    while True:
        for routes in CONFIG["routes"]:
            route = CONFIG["routes"][routes]
            date = datetime.datetime.now().strftime('%d-%m-%Y')
            send_updates = CONFIG["settings"]["send_updates"]
            departure_time = route['departure']
            departure_time = f"{date} {departure_time}"
            departure_time = datetime.datetime.strptime(departure_time, '%d-%m-%Y %H:%M') + datetime.timedelta(hours=2)
            weekday = datetime.datetime.today().weekday()
            if weekday in route["days"]:
                if datetime.datetime.now() < departure_time:
                    if departure_time - datetime.datetime.now() < datetime.timedelta(hours=4):
                        origin = route["origin"]
                        destination = route["destination"]
                        lat = CONFIG["places"][origin]['lat']
                        lon = CONFIG["places"][origin]['lon']
                        start = f"x:{lon} y:{lat}"
                        lat = CONFIG["places"][destination]['lat']
                        lon = CONFIG["places"][destination]['lon']
                        end = f"x:{lon} y:{lat}"
                        distance_static = route['distance']
                        duration_static = route['duration']
                        LOGGER.info(f"Started monitoring route {origin} ({start}) to {destination} ({end})")
                        route = CalculateRoute(start, end)
                        try:
                            duration_realtime, distance_realtime, route_description = route.calc_route()
                        except Exception as e:
                            LOGGER.error(e)
                            raise
                        duration_delay = duration_realtime - duration_static
                        max_delay = CONFIG["settings"]["max_delay"]
                        alerting = Alerting(max_delay, origin, destination, duration_realtime, duration_delay,
                                            distance_static, distance_realtime, route_description)
                        LOGGER.info(vars(alerting))
                        delay = Alerting.check_delay(alerting)
                        reroute = Alerting.check_reroute(alerting)
                        LOGGER.debug(f"delay: {delay}")
                        LOGGER.debug(f"reroute: {reroute}")
                        msg = None
                        if reroute is True and reroute_notified is False:
                            reroute_notified = True
                            clear_notified = True
                            msg = Alerting.set_reroute(alerting)
                        elif delay is True and delay_notified is False and reroute is False:
                            delay_notified = True
                            clear_notified = True
                            msg = Alerting.set_delay(alerting)
                        elif clear_notified is True and delay is False and reroute is False:
                            delay_notified = False
                            reroute_notified = False
                            clear_notified = False
                            msg = Alerting.set_clearing(alerting)
                        elif reroute_notified is True or delay_notified is True and send_updates is True:
                            if reroute:
                                msg = Alerting.set_update(alerting, "reroute")
                            elif delay:
                                msg = Alerting.set_update(alerting, "delay")
                        if msg:
                            try:
                                Alerting.send_alert(msg)
                            except Exception as e:
                                LOGGER.error(e)
                    else:
                        LOGGER.info(f"Nothing to monitor. "
                                    f"Start monitoring at {departure_time - datetime.timedelta(hours=4)}")
        time.sleep(300)


if __name__ == "__main__":
    main()
