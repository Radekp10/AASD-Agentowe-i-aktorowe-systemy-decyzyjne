import time
from spade import quit_spade

from src.agents.customer import Customer
from src.agents.request_handler import RequestHandler
from src.agents.control_station import ControlStation
from src.agents.control_station_status_send import ControlStationStatusSender
from src.agents.control_station_monitor import ControlStationMonitor
from src.agents.drones_status_send import DronesStatusSender
from src.agents.drones_monitor import DronesMonitor
from src.agents.drone import Drone

if __name__ == "__main__":
    customer = Customer("AASD_CUSTOMER@01337.io", "AASD_CUSTOMER")
    requestHandler = RequestHandler("AASD_REQUEST_HANDLER@01337.io", "AASD_REQUEST_HANDLER")
    controlStation = ControlStation("AASD_CONTROL_STATION@01337.io", "AASD_CONTROL_STATION")
    drone = Drone("AASD_DRONE@01337.io", "AASD_DRONE", "AASD_CONTROL_STATION@01337.io")
    drones_monitor = DronesMonitor("AASD_DRONES_MONITOR@01337.io", "AASD_DRONES_MONITOR")
    drones_status_sender = DronesStatusSender("AASD_DRONES_STATUS_SENDER@01337.io", "AASD_DRONES_STATUS_SENDER")
    control_station_monitor = ControlStationMonitor("AASD_CONTROL_STATION_MONITOR@01337.io", "AASD_CONTROL_STATION_MONITOR")
    control_station_status_sender = ControlStationStatusSender("AASD_CONTROL_STATION_STATUS_SENDER@01337.io", "AASD_CONTROL_STATION_STATUS_SENDER")

    customer_future = customer.start()
    request_handler_future = requestHandler.start()
    control_station_future = controlStation.start()
    drone_future = drone.start()
    drones_monitor_future = drones_monitor.start()
    drones_status_sender_future = drones_status_sender.start()
    control_station_monitor_future = control_station_monitor.start()
    control_station_status_sender_future = control_station_status_sender.start()

    customer_future.result()  # Wait until the start method is finished
    request_handler_future.result()
    control_station_future.result()
    drone_future.result()
    drones_monitor_future.result()
    drones_status_sender_future.result()
    control_station_monitor_future.result()
    control_station_status_sender_future.result()

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
