import time
from threading import Thread


class TimerCounter:
    def __init__(self, prefixMsg: str | None = None):
        self.is_break = False
        self.t = None
        self.counter = 1
        self.prefixMsg = prefixMsg if prefixMsg is not None else 'Waiting '

    def __FormatWaitMsg(self) -> str:
        return f'{self.prefixMsg}: {self.counter} sec(s)'

    # private method (Start with __)
    def __Counting(self):
        while True:
            print(self.__FormatWaitMsg(), end='\r', flush=True)
            time.sleep(1) # รอ 1 วินาทีแล้วค่อยนับต่อ
            self.counter += 1
            if self.is_break == True:
                break


    def StartWaiting(self):
        self.is_break = False
        self.t = Thread(target=self.__Counting, args=[])
        #self.t = threading.currentThread().__init__(target=self.counter, args=[])
        self.t.start()

    def StopWaiting(self):
        self.is_break = True
        self.t = None
        self.counter = 1
        return self.__FormatWaitMsg()
