class PortManager:
    def __init__(self, start_port=8000, end_port=9000):
        self.start_port = start_port
        self.end_port = end_port
        self.used_ports = set()

    def get_available_port(self):
        for port in range(self.start_port, self.end_port):
            if port not in self.used_ports:
                self.used_ports.add(port)
                return port
        raise Exception("No available ports")

    def release_port(self, port):
        self.used_ports.discard(port)
