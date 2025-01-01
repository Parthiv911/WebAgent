from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
import pandas as pd
import cv2
import numpy as np
import torch
from utility import enable_cursor,are_images_same,find_string_between, run_tesseract_ocr, hocr_to_dataframe, extract_bbox_coods, bbox_coods_to_HTML_coods, excel_to_dict, dict_to_excel

class Agent:
    def __init__(self,driver,inventory):
        self.driver=driver
        self.cursor_location_selenium=(0,0)
        #self.transition_function={(" ",True):[(self.perceive_vision.__name__,1)],
        #                        (self.perceive_vision.__name__,True):[(self.move_focus_to_next_object.__name__,1)]}
        #dict_to_excel(self.transition_function)
        self.transition_function=excel_to_dict()
        self.inventory=inventory
        self.objects=None
        self.objects_index=-1
        self.previous_function=" "
        self.previous_function_return_val=True

        self.functions_list=["perceive_vision","move_focus_to_next_object","move_cursor_to_focussed_object","is_inventory_equals_object_text",
                             "move_cursor_to_search_bar","click","is_change_in_screenshot"]
    
    def is_change_in_screenshot(self):
        image1=cv2.imread(r"C:\Users\USER\Desktop\WebAgent\screenie.png")
        self.driver.save_screenshot('compare_screenie.png')
        image2=cv2.imread('compare_screenie.png')
        
        return  (not are_images_same(image1,image2))
    
    def move_focus_to_next_object(self):
        self.objects_index=self.objects_index+1
        return True

    def move_cursor_to_focussed_object(self):
        top,bottom=extract_bbox_coods(self.objects["bbox"].loc[self.objects_index])
        centre=((top[0]+bottom[0])/2,(top[1]+bottom[1])/2)
        self.move_cursor(bbox_coods_to_HTML_coods(centre))
        return True
    
    def is_inventory_equals_object_text(self):
        print("Inventory: ", self.inventory)
        print("Objects text: ",self.objects.loc[self.objects_index]["word"])
        return (self.inventory==self.objects.loc[self.objects_index]["word"])

    def move_cursor_to_search_bar(self):
        self.move_cursor((738,259))
        return True
    
    def click(self):
        ActionChains(self.driver).click().perform()
        print("clicking")
        time.sleep(2)
        return True
    
    def do_next_action(self):
        #next_action=max(self.action_rewards, key=self.action_rewards.get)
        possible_next_actions=self.transition_function.get((self.previous_function,self.previous_function_return_val),[])

        chosen_next_function=None
        max_reward=0
        forbidden_next_functions=[]
        for next_function, reward in possible_next_actions:
            if reward<0:
                forbidden_next_functions.append(next_function)
            if reward>max_reward:
                max_reward=reward
                chosen_next_function=next_function
        
        if chosen_next_function==None:
            for next_function in self.functions_list:
                if(next_function not in forbidden_next_functions):
                    chosen_next_function=next_function
                    break
            print("Chosen next function: ", chosen_next_function)
            if (self.previous_function,self.previous_function_return_val) not in self.transition_function:
                self.transition_function[(self.previous_function,self.previous_function_return_val)]=[]
            user_inputed_reward=input("Enter Reward for chosen function: ")
            user_inputed_reward=int(user_inputed_reward)
            self.transition_function[(self.previous_function,self.previous_function_return_val)].append((chosen_next_function,user_inputed_reward))
            dict_to_excel(self.transition_function)

            if user_inputed_reward<0:
                print("Not executing it")
                return
        else:
            print("Chosen next function: ", chosen_next_function)
        # self.driver.save_screenshot("new_screenie.png")
        # if are_images_same(cv2.imread("new_screenie.png"),cv2.imread("screenie.png")):


        self.previous_function_return_val=getattr(self,chosen_next_function)()
        self.previous_function=chosen_next_function
    
    def reset_cursor_location_selenium(self):
        self.move_cursor((-self.cursor_location_selenium[0],-self.cursor_location_selenium[1]))
        self.cursor_location_selenium=(0,0)

    def move_cursor_to_element(self,element):
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(2)

    def move_cursor(self,coods):
        ActionChains(self.driver).move_by_offset(-int(self.cursor_location_selenium[0]), -int(self.cursor_location_selenium[1])).perform()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(int(coods[0]), int(coods[1])).perform()
        time.sleep(2)
        print("Moved cursor by offset: ",coods[0],",",coods[1])
        self.cursor_location_selenium=coods

    def screenshot(self):
        self.driver.save_screenshot('screenie.png')
        image=cv2.imread('screenie.png')
        return image

    def perceive_vision(self):
        image=self.screenshot()
        run_tesseract_ocr("screenie.png", "output")
        self.objects=hocr_to_dataframe(r"C:\Users\USER\Desktop\WebAgent\output.hocr")
        self.objects_index=-1
        self.driver.execute_script(enable_cursor)
        return True
    
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
