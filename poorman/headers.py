class RequestHeaders:
    def __init__(self, headers):
        self.headers = headers
    
    def add_header(self, key, value):
        self.headers[key] = value
    
    def update_header(self, key, value):
        if key in self.headers:
            self.headers[key] = value
        else:
            raise KeyError("Header not found")
    
    def get_header(self, key):
        if key in self.headers:
            return self.headers[key]
        else:
            raise KeyError("Header not found")