from agent.coordination import Action
from agent.coordination import CoordinateAction

action_coord = CoordinateAction(goal="PushTheBox", actions={
    "action1": [
        Action(name="Preparer", function=lambda a: print("Preparer l'action")),
        Action(name="Push", function=lambda a: print("Pousser la boite"))
    ],
    "action2": [
        Action(name="Preparer2", function=lambda a: print("Preparer l'action")),
        Action(name="Push2", function=lambda a: print("Pousser la boite"))]
})

exemple1 = [
    Action("Bouger1", function=lambda a: print("Je bouger ver x,y")),
    Action("Bouger2", function=lambda a: print("Je bouger ver x,y")),
    Action("Bouger3", function=lambda a: print("Je bouger ver x,y")),
    action_coord
]
