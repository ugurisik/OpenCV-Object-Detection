import time
class Logs:
    def __init__(self, log_file):
        self.log_file = log_file
    
    def write_to_log(self, exception):
        with open(self.log_file, 'a') as file:
            file.write('--- Log inserted Time:'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'  ---\n')
            file.write(str(exception))
            file.write('\n')