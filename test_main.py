"""
This module contains shared fixtures for web UI tests.
"""

import json
import pytest
import time
import selenium

from selenium.webdriver import Chrome, Firefox
from selenium import webdriver


CONFIG_PATH = 'config.json'
DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ['chrome', 'firefox']


@pytest.fixture(scope='session')
def config():
  # Read the JSON config file and returns it as a parsed dict
  with open(CONFIG_PATH) as config_file:
    data = json.load(config_file)
  return data

#print(data)

@pytest.fixture(scope='session')
def config_browser(config):
  # Validate and return the browser choice from the config data
  if 'browser' not in config:
    raise Exception('The config file does not contain "browser"')
  elif config['browser'] not in SUPPORTED_BROWSERS:
    raise Exception(f'"{config["browser"]}" is not a supported browser')
  return config['browser']


@pytest.fixture(scope='session')
def config_wait_time(config):
  # Validate and return the wait time from the config data
  return config['wait_time'] if 'wait_time' in config else DEFAULT_WAIT_TIME


@pytest.fixture
def browser(config_browser, config_wait_time):
  # Initialize WebDriver
  global driver
  if config_browser == 'chrome':
    driver = webdriver.Chrome()
  elif config_browser == 'firefox':
    driver = webdriver.Firefox()
  else:
    raise Exception(f'"{config_browser}" is not a supported browser')

  # Wait implicitly for elements to be ready before attempting interactions
  driver.implicitly_wait(config_wait_time)
  
  # Return the driver object at the end of setup
  yield driver
  
  # For cleanup, quit the driver
  driver.quit()

def test_open_google(browser):
    driver.get('http://192.168.56.101/opencart/')
    assert driver.title == 'Your Store', 'Title of website not Your Store'