import threading


# Note: No need class, all members are global and static
current_state = dict()     # Stores the current state of the world; no duplicated states
states = []
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
    """Event for when tick messages are received
    
    example: {
        "type": "tick",
        "data": {
            actionIds: []
            state: {
                players: [
                    player1: {
                        transform: {
                            position: {
                                x: 1,
                                y: 2,
                                z: 7
                            },
                            rotation: {
                                ...
                            }
                        }
                        dead: false,
                        team: 1,
                    },
                    player2: {
                        transform: {...}
                        dead: true,
                        team: 0,
                    }
                ],
                building: [
                    build1: {
                        destroyed: false
                    },
                    platforms: [
                        # created by the players
                    ]
                ]
            },
            reward: 4,
        }
    }

    """
    #print(data)
    states.append((data['state']))
    print("length:", len(states))
    
   