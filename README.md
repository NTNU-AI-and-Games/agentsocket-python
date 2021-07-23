# agentsocket-python

agentsocket-python serves as a tunnel for agents to remotely connect to the 
[AgentSocket](https://github.com/NTNU-AI-and-Games/AgentSocket "AgentSocket's Github Repo") plugin made for Unreal Engine.
With this library, the agents will have to ability to input arbritry actions and keys to a game, and receive updated states responses.

agentsocket-python is made with reinforcement learning support in mind, such that agents will wait for a step response for each step action.


## Gettings Started
1. Install dependencies with `pip install -r requirements.txt`

Run any of the following files:
 - TCPClient.py
 - AgentSocketOnlyStream.py
 - AgentSocketStepListener.py
 
 

## Notes
Many of the files are outdated, and may need to be updated to properly interpret responses of the AgentSocket plugin for Unreal Engine 4.
