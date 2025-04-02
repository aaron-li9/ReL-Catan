#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
#from keras.callbacks import TensorBoard
#from keras.optimizers import Adam

#For some reason all the keras imports don't even work on my computer, they produce "illegal hardware instruction" errors!

from collections import deque
import numpy as np
import time

DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 50_000  # How many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)

#For (state, action, new_state, reward), see Game.py

class DQNAgent:

    def __init__(self, game):

        self.game = game

        """
        #Main model
        self.model = self.create_model()

        #Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        #An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0
        """

    #SEE Game.py for the reward function, it takes an old state and a new state and generates a reward

    """
    def create_model(self):
        model = Sequential()
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.2))
        model.add(Dense(48))
        model.add(Activation("relu"))
        model.add(Dropout(0.2))
        model.add(Dense(48))
        model.add(Dense(15), activation = "softmax")     #because 15 is the number of actions you can do every turn, although it's probably more
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model

    #experience update
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state, step):
        return self.model.predict(np.array(state).reshape(-1, *state.shape) / 255)[0]

    # Trains main network every step during episode
    def train(self, terminal_state, step):
        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return
        # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = np.array([transition[0] for transition in minibatch]) / 255
        current_qs_list = self.model.predict(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = np.array([transition[3] for transition in minibatch]) / 255
        future_qs_list = self.target_model.predict(new_current_states)
        
    """
