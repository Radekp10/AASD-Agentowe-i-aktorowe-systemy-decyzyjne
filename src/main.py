import time
from spade import quit_spade

from src.agents.customer import Customer
from src.agents.request_handler import RequestHandler
from src.agents.control_station import ControlStation
from src.agents.drone import Drone

if __name__ == "__main__":
    customer = Customer("AASD_CUSTOMER@01337.io", "AASD_CUSTOMER")
    requestHandler = RequestHandler("AASD_REQUEST_HANDLER@01337.io", "AASD_REQUEST_HANDLER")
    controlStation = ControlStation("AASD_CONTROL_STATION@01337.io", "AASD_CONTROL_STATION")
    drone = Drone("AASD_DRONE@01337.io", "AASD_DRONE")

    customer_future = customer.start()
    request_handler_future = requestHandler.start()
    control_station_future = controlStation.start()
    drone_future = drone.start()

    customer_future.result()  # Wait until the start method is finished
    request_handler_future.result()
    control_station_future.result()
    drone_future.result()

    while customer.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            customer.stop()
            requestHandler.stop()
            controlStation.stop()
            drone.stop()
            break
    print("Agents finished")

    quit_spade()
