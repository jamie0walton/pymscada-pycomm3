from pymscada import BusClient

class EIPClient:

    def __init__(self, bus_ip: str = '127.0.0.1', bus_port: int = 1324,
                 rtus: dict = {}, tags: dict = {}) -> None:
        """
        Connect to bus on bus_ip:bus_port, serve on ip:port for webclient.

        Serves the webclient files at /, as a relative path. The webclient uses
        a websocket connection to request and set tag values and subscribe to
        changes.

        Event loop must be running.
        """
        self.busclient = None
        if bus_ip is not None:
            self.busclient = BusClient(bus_ip, bus_port)
        pass

    async def start(self):
        """Provide a web server."""
        pass
