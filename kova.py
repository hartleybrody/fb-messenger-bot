class Kova:

    def __init__(self):
      self.chapter = 0

    def chat(self, input):
        self.chapter += 1
        return "I see that you said " + str(self.chapter) + ' times'
