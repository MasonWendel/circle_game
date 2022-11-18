# Importing arcade module
import arcade
import arcade.gui as gui
import random
import math
import json
import requests
BIN_ID = '6373b45a0e6a79321e4a8ca7'
url = 'https://api.jsonbin.io/v3/b/'+BIN_ID+'/latest'
headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': '<$2b$10$Udpb3TQGuNBmgDV5RhP6.OKFval0Tr1619w4FkzTaaUtWAk6Kcc5S>'
}
try:
   req = requests.get(url, json=None, headers=headers).json()['record']
   with open("high_scores.json", 'w') as f:
        json.dump(req, f)
except requests.exceptions.ConnectionError:
    req = {"1st": ["No Connection"]}


# Size of the rectangle
RECT_WIDTH = 50
RECT_HEIGHT = 50
PLAYER_MOVEMENT_SPEED = 5
IS_CONNECTED = not(req["1st"][0] == "No Connection")
min_circle_size = 5
colors = [arcade.color.GREEN,
          arcade.color.RED,
          arcade.color.BLUE,
          arcade.color.PURPLE,
          arcade.color.YELLOW,
    ]
# Creating MainGame class
def update_server(data):
    url = 'https://api.jsonbin.io/v3/b/'+BIN_ID
    headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': '$2b$10$Udpb3TQGuNBmgDV5RhP6.OKFval0Tr1619w4FkzTaaUtWAk6Kcc5S'
    }
    req = requests.put(url, json=data, headers=headers)
    print(req.text)

def get_scores(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)
def change_score(file_name, key, value):
    file = get_scores(file_name)
    file[key] = value
    with open(file_name, 'w') as f:
        json.dump(file, f)
def angleTo(x1,y1,x2,y2):
    
    a = x1-x2
    
    o = y1-y2
    
    if (o == 0):
        return None
    else:
        side = ((o)/abs(o))
        
        
        # 
        return (180 - (180*side)+(math.degrees(math.atan2(o,a))));


def getPointInDir(ox,oy,angle,distance):
    angle *= -1
    angle = angle + 90
    x = distance*math.cos(math.radians(angle)) + ox
    y = distance*math.sin(math.radians(angle)) + oy
    return x,y

def hits(cir1, cir2):
    x1 = cir1["posX"]
    y1 = cir1["posY"]
    x2 = cir2["posX"]
    y2 = cir2["posY"]
    distance = distanceTo(x1,y1,x2,y2)
    if distance <= cir1["radius"] + cir2["radius"]:
        return True
    return False 

def distanceTo(x1,y1,x2,y2):
    return abs(math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2)))

def customRand(low,high,excluding = [],increment = 1):
    possible_values = []
    for i in range(low,high,increment):
        if i not in excluding:
            possible_values.append(i)
    return random.choice(possible_values)

