import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import src.Messages as Messages

STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "SEND_REQUEST_ABOUT_AVAILABLE_DRONES_STATE"
STATE_THREE = "GET_RESPONSE_ABOUT_AVAILABLE_DRONES_STATE"
STATE_FOUR = "GIVE_FLIGHT_PROPOSITION_STATE"
STATE_FIVE = "GET_DECISION_STATE"
STATE_SIX = "SEND_START_RESERVATION_STATE"
STATE_SEVEN = "SEND_END_RESERVATION_STATE"
STATE_EIGHT = "SEND_FLIGHT_PARAMETERS_TO_DRONE_STATE"


class RequestHandler(Agent):
    class RequestHandlerBehaviour(FSMBehaviour):

        async def on_start(self):
            print("[REQUEST_HANDLER]: Starting behaviour . . .")

        async def on_end(self):
            print("[REQUEST_HANDLER]: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):

        def __init__(self):
            super().__init__()

        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 1")
            flight_parameters = await self.receive(timeout=30)  # wait for a message for 10 seconds
            if flight_parameters:
                message = json.loads(flight_parameters.body)
                customerId = message['customerId']
                startStationId = message['startStationId']
                endStationId = message['endStationId']
                print("[REQUEST_HANDLER]: Message received with content: {}".format(flight_parameters.body))

                status_msg = Message(to=self.agent.jid)
                status_msg.set_metadata("performative", "inform")
                status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, None)
                await self.send(status_msg)
                self.set_next_state(STATE_TWO)
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")

    class StateTwo(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 2")
            status = await self.receive(timeout=20)
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                are_drones_available_request = Message(to='AASD_CONTROL_STATION@01337.io')
                are_drones_available_request.set_metadata("performative", "inform")
                are_drones_available_request.body = Messages.rh_drones_available_request(self, startStationId, endStationId, customerId, None)
                await self.send(are_drones_available_request)
                print("[REQUEST_HANDLER]: Request about available drones sent")

                status_msg = Message(to=self.agent.jid)
                status_msg.set_metadata("performative", "inform")
                status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, None)
                await self.send(status_msg)
                self.set_next_state(STATE_THREE)

    class StateThree(State):
        def __init__(self):
            super().__init__()

        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 3")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']

            are_drones_available_response = await self.receive(timeout=10)
            if are_drones_available_response:
                print("[REQUEST_HANDLER]: Message received with content: {}".format(are_drones_available_response.body))
                message = json.loads(are_drones_available_response.body)
                availableDroneId = message['droneId']

                status_msg = Message(to=self.agent.jid)
                status_msg.set_metadata("performative", "inform")
                status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, availableDroneId)
                await self.send(status_msg)
                self.set_next_state(STATE_FOUR)
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")

    class StateFour(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 4")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            droneId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                droneId = status['droneId']

            flight_proposition = Message(to='AASD_CUSTOMER@01337.io')
            flight_proposition.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            flight_proposition.body = Messages.rh_flight_proposition_info(self.agent, droneId, customerId)
            await self.send(flight_proposition)
            print("[REQUEST_HANDLER]: Proposition sent")

            status_msg = Message(to=self.agent.jid)
            status_msg.set_metadata("performative", "inform")
            status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, droneId)
            await self.send(status_msg)
            self.set_next_state(STATE_FIVE)

    class StateFive(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 5")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            droneId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                droneId = status['droneId']

            customer_decision = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if customer_decision:
                print("[REQUEST_HANDLER]: Message received with content: {}".format(customer_decision.body))
                status_msg = Message(to=self.agent.jid)
                status_msg.set_metadata("performative", "inform")
                status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, droneId)
                await self.send(status_msg)
                self.set_next_state(STATE_SIX)
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")

    class StateSix(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 6")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            droneId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                droneId = status['droneId']

            reservation_start = Message(to='AASD_CONTROL_STATION@01337.io')  # wait for a message for 10 seconds
            reservation_start.set_metadata("performative", "inform")
            reservation_start.body = Messages.rh_start_flight_reservation(self.agent, droneId, customerId,
                                                                          startStationId, endStationId)
            print("[REQUEST_HANDLER]: Start reservation sent")
            status_msg = Message(to=self.agent.jid)
            status_msg.set_metadata("performative", "inform")
            status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, droneId)
            await self.send(status_msg)
            self.set_next_state(STATE_SEVEN)

    class StateSeven(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 7")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            droneId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                droneId = status['droneId']

            reservation_end = Message(to='AASD_CONTROL_STATION@01337.io')  # wait for a message for 10 seconds
            reservation_end.set_metadata("performative", "inform")
            reservation_end.body = Messages.rh_end_flight_reservation(self.agent, droneId, customerId, endStationId)
            await self.send(reservation_end)
            print("[REQUEST_HANDLER]: End reservation sent")
            status_msg = Message(to=self.agent.jid)
            status_msg.set_metadata("performative", "inform")
            status_msg.body = Messages.rh_status(self, startStationId, endStationId, customerId, droneId)
            await self.send(status_msg)
            self.set_next_state(STATE_EIGHT)

    class StateEight(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 8")
            status = await self.receive(timeout=20)
            customerId = None
            startStationId = None
            endStationId = None
            droneId = None
            if status:
                customerId = status['customerId']
                startStationId = status['startStationId']
                endStationId = status['endStationId']
                droneId = status['droneId']

            flight_parameters = Message(to='AASD_DRONE@01337.io')  # wait for a message for 10 seconds
            flight_parameters.set_metadata("performative", "inform")
            flight_parameters.body = Messages.rh_flight_parameters(self.agent, droneId, customerId, startStationId, endStationId)
            await self.send(flight_parameters)
            print("[REQUEST_HANDLER]: Flight parameters sent")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.requestHandlerBehaviour = self.RequestHandlerBehaviour()
        self.customerId = None
        self.startStationId = None
        self.endStationId = None

    async def setup(self):
        print("[REQUEST_HANDLER]: Agent starting . I'm agent {}".format(str(self.jid)))
        self.requestHandlerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.requestHandlerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.requestHandlerBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.requestHandlerBehaviour.add_state(name=STATE_FOUR, state=self.StateFour())
        self.requestHandlerBehaviour.add_state(name=STATE_FIVE, state=self.StateFive())
        self.requestHandlerBehaviour.add_state(name=STATE_SIX, state=self.StateSix())
        self.requestHandlerBehaviour.add_state(name=STATE_SEVEN, state=self.StateSeven())
        self.requestHandlerBehaviour.add_state(name=STATE_EIGHT, state=self.StateEight())
        self.requestHandlerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.requestHandlerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.requestHandlerBehaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        self.requestHandlerBehaviour.add_transition(source=STATE_FOUR, dest=STATE_FIVE)
        self.requestHandlerBehaviour.add_transition(source=STATE_FIVE, dest=STATE_SIX)
        self.requestHandlerBehaviour.add_transition(source=STATE_SIX, dest=STATE_SEVEN)
        self.requestHandlerBehaviour.add_transition(source=STATE_SEVEN, dest=STATE_EIGHT)
        self.add_behaviour(self.requestHandlerBehaviour)
