The goal of the project is to develop an agent that:
1. Perform tasks demanded by user
2. Autonomously explore the web and learn from it
3. Have conversations in natural language. 

Perception:
Optical Character Recognition, Object Detection and HTML parsing are used to perceive the environment.

Fundamental Actions: click, scroll, move mouse, screenshot, obtain iteractables from HTML

State variables: previous action

Learning: 
As of now, a basic learning method is employed.
The agent keeps track of the previous action.
The agent chooses next action based on transition function next_action = F(previous action,previous action return value).
The agent is able to learn the basic dos and donts. For example, after click action, the next action it selects is the perceive action.
More sophisticated methods will be employed.

Method of knowledge representation and language modelling are being explored.
This repo will be updated regularly.