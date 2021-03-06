import threading


# Note: No need class, all members are global and static
current_state = dict()     # Stores the current state of the world; no duplicated states
states = []
images = []
rewards = []
lock = threading.Lock()  # FIXME: Do we really need mutex here? We are only writing here from the messagereceiver thread, and only reading 

tick_data = []


def on_state_received(data):
    """Event for when state messages are received"""
    print(data)
    states.append((data['stateType'], data['value']))

        
def on_reward_received(data): 
    """Event for when reward messages are received"""
    print(data)
    rewards.append(data)

def on_step_received(data):
    states.append((data['state']))
    rewards.append((data['reward']))
    print("length:", len(states))
    
   