import pygame
import random
import sys
import torch

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the window size
window_size = (600, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Snake")

# Set up the clock
clock = pygame.time.Clock()

# Set up the snake
snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill(WHITE)

# Set up the apple
apple_pos = (random.randint(0,59)*10,random.randint(0,59)*10)
apple = pygame.Surface((10,10))
apple.fill(WHITE)

# Set the initial direction of the snake
direction = "up"
learning_rate = 0.01
input_size = 3
hidden_size = 1
output_size = 1

# Set up the neural network
def initialize_network():
  # Create a neural network with a few hidden layers
  network = torch.nn.Sequential(
      torch.nn.Linear(input_size, hidden_size),
      torch.nn.ReLU(),
      torch.nn.Linear(hidden_size, hidden_size),
      torch.nn.ReLU(),
      torch.nn.Linear(hidden_size, output_size)
  )
  return network

# Set up the optimizer
def initialize_optimizer(network):
  # Create an optimizer for the network
  optimizer = torch.optim.Adam(network.parameters(), lr=learning_rate)
  return optimizer

# Set up the loss function
def initialize_loss_function():
  # Create a loss function
  loss_fn = torch.nn.MSELoss()
  return loss_fn

# Get the current state of the game
def get_game_state(snake, apple):
  # Flatten the snake positions into a single list
  snake_positions = [pos for sublist in snake for pos in sublist]
  print(snake_positions)

  # Concatenate the snake positions and apple position into a single list
  state = snake_positions + list(apple)
  if direction == "up":
    state = snake_positions + list(apple) + [0]
  elif direction == "down":
    state = snake_positions + list(apple) + [1]
  elif direction == "left":
    state = snake_positions + list(apple) + [2]
  elif direction == "right":
    state = snake_positions + list(apple) + [3]


  print(state)

  return state

# Predict the action to take using the neural network
def predict_action(network, state):
  state = torch.tensor(state, dtype=torch.float32)

  # Use the network to predict the action to take given the current state
  action_probs = network(state)

  # Convert the output to a probability distribution
  action_probs = torch.nn.functional.softmax(action_probs, dim=0)

  # Sample from the probability distribution to choose the action
  action = torch.multinomial(action_probs, 1)

  print(action)

  return action

# Take the action and get the new state, reward, and whether the game is over
def take_action(snake, apple, action):
  # Update the snake based on the action
  if action == 0:
    # Move up
    direction = "up"
    snake[0] = (snake[0][0], snake[0][1] - 10)
  elif action == 1:
    # Move down
    direction = "down"
    snake[0] = (snake[0][0], snake[0][1] + 10)
  elif action == 2:
    # Move left
    direction = "left"
    snake[0] = (snake[0][0] - 10, snake[0][1])
  elif action == 3:
    # Move right
    direction = "right"
    snake[0] = (snake[0][0] + 10, snake[0][1])

  # Update the rest of the snake
  for i in range(1, len(snake)):
    snake[i] = (snake[i-1][0], snake[i-1][1])

  # Check if the snake has collided with the edge of the screen
  if snake[0][0] < 0 or snake[0][0] >= window_size[0] or snake[0][1] < 0 or snake[0][1] >= window_size[1]:
    # Snake has collided with the edge of the screen
    return ((snake, apple), -1, True)

  # Check if the snake has collided with itself
  if snake[0] in snake[1:]:
    # Snake has collided with itself
    return ((snake, apple), -1, True)

  # Check if the snake has eaten the apple
  if snake[0] == apple:
    # Snake has eaten the apple
    apple = (random.randint(0,59)*10,random.randint(0,59)*10)
    snake.append((0,0))
    return ((snake, apple), 1, False)

  # Snake has not collided with anything
  return ((snake, apple), 0, False)


# Set up the neural network
network = initialize_network()

# Set up the optimizer
optimizer = initialize_optimizer(network)

# Set up the loss function
loss_fn = initialize_loss_function()

# Run the game loop
while True:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # Get the current state of the game
  state = get_game_state(snake, apple_pos)

  # Predict the action to take using the neural network
  action = predict_action(network, state)

  # Take the action and get the new state, reward, and whether the game is over
  new_state, reward, done = take_action(snake, apple, action)

  # Compute the loss
  loss = loss_fn(reward, 0)

  # Zero the gradients
  optimizer.zero_grad()

  # Backpropagate the loss and update the weights
  loss.backward()
  optimizer.step()

  # If the game is over, reset the game
  if done:
    snake = [(200, 200), (210, 200), (220,200)]
    direction = "up"
    apple_pos = (random.randint(0,59)*10,random.randint(0,59)*10)
    score = 0
   
  # Update the screen
  screen.fill(BLACK)
  screen.blit(apple, apple_pos)
  for pos in snake:
    screen.blit(snake_skin,pos)
  pygame.display.update()
  clock.tick(5)