class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(1000, 1000,
                         title="Circle Game", resizable=True)
        # Example of circle object: {"velocityX": 1,"velocityY": 1, "posX": 200, "posY": 200, "radius": 20, "color":arcade.color.GREEN }
        self.circles = []
        self.manager = gui.UIManager()
        self.manager.enable()
        # Getting scores
        self.high_scores = get_scores('high_scores.json')
        self.high_scores_list = []
        

        # the velocity of the player
        self.vel_x = 0
        self.TIMER = 0
        self.PLAYER_SIZE = 0
        self.name = "Bob"
        
        # Creating variable for Camera
        self.camera = None
        self.GAME_GO = False
        self.game_has_begun = False
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Creating variable to store current score
        self.score = 0
        self.scores_label = ""
        self.score_label_x = 0
    
  
        # Creating variable to store player sprite
        self.player = {"velocityX": 0,"velocityY": 0, "posX": 500, "posY": 500, "radius": 20, "color":arcade.color.WHITE }
        self.center_x = 50
        self.center_y = 50
        
        self.start_btn = {"centerX":500,"centerY":360,"width":150, "height": 70, "color": arcade.color.RED}
        
        
        
        # Creating objects for the title screen
        self.start_label= arcade.Text(
            "Start",
            445, 350,
            arcade.color.WHITE,
            30,
            font_name="Kenney Mini Square",   
        )
        self.lost_label= arcade.Text(
            "You're Trash!",
            60, 500,
            arcade.color.RED,
            100,
            font_name="Kenney Mini Square"
        )
        
        
        self.display_input_gui = True
        
        # Create a text label
        self.label = arcade.gui.UILabel(
            text="Enter name:",
            text_color=arcade.color.DARK_RED,
            width=350,
            height=40,
            font_size=24,
            font_name="Kenney Future")

        # Create an text input field
        self.input_field = gui.UIInputText(
          x = 600,
          text_color=arcade.color.DARK_RED,
          font_size=24,
          width=460,
          text='Replace me and put name here')

        # Create a button
        submit_button = gui.UIFlatButton(x=50,y=200,
          color=arcade.color.DARK_BLUE_GRAY,
          text='Submit')
        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        submit_button.on_click = self.on_click 
        
        self.v_box = gui.UIBoxLayout()
        self.v_box.add(self.label.with_space_around(bottom=0))
        self.v_box.add(self.input_field)
        self.v_box.add(submit_button)
        
        
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.v_box)
        )
       
  
    # Creating on_draw() function to draw on the screen
    def update_scores_list(self):
        hasScore = False
        SCORE = None
        for score in self.high_scores_list:
            if score[2] == True:
                hasScore = True
                SCORE = score
                break
        if hasScore:
            for i in range(0, len(self.high_scores_list)):
                if self.score > self.high_scores_list[i][1]:
                    replace = self.high_scores_list.pop(self.high_scores_list.index(SCORE))
                    replace[1] = self.score
                    self.high_scores_list.insert(i,replace)
                    break
        else:
            for i in range(0, len(self.high_scores_list)):
                if self.score >= self.high_scores_list[i][1]:
                    self.high_scores_list.insert(i,[self.name,self.score,True])
                    self.high_scores_list.pop(-1)
                    break
            
                
                
    
    def update_scores_label(self):
        self.scores_label = ''
        for key in self.high_scores:
            if not IS_CONNECTED:
                self.scores_label = "No Internet Connection"
            elif self.high_scores[key][1] == 0:
                self.scores_label += key + ",  " + "No score yet\n\n" 
            else:
                self.scores_label += key + ",  " + self.high_scores[key][0] + ": " + str(self.high_scores[key][1]) + "\n\n"
                
    
    def update_high_scores(self):
        if IS_CONNECTED:
            self.update_scores_list()
            for key in self.high_scores:
                self.high_scores[key][1] = self.high_scores_list[int(key[0:1])-1][1]
                self.high_scores[key][0] = self.high_scores_list[int(key[0:1])-1][0]
                self.update_scores_label()
                change_score('high_scores.json',key,self.high_scores[key])            
                
        self.update_scores_label()
    def draw_scores_label(self):
        arcade.draw_text(self.scores_label,25,975.0,
                         arcade.color.WHITE,10,120,'left',multiline=True)
                
    def draw_title_screen(self):
        arcade.draw_rectangle_filled(self.start_btn["centerX"],self.start_btn["centerY"],self.start_btn["width"],
                              self.start_btn["height"],self.start_btn["color"])
        self.start_label.draw()
        
    def draw_end_screen(self):
        self.lost_label.draw()
        
    def hit_btn(self,btn,mx,my):
        x = btn["centerX"] 
        y = btn["centerY"] 
        width = btn["width"]
        height = btn["height"]
        if abs(x-mx) < width and abs(y-my) < height:
            return True
        return False
    
    def on_draw(self):
        # clears the window
        arcade.start_render()

        to_be_removed = []
        # Draws updated circles. Removes if out of bounds. 
        for circle in self.circles:
            
            if circle["posX"]-circle["radius"] > 1300 or circle["posY"]-circle["radius"] > 1300 or circle["posX"]+circle["radius"] < -300 or circle["posY"]+circle["radius"] < -300 :
                to_be_removed.append(circle)
                
            else: 
                arcade.draw_circle_filled(circle["posX"], circle["posY"], circle["radius"],circle["color"])
                # Checks if a circle hits player
            if hits(self.player,circle):
                if circle["radius"] < self.player["radius"]:
                    self.PLAYER_SIZE += circle["radius"]
                    self.player["radius"] += math.log(self.PLAYER_SIZE,15)*0.5
                    self.score += self.PLAYER_SIZE
                    self.update_high_scores()
                    to_be_removed.append(circle)
                    
                    
                else:
                    self.GAME_GO = False 
                 
        for circle in to_be_removed:
            self.circles.remove(circle)
        # Drawing the text
        
        # Draws the player
        if self.display_input_gui == False:
            arcade.draw_circle_filled(self.player["posX"], self.player["posY"], self.player["radius"],self.player["color"])
            arcade.draw_text('Score: '+str(self.score),800.0,900.0,
                         arcade.color.WHITE,30,180,'right')
        # Using the camera
        #self.camera.use()
        # Drawing the title screen
        if self.GAME_GO == False and self.game_has_begun == False and self.display_input_gui == False:
            self.draw_title_screen()
        if self.GAME_GO == False and self.game_has_begun == True:
            self.draw_end_screen()
        
        if self.display_input_gui:
            self.manager.draw()
        self.draw_scores_label()
    def setup(self):
        if IS_CONNECTED:
            for key in self.high_scores:
                name = self.high_scores[key][0]
                score = self.high_scores[key][1]
                self.high_scores_list.append([name,score,False])
        
   
      
    # Creating on_update function to
    # update the x coordinate
    def on_update(self, delta_time):
        
        
        if self.GAME_GO:
            # updating circle position
            for circle in self.circles:
                circle["posX"] += circle["velocityX"]
                circle["posY"] += circle["velocityY"]
            
    
            self.TIMER += 1
            if self.TIMER % 5 == 0:
                angle = customRand(0,361)
                
                x,y  = getPointInDir(500,500,angle,750)
                newCircle = {"velocityX": customRand(-5,5,excluding = [0]),"velocityY": customRand(-5,5,[0]),
                             "posX": x, "posY": y, "radius": customRand(min_circle_size,100), "color": random.choice(colors)}
                self.circles.append(newCircle)
            if self.TIMER/50000 == 0:
                self.TIMER = 0
                
            # Alters the player position 
            self.player["posX"] += self.player["velocityX"]
            self.player["posY"] += self.player["velocityY"]
    # Gets and records mouse psoition
    def on_mouse_motion(self, x, y, dx, dy):
            """
            Called whenever the mouse moves.
            """
            self.mouse_x = x
            self.mouse_y = y
            
    def on_mouse_press(self, x, y, button, modifiers):
        if self.hit_btn(self.start_btn,x,y) and self.game_has_begun == False:
            self.GAME_GO = True
            self.game_has_begun = True
            
    def update_text(self):
        if self.display_input_gui:
            print(f"updating the label with input text '{self.input_field.text}'")
            if self.input_field.text == "Replace me and put name here":
                self.name = "No name"
            else:
                self.name = self.input_field.text.strip().capitalize()   

    def on_click(self, event):
        if self.display_input_gui:
            print(f"click-event caught: {event}")
            self.update_text()
            self.update_high_scores()
            self.display_input_gui = False
            
    
    
    
    def on_key_press(self, key, modifier):
        """Called whenever a key is pressed."""
        if self.GAME_GO:
            if key == arcade.key.UP or key == arcade.key.W:
                self.player["velocityY"] = PLAYER_MOVEMENT_SPEED
            if key == arcade.key.DOWN or key == arcade.key.S:
                self.player["velocityY"] = -PLAYER_MOVEMENT_SPEED
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.player["velocityX"] = -PLAYER_MOVEMENT_SPEED
            if key == arcade.key.RIGHT or key == arcade.key.D:
                self.player["velocityX"] = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.R and self.GAME_GO == False:
            print("works")
            self.GAME_GO = False
            self.game_has_begun = False
            self.player['posX'] = 500
            self.player['posY'] = 500
            self.player['velocityX'] = 0
            self.player['velocityY'] = 0
            self.player['radius'] = 20
            self.score = 0
            self.PLAYER_SIZE = 0
            
            self.circles.clear()
                
  
    def on_key_release(self, key, modifier):
        
        """ called when a key is released """
        if self.GAME_GO:
            if key == arcade.key.UP or key == arcade.key.W:
                self.player["velocityY"] = 0
            if key == arcade.key.DOWN or key == arcade.key.S:
                self.player["velocityY"] = 0
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.player["velocityX"] = 0
            if key == arcade.key.RIGHT or key == arcade.key.D:
                self.player["velocityX"] = 0
                
        

  
# Calling MainGame class

game = MainGame()
game.setup()
arcade.run()
if IS_CONNECTED:
    print("works")
    update_server(get_scores('high_scores.json'))
