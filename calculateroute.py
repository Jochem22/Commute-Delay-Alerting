import requests


class CalculateRoute:
    """
    Class to fetch route information from Waze API used to calculate delay or reroute for commute

    Attributes
    ----------
    start : str
        Cooridnates to calculate route from
    end : str
        Cooridnates to calculate route to
    """
    def __init__(self, start, end):
        self.start_coords = start
        self.end_coords = end

    @staticmethod
    def distance(results: list) -> int:
        """Calculate distance that is the sum of length from every segment of route"""
        distance = 0
        for result in results:
            distance += result['length']
        distance = int(distance / 1000.0)
        return distance

    def get_route(self) -> dict:
        """Get route information from Waze API"""
        url = "https://www.waze.com/row-RoutingManager/routingRequest"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "https://www.waze.com/",
        }
        params = {
            "from": self.start_coords,
            "to": self.end_coords,
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "false",
            "returnInstructions": "false",
            "timeout": 60000,
            "nPaths": 0,
            "subscription": "*",
            "options": 'AVOID_TRAILS:t,AVOID_TOLL_ROADS:t,AVOID_FERRIES:t',
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            if "error" not in response.text:
                response_json = response.json()
                response_dict = response_json['response']
                return response_dict
            else:
                raise Exception(response.text)
        else:
            raise Exception(response.status_code)

    def calc_route(self) -> [int, int, str]:
        """Returns route information"""
        route = self.get_route()
        route_description = route['routeName']
        duration_realtime = route['totalRouteTime']
        duration_realtime = int(duration_realtime / 60)
        results = route['results']
        distance_realtime = self.distance(results)
        return duration_realtime, distance_realtime, route_description
