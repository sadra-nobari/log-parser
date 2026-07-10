from collections import Counter
from parser import LogEntry

class Statistics:
    def __init__(self):
        self.total_requests = 0
        self.total_errors = Counter()
        self.total_pass = Counter()
        self.ip_counts = Counter()


    def entry_proc(self, entry: LogEntry):
        self.total_requests += 1

        #proccessing status codes
        if entry.status in [400, 401, 403, 404, 500, 502, 503]:
            self.total_errors[entry.status] += 1
        else:
            self.total_pass[entry.status] += 1

        #proccessing ip counts
        self.ip_counter(entry.ip)


    def ip_counter(self, ip):
        self.ip_counts[ip]+=1
    
    
