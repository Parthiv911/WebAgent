from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
import pandas as pd
import cv2
import numpy as np
import torch
from utility import find_string_between

class Agent:
    def __init__(self,driver):
        self.driver=driver
        pass

    def click(self):
        ActionChains(self.driver).click().perform()
        print("clicking")
        time.sleep(2)

    def move_cursor_to_element(self,element):
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(2)

    def move_cursor(self,x,y):
        ActionChains(self.driver).move_by_offset(x, y).perform()
        time.sleep(2)
        print("Moved cursor to: ",x,",",y)

    def perceive_vision(self):
        self.driver.save_screenshot('screenie.png')
        image=cv2.imread('screenie.png')
        return image

    def get_cursor_coordinate(self):
        cursor=self.driver.find_element(By.ID, "selenium_mouse_follower")
        css_style=cursor.get_attribute("style")
        cood_x=find_string_between(css_style,"left: ","px")
        cood_y=find_string_between(css_style,"top: ","px")
        return int(cood_x),int(cood_y)
    
    def get_interactables(self):
        interactables=["button","a","textarea"]

        interactables_dict={}
        for interactable in interactables:
            elements=self.driver.find_elements(By.TAG_NAME, interactable)
            interactables_dict[interactable]=elements

        return interactables_dict
