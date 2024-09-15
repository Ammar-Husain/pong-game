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
  
  except common.ScreenInfoError: # the game is propaply running in an android device
    pass
  
  print("\n\n\nIt seems like you are propaply running the game in an android phone because we were not able to detect your screen resolution informations, So we need you to manually enter your screen resolution values (width and height in pixels), you can get it from your device setting")
  
  while True:
    try:
      screen_width = int(input("Width:\n"))
      break
    except ValueError:
      print("Width must be a number, Try again.")
  
  while True:
    try:
      screen_height = int(input("Height:\n"))
      break
    except ValueError:
      print("height must be a number, Try again.")
            
  store = input("Do you want us to store your screen resolutions values ?\nEnter Y or y for \"Yes\" any other thing for \"No\"\nTo delete them you will need to manually delete dimensions.py file in the working directory\n")
  
  if store == "Y" or store == "y":
    f = open("dimensions.py", "w")
    f.write(f"screen_width = {screen_width}\nscreen_height = {screen_height}")
    f.close()
  
  return screen_width, screen_height