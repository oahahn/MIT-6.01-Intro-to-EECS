class Hammock:
    """
    Keeps track of who is allowed to sit on a hammock. If the hammock is empty, 
    then anyone can sit on it. If the hammock is not empty, then a new request 
    to sit on it will be refused. However, if the next request to sit is from 
    the same person who was refused last time, then the request is granted.
    """
    def __init__(self):
        self.state = 0
        self.lastRequest = ''
    
    def sitDown(self, name):
        if self.state == 0 or self.lastRequest == name:
            self.state += 1
            print('welcome!')
        else:
            self.lastRequest = name
            print('sorry, no room')

    def leave(self):
        if self.state > 0:
            self.state -= 1
        print(self.state)

# Testing output
myHammock = Hammock()
myHammock.sitDown('George') 
# welcome!
myHammock.sitDown('Bobby') 
# sorry, no room
myHammock.sitDown('Bobby') 
# welcome!
myHammock.leave()
# 1
myHammock.leave()
# 0
myHammock.leave()
# 0
myHammock.sitDown('Martha') 
# welcome!
myHammock.sitDown('Wilhelm') 
# sorry, no room
myHammock.sitDown('Klaus') 
# sorry, no room
myHammock.sitDown('Wilhelm')
myHammock.sitDown('Wilhelm') 
# sorry, no room
myHammock.leave()
# 0