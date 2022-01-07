from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "SEND_REQUEST_ABOUT_AVAILABLE_DRONES_STATE"
STATE_THREE = "GET_RESPONSE_ABOUT_AVAILABLE_DRONES_STATE"
STATE_FOUR = "GIVE_FLIGHT_PROPOSITION_STATE"
STATE_FIVE = "GET_DECISION_STATE"
STATE_SIX = "SEND_START_RESERVATION_STATE"
STATE_SEVEN = "SEND_END_RESERVATION_STATE"


class RequestHandler(Agent):
    class RequestHandlerBehaviour(FSMBehaviour):
        async def on_start(self):
            print("[REQUEST_HANDLER]: Starting behaviour . . .")

        async def on_end(self):
            print("[REQUEST_HANDLER]: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 1")
            flight_parameters = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if flight_parameters:
                print("[REQUEST_HANDLER]: Message received with content: {}".format(flight_parameters.body))
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")
            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 2")
            are_drones_available_request = Message(to='AASD_CONTROL_STATION@01337.io')
            are_drones_available_request.set_metadata("performative", "inform")
            are_drones_available_request.body = "Are drones available?"
            await self.send(are_drones_available_request)
            print("[REQUEST_HANDLER]: Request about available drones sent")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 3")
            are_drones_available_response = await self.receive(timeout=10)
            if are_drones_available_response:
                print("[REQUEST_HANDLER]: Message received with content: {}".format(are_drones_available_response.body))
                self.set_next_state(STATE_FOUR)
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")

    class StateFour(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 4")
            flight_proposition = Message(to='AASD_CUSTOMER@01337.io')
            flight_proposition.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            flight_proposition.body = "Flight proposition"
            await self.send(flight_proposition)
            print("[REQUEST_HANDLER]: Proposition sent")
            self.set_next_state(STATE_FIVE)

    class StateFive(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 5")
            customer_decision = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if customer_decision:
                print("[REQUEST_HANDLER]: Message received with content: {}".format(customer_decision.body))
                self.set_next_state(STATE_SIX)
            else:
                print("[REQUEST_HANDLER]: Did not received any message after 10 seconds")

    class StateSix(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 6")
            reservation_start = Message(to='AASD_CONTROL_STATION@01337.io')  # wait for a message for 10 seconds
            reservation_start.set_metadata("performative", "inform")
            reservation_start.body = "Start station reservation"
            print("[REQUEST_HANDLER]: Start reservation sent")
            self.set_next_state(STATE_SEVEN)

    class StateSeven(State):
        async def run(self):
            print("[REQUEST_HANDLER]: I'm at state 7")
            reservation_end = Message(to='AASD_CONTROL_STATION@01337.io')  # wait for a message for 10 seconds
            reservation_end.set_metadata("performative", "inform")
            reservation_end.body = "End station reservation"
            await self.send(reservation_end)
            print("[REQUEST_HANDLER]: End reservation sent")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.requestHandlerBehaviour = self.RequestHandlerBehaviour()

    async def setup(self):
        print("[REQUEST_HANDLER]: Agent starting . I'm agent {}".format(str(self.jid)))
        self.requestHandlerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.requestHandlerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.requestHandlerBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.requestHandlerBehaviour.add_state(name=STATE_FOUR, state=self.StateFour())
        self.requestHandlerBehaviour.add_state(name=STATE_FIVE, state=self.StateFive())
        self.requestHandlerBehaviour.add_state(name=STATE_SIX, state=self.StateSix())
        self.requestHandlerBehaviour.add_state(name=STATE_SEVEN, state=self.StateSeven())
        self.requestHandlerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.requestHandlerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.requestHandlerBehaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        self.requestHandlerBehaviour.add_transition(source=STATE_FOUR, dest=STATE_FIVE)
        self.requestHandlerBehaviour.add_transition(source=STATE_FIVE, dest=STATE_SIX)
        self.requestHandlerBehaviour.add_transition(source=STATE_SIX, dest=STATE_SEVEN)
        self.add_behaviour(self.requestHandlerBehaviour)