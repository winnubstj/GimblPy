import paho.mqtt.client as mqtt
import json


class GimblControl:

    # Private
    _client = mqtt.Client()
    _colFlag = False

    # Public
    isRunning = False

    # Constructor
    def __init__(self):
        # Connect to Broker.
        self._client.connect("127.0.0.1", 1883)
        # Subscription for Status change.
        self._client.on_message = self._collision  # for waitoncollision.
        self._statusSub = self._client.subscribe("Gimbl/Session/+")
        self._client.message_callback_add("Gimbl/Session/+", self._statuschange)
        self._client.loop_start()

    # MQTT Functions.
    # Send Message.
    def send_message(self, topic, message):
        self._client.publish(topic,message)
    # Log.
    def log(self,message):
        content = "{{\"source\": \"Python\", \"msg\":\"{}\" }}".format(message)
        self._client.publish("Log/", content)
    # Session Functions.
    def wait_on_start(self):
        print("Waiting for Gimbl start")
        self.isRunning = False
        while self.isRunning==False:
            pass
    # WaitOnCollision
    def wait_on_collision(self, name):
        topic = "Gimbl/{}/Collision".format(name)
        mySub = self._client.subscribe(topic)
        while self._colFlag==False:
            pass
        self._colFlag = False
        self._client.unsubscribe(topic)
    # Collision.
    def _collision(self,client,userdata,msg):
        print(msg.topic)
        self._colFlag = True

    # AddCollisionCallback.
    def add_collision_callback(self, name, fnc):
        # subscribe.
        topic = "Gimbl/{}/Collision".format(name)
        self._client.subscribe(topic)
        # set callback
        callback = lambda client, userdata, msg : self._collision_callback(msg, name, fnc)
        self._client.message_callback_add(topic,callback)

    def _collision_callback(self, msg, name, fnc):
        data = json.loads(msg.payload)
        fnc(name,data['collider'])

    # Object Functions.
    # Move
    def move(self, name, x, y, z):
        self._send_command(name, "Move", self._arraystring(x, y, z))

    # MoveTo
    def move_to(self, name, x, y, z):
        self._send_command(name, "MoveTo", self._arraystring(x, y, z))

    # Rotate
    def rotate(self, name, rot):
        self._send_command(name, "Rotate", self._valuestring(rot))

    # RotateTo
    def rotate_to(self, name, rot):
        self._send_command(name, "RotateTo", self._valuestring(rot))

    # SetColor
    def set_color(self,name, r, g, b):
        self._send_command(name, "SetColor", self._arraystring(r, g, b))

    # SetMaterial
    def set_material(self,name,mat):
        self._send_command(name, "SetMaterial", self._stringmsg(mat))

    # SetTexture
    def set_texture(self,name,tex):
        self._send_command(name, "SetTexture", self._stringmsg(tex))

    # SetOpacity
    def set_opacity(self,name,value):
        self._send_command(name, "SetOpacity", self._valuestring(value))

    # SetVisibility
    def set_visibility(self,name,value):
        self._send_command(name, "SetVisibility", self._boolstring(value))

    # PlaySound
    def play_sound(self,name,value):
        self._send_command(name, "PlaySound", self._boolstring(value))

    # SetBrightness
    def set_brightness(self,name,value):
        self._send_command(name, "SetBrightness", self._valuestring(value))

    # Blink
    def blink(self,name,darkTime,fadeTime,disable):
        self._send_command(name, "Blink", self._blinkmsg(darkTime, fadeTime, disable))

    # Session Status change.
    def _statuschange(self, client, userdata, msg):
        if msg.topic == "Gimbl/Session/Start":
            print("Gimbl: session started")
            self.isRunning = True
        else:
            print("Gimbl: session ended")
            self.isRunning = False

    # Send Command.
    def _send_command(self, name, fncName, msg):
        self._client.publish("Gimbl/{0}/{1}".format(name, fncName), msg)

    def _arraystring(self, x, y, z):
        return "{{\"array\":[{},{},{}]}}".format(x, y, z)

    def _valuestring(self,value):
        return "{{\"value\":{}}}".format(value)

    def _boolstring(self,value):
        return "{{\"flag\":\"{}\"}}".format(value)

    def _stringmsg(self,str):
        return "{{\"strMsg\":\"{}\"}}".format(str)

    def _blinkmsg(self,darkTime,fadeTime,disable):
        return "{{\"darkTime\":{}, \"fadeTime\":{}, \"disable\":\"{}\"}}".format(darkTime*1000,fadeTime*1000,disable)


