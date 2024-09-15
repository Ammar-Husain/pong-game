from screeninfo import get_monitors, common

def get_screen_dimensions():
  
  try:
    from dimensions import screen_width, screen_height
  except ModuleNotFoundError: # No stored dimensions data:
      pass
  else:
    print(f"Stored resolution value ({screen_width}x{screen_height}) has been used!")
    print("To delete the stored value delete the file\"dimensions.py\"")
    return screen_width, screen_height
    
  try:
    monitor = get_monitors()[0]
    return monitor.width, monitor.height
  
  except common.ScreenInfoError: # the game is running in an android device
    pass
  
  print("Because you are using a stupid android phone I need you to manually enter your screen width and height, you can get it from your device setting")
  
  while True:
    try:
      screen_width = int(input("Width:\n"))
      screen_height = int(input("Height:\n"))
      store = input("Do you want me to store the width and height values ?\nEnter Y or y for yes any other thing for no\n To delete them you will need to manually delete dimensions.py\n")
      
      if store == "Y" or store == "y":
        f = open("dimensions.py", "w")
        f.write(f"screen_width = {screen_width}\nscreen_height = {screen_height}")
        f.close()
      
      return screen_width, screen_height
    except ValueError:
      print("Enter a number stupid!!!, now we have to start again")