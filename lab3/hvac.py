"""
CSCI4900/5900: Lab 3

This program simulates a very basic HVAC system that implements limited
requirements monitoring.  The intention will be to extend this (or use it
as a basis) for more...adaptive work.
"""
import os, random, time, copy
import argparse

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

  for timestep in xrange(args.timesteps):
    curr_temp     = getTemperature(curr_temp)
    curr_humidity = getHumidity(curr_humidity)

    print "T [%f] H [%f] F [%s] AC [%s] H [%s]" % (curr_temp, curr_humidity, state['furnace'], state['AC'], state['humidifier'])

    curr_temp, curr_humidity, state = adjustSystem(curr_temp, curr_humidity, state)

    utils = monitorRequirements(curr_temp, curr_humidity, state)

    print utils
    print ""

    history[timestep] = {'temperature': curr_temp,           \
                         'humidity'   : curr_humidity,       \
                         'furnace'    : state['furnace'],    \
                         'AC'         : state['AC'],         \
                         'humidifier' : state['humidifier'], \
                         'utils'      : copy.deepcopy(utils)}
                

    time.sleep(0.5)

with open('HVAC_history.txt','w') as f:
  f.write('timestep  temperature  humidity  sFurnace  sAC  sHumidifier req\n')
  for timestep in xrange(args.timesteps):
    f.write('%d, %f, %f, %s, %s, %s, %s\n' % (timestep, \
                                                    history[timestep]['temperature'], \
                                                    history[timestep]['humidity'], \
                                                    history[timestep]['furnace'], \
                                                    history[timestep]['AC'], \
                                                    history[timestep]['humidifier'], \
                                                    history[timestep]['utils']))