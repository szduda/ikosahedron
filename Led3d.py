import neopixel
import board
from sys import sleep


class Led3d:
  led = None
  nodes = None

  def __init__(self, nodes, pin=board.D18):
    self.edge_size = 10
    self.led = neopixel.NeoPixel(pin, 300)
    self.nodes = nodes

  def ledx(self, a, b, n):
    from_led, to_led = self.nodes[a][b]
    return from_led + n if to_led > from_led else from_led - n

  def cx(self, a, b, n, color):
    x = self.ledx(a, b, n)
    self.led.fill(color, x)

  def fill_transition(self, led, t, duration=1000):
    for step in range(0, self.edge_size - 1):
      for end_point in range(0, len(t['to'])):
        for start_point in range(0, len(t['from'])):
          led.fill((0, 223, 127), self.ledx(start_point, end_point, step))
      sleep(duration / self.edge_size)

  def create_animation(self, frames, transform=fill_transition):
    def fn():
      for frame in frames:
        for t in frame['transitions']:
          transform(self.led, t, frame['duration'])
        sleep(frame['delay'])

    return fn


# wN - wierzchołek N
# lN - indeks leda w sekwencji (taśmie)
# w1: { w2: [l1, l2], w3:... }
ikosaeder = Led3d(nodes={
  0: {1: [0, 9], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]},
  1: {0: [9, 0], 5: [0, 0], 2: [10, 19], 6: [0, 0], 7: [0, 0]},
  2: {0: [0, 0], 1: [0, 0], 3: [0, 0], 7: [0, 0], 8: [0, 0]},
  3: {0: [0, 0], 2: [0, 0], 4: [0, 0], 8: [0, 0], 9: [0, 0]},
  4: {0: [0, 0], 3: [0, 0], 5: [0, 0], 9: [0, 0], 10: [0, 0]},
  5: {0: [0, 0], 4: [0, 0], 1: [0, 0], 10: [0, 0], 6: [0, 0]},
  6: {11: [0, 0], 10: [0, 0], 7: [0, 0], 5: [0, 0], 1: [0, 0]},
  7: {11: [0, 0], 6: [0, 0], 8: [0, 0], 1: [0, 0], 2: [0, 0]},
  8: {11: [0, 0], 7: [0, 0], 9: [0, 0], 2: [0, 0], 3: [0, 0]},
  9: {11: [0, 0], 8: [0, 0], 10: [0, 0], 3: [0, 0], 4: [0, 0]},
  10: {11: [0, 0], 9: [0, 0], 6: [0, 0], 4: [0, 0], 5: [0, 0]},
  11: {6: [0, 0], 7: [0, 0], 8: [0, 0], 9: [0, 0], 10: [0, 0]}
})

animate = ikosaeder.create_animation(frames=[{
  'duration': 1000,
  'delay': 0,
  'transitions': [
    {'from': [0], 'to': [1, 2, 3, 4, 5]}
  ]
}, {
  'transitions': [
    {'from': [1, 2, 3, 4, 5], 'to': [1, 2, 3, 4, 5]}
  ]
}, {
  'transitions': [
    {'from': [1, 2, 3, 4, 5], 'to': [6, 7, 8, 9, 10]}
  ]
}, {
  'transitions': [
    {'from': [6, 7, 8, 9, 10], 'to': [6, 7, 8, 9, 10]}
  ]
}, {
  'transitions': [
    {'from': [6, 7, 8, 9, 10], 'to': [11]}
  ]
}])

animate()
