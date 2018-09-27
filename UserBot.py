from time import time

class UserBot:
    def __init__(self, id_chat):
        self.chat_id = id_chat
        self.last_time = time()

    def update(self, interval=0):
        now = time()
        if(now - self.last_time >= interval):
            self.last_time = now
            return True
        else:
            return False
    def __str__(self):
        return self.chat_id