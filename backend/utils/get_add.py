from pprint import pprint
from typing import Tuple, Any

from geopy.geocoders import Nominatim


def get_addr(addr: str) -> Tuple | None:
    geolocator = Nominatim(user_agent="Tester")
    try:
        location = geolocator.geocode(addr, addressdetails=True)
        data: dict = location.raw.get("address")
        return (
            data.get("region"),
            data.get("state"),
            data.get("county"),
            data.get("city"),
            data.get("city_district"),
            data.get("road"),
            data.get("house_number"),
        )
    except:
        return None


if __name__ == "__main__":
    address = str(input('Введите адрес: \n'))
    pprint(get_addr(addr=address))
