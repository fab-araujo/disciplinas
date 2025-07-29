class LightSwitch():
    def __init__(self):
        print("Constructor called")
        self.switchIsOn = False

    def turnOn(self):
        # turn the switch on 
         self.switchIsOn = True

    def turnOff(self):
        # turn the switch off
         self.switchIsOn = False

    def show(self):  # added for testing
        print(self.switchIsOn)

oLightSwitch1 = LightSwitch() # create a light switch object
oLightSwitch2 = LightSwitch() # create another light switch object