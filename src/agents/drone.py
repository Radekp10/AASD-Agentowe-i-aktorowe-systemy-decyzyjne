from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message


STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "STATE_GIVE_FLIGHT_PROPOSITION"
STATE_THREE = "STATE_GET_DECISION"


class Drone(Agent):
    class DroneBehaviour(FSMBehaviour):
        async def on_start(self):
            print("[DRONE]: Starting behaviour . . .")

        async def on_end(self):
            print("[DRONE]: Behaviour finished with exit code {}.".format(self.exit_code))