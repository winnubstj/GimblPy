import GimblPy


class Script:
    gimbl = GimblPy.GimblControl()

    def hit_test(self, name, collider):
        print("{} touched {}".format(name, collider))

    def main_loop(self):
        # Do something interesting here.
        pass

    def start(self):
        # set a collision detection.
        self.gimbl.add_collision_callback("Mouse", self.hit_test)
        # wait for start,
        self.gimbl.wait_on_start()
        # run while session is going.
        while self.gimbl.isRunning:
            self.main_loop()
            pass


if __name__ == '__main__':
    Script().start()


