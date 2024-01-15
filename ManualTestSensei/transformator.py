from datetime import datetime

class Transformator:
    def __init__(self):
        self.start = 0
        with open(self.smell, 'w') as f:
            f.write('')
        return True

    def start_counting_time(self) -> bool:
        self.start = 0
        self.start = datetime.now()
        return True

    def stop_counting_time(self) -> float:
        end = datetime.now()
        total = end - self.start
        self.start = 0
        total = total.total_seconds()
        with open(self.smell, 'a') as f:
            f.write(str(total)+'\n')
        return total