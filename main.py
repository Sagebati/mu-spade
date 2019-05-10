import logging

logging.basicConfig(filename='test_log.log', level=logging.INFO,
                    format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

pwd = "dummy"
jwd1 = "turtle_a@127.0.0.1"
jwd2 = "turtle_b@127.0.0.1"

if __name__ == '__main__':
    from agent.Turtle import Turtle
    from exemples.exemple import exemple1
    turtleBot_a = Turtle(jwd1, pwd, exemple1, [jwd2])
    turtleBot_b = Turtle(jwd2, pwd, exemple1, [jwd1])
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_b.start()
    turtleBot_b.web.start(hostname="127.0.0.1", port="10001")
    turtleBot_b.stop()
    turtleBot_a.stop()
