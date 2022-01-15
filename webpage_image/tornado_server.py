import tornado.ioloop
import tornado.web
import tornado.websocket
import cv2
import cvfilters
import colors
from PIL import Image
from io import BytesIO
import logging
import time
import base64

logger = logging.getLogger('imagestream')

from tornado.options import define, options, parse_command_line

define("port", default = 2601, type = int)

def convert_to_jpg(image):
    """TBW."""
    im = Image.fromarray(image)
    mem_file = BytesIO()
    im.save(mem_file, 'JPEG')
    return mem_file.getvalue()

#Handles a call to the base (localhost:2601/ or index.html)
class IndexHandler(tornado.web.RequestHandler):
    # get request to get base webpage (index) from tornado server
    def get(self):
        self.render("index.html")

#starts websocket connection
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    #funcion to opena  new connection
    def open(self, *args):
        print("new connection")
        self.write_message("welcome!")
    
    def on_message(self, message):
        print('MSG: {}'.format(message.upper())) #what shows as response to new message from client
        
        
        self.write_message(message.lower()) #what shows in the HTML


        boing = "red"

        while(True):
            if(message.lower() == "red"):
                boing = "red"
            elif(message.lower() == "blue"):
                boing = "blue"

            
        # print("this is " + boing)
            
              

     
    def on_close(self):
        print("connection closed")
    
    @staticmethod
    def read_image_loop(application):
        """TBW."""
        cam = application.settings['camera']
        while not WebsocketHandler.stop_event.is_set():
            interval = float(WebsocketHandler.interval) / 1000.0
            if interval > 0:
                if len(application.settings['sockets']):
                    _, image = cam.read()

                    # image = cv2.resize(image, ((int)(640), (int)(400)), 0, 0, cv2.INTER_CUBIC)
                    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


                    jpg = convert_to_jpg(image)
                    for ws in application.settings['sockets']:
                        ws.images.append(jpg)

                interval = 0.001
            else:
                interval = 1.0  # paused
            time.sleep(interval)
        #logger.info('Exiting WebsocketHandler.read_image_loop')



app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebsocketHandler)

])

if __name__ == "__main__":
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

