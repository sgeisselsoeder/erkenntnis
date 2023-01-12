import arcade

import time
from erkenntnis.world import World
from erkenntnis.utils import random_position
from erkenntnis.things_available import *
from erkenntnis.agents_available import *

image_scaling = 0.25

screen_width = 1000
screen_height = 1000
screen_title = "ERKENNTNIS"

initial_world_scale = 100
map_boundary = 1.6 * initial_world_scale
map_resolution = 80


class Thing(arcade.Sprite):
    def __init__(self, agent, image):
        super().__init__(image, image_scaling);
        self.agent = agent;
    
    def update(self):
        self.center_x  = self.agent.position[0]*screen_width/initial_world_scale  + screen_width / 2;
        self.center_y  = self.agent.position[1]*screen_height/initial_world_scale + screen_height / 2;

class Sheep(Thing):
    def __init__(self, agent):
        super().__init__(agent, "visualizer/sheep.png");
        

class Wolf(Thing):
    def __init__(self, agent):
        super().__init__(agent, "visualizer/wolf.png");

class Stone(Thing):
    def __init__(self, agent):
        super().__init__(agent, "visualizer/stone.png");

class Grass(Thing):
    def __init__(self, agent):
        super().__init__(agent, "visualizer/grass.png");

class WorldView(arcade.Window):

    def __init__(self, width, height, title, world):
        super().__init__(width, height, title)
        self.world = world;
        self.player_list = None
        self.player_sprite = None
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        for i in self.world.agents:
            if i.type_properties == "sheep":
                player = Sheep(i);
                self.player_list.append(player);
            if i.type_properties == "wolf":
                player = Wolf(i);
                self.player_list.append(player);
        for i in self.world.things:
            if i.type_properties == "stone":
                player = Stone(i);
                self.player_list.append(player);
            if i.type_properties == "grass":
                player = Grass(i);
                self.player_list.append(player);
            
           
    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):

        (things_to_remove, things_to_add) = self.world.run(time_delta=0.3);
        kill_list = list();
        
        for agent in things_to_add:
            if agent.type_properties == "sheep":
                self.player_list.append(Sheep(agent))
            if agent.type_properties == "wolf":
                self.player_list.append(Wolf(agent))
            
        for player in self.player_list:
            if player.agent in things_to_remove:
                kill_list.append(player)
                
        for player in kill_list:
            self.player_list.remove(player)
            
        if len(self.player_list) !=  len(self.world.agents) + len(self.world.things):          
            raise Exception();
            
        self.player_list.update();
        



def start_world(world):        
    window = WorldView(screen_width, screen_height, screen_title, world)
    window.setup()
    arcade.run()

