## Introduction
This is a 2 players (currently) pong game over local wifi connection.

The first player (i.e the host) must enable the wifi hotspot on his device, inside the game he will be referred to as Player1 and the game server will run on his device.

The second player (i.e the guest) must connect to the host Hotspot, inside the game he will be referred to as Player2.

## How to get started
- Install python if it is not already installed in your device.
visit python [download page](https://www.python.org/downloads/) from python official website, choose your operating system and download the latest stable version.

  If you are in android and use termux run the following command in the terminal:
  ```
  pkg i python
  ```

- Install git if it is not already installed in your device, check git [download page](https://git-scm.com/downloads) for installation instructions.


- Clone this repository by running this code in your terminal:
`git clone https://github.com/Ammar-Husain/pong-game.git`

- Once the repo has been cloned, move to game directory and install the required dependencies by running:
`pip install -r requirements.txt`

#### Note:
if you are in android and termux, pygame library will fail to install directly, check my tutorial [here](https://dev.to/ammar-hussein/setup-pygame-in-termux-g9b) about how to get it downloaded.

-once the dependencies have been installed succefully start the game by running:
`python play.py`