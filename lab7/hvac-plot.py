"""
CSI4900/5900: Lab 7

This program simulates a very basic HVAC system that implements limited
requirements monitoring.  The intention will be to extend this (or use it
as a basis) for more...adaptive work.
"""
import os, random, time, copy
import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')  # necessary since we're headless
import matplotlib.pyplot as plt

# Accept command line arguments
parser = argparse.ArgumentParser(description='Lab 2')
parser.add_argument('--curr_temp', type=float, default=70.0)
parser.add_argument('--curr_humidity', type=float, default=30.0)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--timesteps', type=int, default=300)

# Add some fuzz to the temperature sensor
def getTemperature(temp):
  fuzz = random.uniform(-1.0, 1.0)
  return temp + fuzz

# Add some fuzz to the humidity sensor
def getHumidity(humidity):
  fuzz = random.uniform(-1.0, 1.0)
  return humidity + fuzz

# Perform requirements monitoring, returning a dictionary of the 
# calculated values
def monitorRequirements(temp, humidity, state):
  utils = {}
  
  # R1
  if ((temp >= 66.0) and (temp <= 74.0)):
    utils['R1'] = 1.0
  else:
    utils['R1'] = 0.0

  # R2
  if ((temp <= 70.0) and (state['furnace'] == True)):
    utils['R2'] = 1.0
  elif ((temp <= 70.0) and (state['furnace'] == False)):
    utils['R2'] = 0.0

  # R3
  if ((temp >= 72.0) and (state['AC'] == True)):
    utils['R3'] = 1.0
  elif ((temp >= 72.0) and (state['AC'] == False)):
    utils['R3'] = 0.0

  # R4
  if ((humidity >= 30.0) and (humidity <= 50.0)):
    utils['R4'] = 1.0
  else:
    utils['R4'] = 0.0

  # R5
  if ((humidity <= 40.0) and (state['humidifier'] == True)):
    utils['R5'] = 1.0
  elif ((humidity <= 40.0) and (state['humidifier'] == False)):
    utils['R5'] = 0.0

  # R6
  if ((humidity >= 42.0) and (state['AC'] == True)):
    utils['R6'] = 1.0
  elif ((humidity >= 42.0) and (state['AC'] == False)):
    utils['R6'] = 0.0

  return utils

# Control the HVAC system based on monitored temperature
# and humidity.  
def adjustSystem(temp, humidity, state):
  if temp <= 70.0:
    state['furnace'] = True
  else:
    state['furnace'] = False

  if temp >= 72.0 or humidity >= 42.0:
    state['AC'] = True
  else:
    state['AC'] = False

  if humidity <= 40.0:
    state['humidifier'] = True
  else:
    state['humidifier'] = False

  # Random chance that something broke
  if (random.random() < 0.1):
    state['furnace'] = not state['furnace']
  if (random.random() < 0.1):
    state['AC'] = not state['AC']
  if (random.random() < 0.1):
    state['humidifier'] = not state['humidifier']

  # Adjust temp/humidity as necessary
  if state['AC'] == True:
    humidity -= 1.0
    temp     -= 1.0

  if state['furnace'] == True:
    temp += 1.0

  if state['humidifier'] == True:
    humidity += 1.0

  return temp, humidity, state
  
# Plot out each requirement in its own plot over time
def graph_requirements(history, timesteps):
  # xvalues -- timesteps
  xvals = np.arange(timesteps)

  # Transform history into graphable format (probably a more Pythonic way of doing this)
  # Normally I'd use a list here for ease of use, but since we have missing data points
  # we can use Numpy to mask them (literally)
  yvals = {}
  reqs  = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
  for req in reqs:
    yvals[req] = np.arange(timesteps).astype(np.double)

  for timestep in range(timesteps):
    for req in reqs:
      if req in history[timestep]['utils'].keys():
        yvals[req][timestep] = history[timestep]['utils'][req]
      else:
        yvals[req][timestep] = None

  # Mask off the 'None' values
  yval_masks = {}
  for req in reqs:
    yval_masks[req] = np.isfinite(yvals[req])

  # Now plot
  plt.figure() 
  for req in reqs:
    plt.plot(xvals, yval_masks[req], linestyle='-', marker='o', label=req)
  plt.legend()
  plt.savefig('plots/hvac-all-requirements.png')

  # And plot each seperately
  for req in reqs:
    plt.figure() 
    plt.plot(xvals, yval_masks[req], linestyle='-', marker='o', label=req)
    plt.legend()
    plt.savefig('plots/hvac-requirement-%s.png' % req)
  return
  

# Main function
if __name__ == "__main__":
  args = parser.parse_args()
  history = {}

  # Make this repeatable
  random.seed(args.seed) 

  # Initialize all relevant values
  curr_temp     = args.curr_temp
  curr_humidity = args.curr_humidity

  state = {}
  state['furnace']    = False
  state['AC']         = False
  state['humidifier'] = False

  for timestep in range(args.timesteps):
    curr_temp     = getTemperature(curr_temp)
    curr_humidity = getHumidity(curr_humidity)

    print("T [%f] H [%f] F [%s] AC [%s] H [%s]" % (curr_temp, curr_humidity, state['furnace'], state['AC'], state['humidifier']))

    curr_temp, curr_humidity, state = adjustSystem(curr_temp, curr_humidity, state)

    utils = monitorRequirements(curr_temp, curr_humidity, state)

    print(utils)
    print("")

    history[timestep] = {'temperature': curr_temp,           \
                         'humidity'   : curr_humidity,       \
                         'furnace'    : state['furnace'],    \
                         'AC'         : state['AC'],         \
                         'humidifier' : state['humidifier'], \
                         'utils'      : copy.deepcopy(utils)}
                

    #time.sleep(0.5)

with open('HVAC_history.txt','w') as f:
  f.write('timestep  temperature  humidity  sFurnace  sAC  sHumidifier req\n')
  for timestep in range(args.timesteps):
    f.write('%d, %f, %f, %s, %s, %s, %s\n' % (timestep, \
                                                    history[timestep]['temperature'], \
                                                    history[timestep]['humidity'], \
                                                    history[timestep]['furnace'], \
                                                    history[timestep]['AC'], \
                                                    history[timestep]['humidifier'], \
                                                    history[timestep]['utils']))

# Plot out requirements as well
graph_requirements(history,args.timesteps)
