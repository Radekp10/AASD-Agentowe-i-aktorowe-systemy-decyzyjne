import time
import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.message import Message

from customer import Customer
from request_handler import RequestHandler

if __name__ == "__main__":
    customer = Customer("AASD_CUSTOMER@01337.io", "AASD_CUSTOMER")
    requestHandler = RequestHandler("AASD_REQUEST_HANDLER@01337.io", "AASD_REQUEST_HANDLER")
    future = customer.start()
    future2 = requestHandler.start()
    future.result()  # Wait until the start method is finished
    future2.result()

    while customer.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            customer.stop()
            requestHandler.stop()
            break
    print("Agents finished")

    quit_spade()
