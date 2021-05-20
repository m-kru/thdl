from . import file_info

class Checker():
    def __init__(self):
        self.silent = False

    def message(self, msg):
        if not self.silent:
            print("{}:{}".format(file_info.FILEPATH, file_info.LINE_NUMBER))
            print(file_info.LINE, end='')
            print(msg + "\n")

        return msg
