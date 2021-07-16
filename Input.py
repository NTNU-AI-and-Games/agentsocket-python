class Key:   # Use ActionMapping instead?
    def __init__(self, keycode: str):
        self.keycode = keycode
        self._is_pressed = False
    

    def is_pressed(self):
        return self._is_pressed
    



class Axis:   # Use AxisMapping instead?
    def __init__(self, name: str):
        self.name = name
        self._value = 0
    
    def get_value(self):
        return self._value
        
    
    

class Action:   # Use AxisMapping instead?

    def __init__(self, name, action_type = "ONCE", value = ""):
        self.name = name
        self.type = action_type
        self.value = value
        
    def __str__(self) -> str:
        return f'{self.name} {self.type}{self.value}'
    
    def to_command(self):
        return f'action {self.name} {"" if self.type == "ONCE" else self.type + " "}{self.value}'

    def to_dict(self) -> dict:
        return {
            'ActionName': self.name,
            'ActionType': self.type,
            'value': self.value,
        }

