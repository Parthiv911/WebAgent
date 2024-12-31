import subprocess
import matplotlib.pyplot as plt
import re

def extract_bbox_coods(bbox_string):
    return [(int(bbox_string.split()[1]),int(bbox_string.split()[2])),(int(bbox_string.split()[3]),int(bbox_string.split()[4]))]

def find_string_between(string, start_str, end_str):
  """
  Finds the substring between two given strings in a string.

  Args:
    string: The input string.
    start_str: The starting string.
    end_str: The ending string.

  Returns:
    The substring between start_str and end_str, or None if not found.
  """
  try:
    start_index = string.index(start_str) + len(start_str)
    end_index = string.index(end_str, start_index)
    return string[start_index:end_index]
  except ValueError:
    return None



def matplotlibplot(image):
   plt.imshow(image)
   plt.show()

def run_tesseract_ocr(image_path, output_path):
  """
  Runs the Tesseract OCR command to extract text from an image.

  Args:
    image_path: Path to the image file.
    output_path: Path to the output file (e.g., "output.txt").

  Returns:
    True if the command executed successfully, False otherwise.
  """
  try:
    command = [
        "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        image_path,
        output_path,
        "hocr" 
    ]
    subprocess.run(command, check=True)
    return True
  except subprocess.CalledProcessError as e:
    print(f"Error executing Tesseract OCR: {e}")
    return False

def hocr_to_dataframe(fp):

    from lxml import etree
    import pandas as pd
    import os

    doc = etree.parse(fp)
    words = []
    wordConf = []
    bboxes=[]
    for path in doc.xpath('//*'):
        
        if 'ocrx_word' in path.values():
            #print("path values",path.values())
            conf = [x for x in path.values() if 'x_wconf' in x][0]
            bbox= [x for x in path.values() if 'bbox' in x][0]
            #print("conf",conf)
            #print("bbox",bbox.split(';')[0])
            wordConf.append(int(conf.split('x_wconf ')[1]))
            bboxes.append(bbox.split(';')[0])
            words.append(path.text)

    dfReturn = pd.DataFrame({'word' : words, 'bbox': bboxes,'confidence' : wordConf})
    return(dfReturn)

# python
enable_cursor = """
        function enableCursor() {
          var seleniumFollowerImg = document.createElement("img");
          seleniumFollowerImg.setAttribute('src', 'data:image/png;base64,'
            + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
            + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
            + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
            + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
            + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
            + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
            + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
            + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
            + 'dAAAAABJRU5ErkJggg==');
          seleniumFollowerImg.setAttribute('id', 'selenium_mouse_follower');
          seleniumFollowerImg.setAttribute('style', 'position: absolute; z-index: 99999999999; pointer-events: none; left:0; top:0');
          document.body.appendChild(seleniumFollowerImg);
          document.onmousemove = function (e) {
            document.getElementById("selenium_mouse_follower").style.left = e.pageX + 'px';
            document.getElementById("selenium_mouse_follower").style.top = e.pageY + 'px';
          };
        };

        enableCursor();
"""

import pyautogui

def move_mouse_to_coordinates(x, y, duration=0.5):
  """
  Moves the mouse cursor to the specified coordinates.

  Args:
    x: The x-coordinate.
    y: The y-coordinate.
    duration: The time in seconds for the mouse to move to the coordinates. 
              Defaults to 0.5 seconds.
  """
  pyautogui.moveTo(x, y, duration=duration)
