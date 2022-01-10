import datetime
import json
import random

from spade.agent import Agent

STATIONS_NUMBER = 20

# CONTROL_STATION
CD_DRONES_AVAILABLE = "Drones available"

# CUSTOMER
C_FLIGHT_PARAMS = "Flight parameters: start_point_id: {}, end_point_id: {}"
C_AFFIRMATIVE_DECISION = "Decision affirmative"

# DRONE

# REQUEST_HANDLER
RH_RQ_DRONES_AVAILABLE = "Are drones available?"
RH_RQ_FLIGHT_PROPOSITION = "Flight proposition"
RH_START_RESERVATION = "Start station reservation"
RH_END_RESERVATION = "End station reservation"
RH_FLIGHT_PARAMETERS = "Flight parameters"


# CONTROL_STATION

def drones_available_req_message(agent: Agent):
    drones_available_request = {
        "controlStationId": agent.jid,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(drones_available_request)



# CUSTOMER

def flight_params_message(agent: Agent):
    flight_request_params = {
        "customerId": agent.jid,
        "startStationId": str (random.randrange(0, STATIONS_NUMBER, 1)),
        "endStationId": str (random.randrange(0, STATIONS_NUMBER, 1)),
        "createDate": datetime.datetime.now()
    }
    return json.dumps(flight_request_params)


def affirmative_decision(agent: Agent):
    decision = {
        "customerId": agent.jid,
        "decision": True,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision)


def reject_decision(agent: Agent):
    decision = {
        "customerId": agent.jid,
        "decision": False,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision)


# REQUEST_HANDLER
def drones_available_request(agent: Agent, controlStationId: str, startStationId: str, endStationId: str):
    request = {
        "requestHandlerId": agent.jid,
        "controlStationId": controlStationId,
        "startStationId": startStationId,
        "endStationId": endStationId,

    }
    return json.dumps(request)

