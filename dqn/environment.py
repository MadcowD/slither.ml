import gym
import random
import numpy as np
from .utils import rgb2gray, imresize

class Environment(object):
  def __init__(self, config):
    self.env = gym.make(config.env_name)

    screen_width, screen_height, self.action_repeat, self.random_start = \
        config.screen_width, config.screen_height, config.action_repeat, config.random_start

    self.display = config.display
    self.dims = (screen_height, screen_width)

    self._screen = None
    self._last_screen = None
    self._reward = [0]
    self._terminal = True

  def new_game(self, from_random_game=False):
    self._screen = self.env.reset()
    while not self._screen or self._screen[0] is None:
        ret = self._step(0)
        if ret:
            self._screen, _, _ = ret
       
    self._step(0)
    self.render()
    return self.screen, 0, 0, self.terminal

  def new_random_game(self):
    self.new_game(True)
    for _ in range(random.randint(0, self.random_start - 1)):
      self._step(0)
    self.render()
    return self.screen, 0, 0, self.terminal

  def _step(self, action):
    self._screen, self._reward, self._terminal, _ = self.env.step(action)
  def _random_step(self):
    action = self.env.action_space.sample()
    self._step(action)

  @property
  def screen(self):
    if not self._screen or self._screen[0] is None:
      self._screen = self._last_screen
    screen = self._screen[0]['vision']
    return imresize(rgb2gray(screen)/255., self.dims)
    #return cv2.resize(cv2.cvtColor(self._screen, cv2.COLOR_BGR2YCR_CB)/255., self.dims)[:,:,0]
  @property
  def action_size(self):
    return self.env.action_space.n

  @property
  def terminal(self):
    return self._terminal[0]

  @property
  def reward(self):
    return self._reward[0]
  @property
  def lives(self):
    return self.env.ale.lives()

  @property
  def state(self):
    return self.screen, self.reward, self.terminal

  def render(self):
    if self.display:
      self.env.render()

  def after_act(self, action):
    self.render()

class GymEnvironment(Environment):
  def __init__(self, config):
    super(GymEnvironment, self).__init__(config)

  def act(self, action, is_training=True):
    cumulated_reward = 0
    start_lives = self.lives

    for _ in range(self.action_repeat):
      self._step(action)
      cumulated_reward = cumulated_reward + self.reward

      if is_training and start_lives > self.lives:
        cumulated_reward -= 1
        self.terminal = True

      if self.terminal:
        break

    self.reward = cumulated_reward

    self.after_act(action)
    return self.state

class SimpleGymEnvironment(Environment):
  def __init__(self, config):
    super(SimpleGymEnvironment, self).__init__(config)

  def act(self, action, is_training=True):
    self._step(action)

    self.after_act(action)
    return self.state




class UniverseEnvironment(Environment):
  def __init__(self, config):
    super(UniverseEnvironment, self).__init__(config)
#    self.env.configure(remotes='vnc://localhost:5900+15900')
    self.env.configure(remotes=1)
  @property
  def action_size(self):
    return 5

  def _step(self, action):
    act_dict = {
      0 : [('KeyEvent', 'ArrowLeft', True),
           ('KeyEvent', 'ArrowRight', False),
           ('KeyEvent', 'space', False)],
      1 : [('KeyEvent', 'ArrowRight', True),
           ('KeyEvent', 'ArrowLeft', False),
           ('KeyEvent', 'space', False)],
      2: [('KeyEvent', 'space', False),
          ('KeyEvent', 'ArrowLeft', False),
          ('KeyEvent', 'ArrowRight', False)],
      3 : [('KeyEvent', 'ArrowLeft', True),
           ('KeyEvent', 'ArrowRight', False),
           ('KeyEvent', 'space', False)],
      4 : [('KeyEvent', 'ArrowRight', True),
           ('KeyEvent', 'ArrowLeft', False),
           ('KeyEvent', 'space', False)],
    }
    self._last_screen = self._screen
    self._screen, self._reward, self._terminal, _ = self.env.step([act_dict[action]])
   # if not self._screen or self._screen[0] is None:
   #   self._terminal = [True]
   #   self._screen = [{'vision': None}]


  def _random_step(self):
    
    x = np.random.randint(5) + 1
    self._step(x)

  def act(self, action, is_training=True):
    self._step(action)
    return self.state

  def render(*args, **kwargs):
    pass

  @property
  def screen(self):
    if not self._screen or self._screen[0] is None:
      self._screen = self._last_screen
    screen = self._screen[0]['vision'][21:512,83:384]
    return imresize(rgb2gray(screen)/255., self.dims)

  @property
  def lives(self):
    return 1
