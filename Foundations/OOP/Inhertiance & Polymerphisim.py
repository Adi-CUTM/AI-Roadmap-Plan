# Inheritance

class car:
    color = "Black"
    
    def start(self):
       return "Car started"
    
    def stop(self):
        return "car stoped"

class toyota(car):
    def info(self):
        print(f" Toyota car which color is {self.color} is {self.start()} and {self.stop()}")

car1 = toyota()
car1.info()

