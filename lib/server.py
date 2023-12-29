# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------
import rester

class Server(rester.Rester):
    
    def __init__(self, host: str, port: int, led, loop, sensor_task, sensor):
        """
        Initializes a Server-object based on the Rester "api".
        
        :param host: str - the IPv4 addresse on which the server should run
        :param port: int - the port number for the server
        :param led: Leds - Leds-object so it can be controlled
        :param loop: event_loop - loop to cancel/reactivate sensor task
        :param sensor_task: task - currently running sensor task
        :param sensor: HCSR04 - sensor object needed for the async methode inside of it
        """
        super().__init__(self, host, port)
        self.led = led
        self.loop = loop
        self.sensor_task = sensor_task
        self.sensor = sensor
    
    def check_exceptions(self, color) -> bool:
        """
        Checks for exceptions that can be maybe when passing a value.
        
        :param color: (int, int, int) - the given color tuple to check for correctness
        :return: bool - is given color ok?
        """
        try:
            if not len(color) == 3:
                if len(color) == 4 and color[0] == 666 and color[1] == 666 and color[2] == 666 and color[3] > 0:
                    return True
                else:
                    raise Exception()
                    
            for col in color:
                        if not 0 <= col <= 255:
                            raise Exception()
            return True
        except:
            return False
    
    def get_changecolor(self, color) -> (str, ):
        """
        Changes the color of the LEDSchild to the given color inside the URL.
        
        :param color: the color given inside the URL as a parameter
        :return: str - HTTP.status
        """
        set_color = tuple(map(int, color.split(";")))
        if not self.check_exceptions(set_color):
            return self.BAD_REQUEST
        
        self.led.change_color(set_color)
        
        return self.OK
    
    def post_blocksensor(self) -> (str, ):
        """
        Blocks/Reactivates the HCSR04-sensor.
        
        :return: str - HTTP.status
        """
        if not self.sensor_task == None:
            self.sensor_task.cancel()
            self.sensor_task = None
        else:
            self.sensor_task = self.loop.create_task(self.sensor.change_by_distance())
        return self.OK
        
    def get_(self) -> (str, str):
        """
        Sends the index.html to the client.
        
        :return: (str, str) - (HTTP.status, html-code)
        """
        with open("assets/answer.html") as index:
            index_html = index.read()
            index.close()
        return (self.OK, index_html)
        
