import time
from spade import quit_spade

from src.agents.customer import Customer
from src.agents.request_handler import RequestHandler
from src.agents.control_station import ControlStation

if __name__ == "__main__":
    customer = Customer("AASD_CUSTOMER@01337.io", "AASD_CUSTOMER")
    requestHandler = RequestHandler("AASD_REQUEST_HANDLER@01337.io", "AASD_REQUEST_HANDLER")
    controlStation = ControlStation("AASD_CONTROL_STATION@01337.io", "AASD_CONTROL_STATION")

    customer_future = customer.start()
    request_handler_future = requestHandler.start()
    control_station_future = controlStation.start()

    customer_future.result()  # Wait until the start method is finished
    request_handler_future.result()
    control_station_future.result()

    while customer.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            customer.stop()
            requestHandler.stop()
            controlStation.stop()
            break
    print("Agents finished")

    quit_spade()
