from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import src.Messages as Messages

STATE_ONE = "GIVE_REQUIREMENTS_STATE"
STATE_TWO = "GET_FLIGHT_PROPOSITION_STATE"
STATE_THREE = "GIVE_DECISION_STATE"

START_STATION_ID = "AASD_CONTROL_STATION@01337.io"
END_STATION_ID = "AASD_CONTROL_STATION2@01337.io"
STATIONS_NUMBER = 20


class Customer(Agent):

    class CustomerBehaviour(FSMBehaviour):

        def __init__(self):
            super().__init__()

        async def on_start(self):
            print("[CUSTOMER]: Starting behaviour. . .")

        async def on_end(self):
            print("[CUSTOMER]: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print("[CUSTOMER]: I'm at state 1 (initial state)")
            flight_parameters = Message(to='AASD_REQUEST_HANDLER@01337.io')
            flight_parameters.set_metadata("performative", "request")  # Set the "inform" FIPA performative
            flight_parameters.body = Messages.c_flight_params_message(self.agent, START_STATION_ID, END_STATION_ID)
            await self.send(flight_parameters)
            print("[CUSTOMER]: Params sent: "+flight_parameters.body)

            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print("[CUSTOMER]: I'm at state 2")

            flight_proposition = await self.receive(timeout=30)  # wait for a message for 10 seconds
            if flight_proposition:
                print("[CUSTOMER]: Message received with content: {}".format(flight_proposition.body))
            else:
                print("[CUSTOMER]: Did not received any message after 10 seconds")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print("[CUSTOMER]: I'm at state 3")
            customer_decision = Message(to='AASD_REQUEST_HANDLER@01337.io')
            customer_decision.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            customer_decision.body = Messages.c_affirmative_decision(self.agent)
            await self.send(customer_decision)
            print("[CUSTOMER]: Decision sent")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.customerBehaviour = self.CustomerBehaviour()

    async def setup(self):
        print("[CUSTOMER]: Agent starting . I'm agent {}".format(str(self.jid)))
        self.customerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(str(self.jid)), initial=True)
        self.customerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo(str(self.jid)))
        self.customerBehaviour.add_state(name=STATE_THREE, state=self.StateThree(str(self.jid)))
        self.customerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.customerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(self.customerBehaviour)
