from kivy.properties import NumericProperty,StringProperty,ListProperty,BooleanProperty
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.uix.behaviors import ButtonBehavior

class Panel(BoxLayout):
    left = NumericProperty(0)
    right = NumericProperty(0)
    
    def __init__(self,**a):
        super(Panel,self).__init__(**a)

class PanelButton(CircularRippleBehavior,ButtonBehavior,BoxLayout):
    angle = NumericProperty(0)
    xT = NumericProperty(0)
    yT = NumericProperty(0)
    direction = StringProperty("left")

    def on_release(self):
        if self.direction == "left":
            if self.angle == 0:
                anm = Animation(angle = 25,xT = 0.25,yT = -1.5,duration = .2)
            else:
                anm = Animation(angle = 0,xT = 0,yT=0,duration = .2)
        else:
            if self.angle == 0:
                anm = Animation(angle = -25,xT = -0.25,yT = -1.5,duration = .2)
            else:
                anm = Animation(angle = 0,xT = 0,yT=0,duration = .2)
        anm.start(self)
        return super().on_release()

class MDSidePanel(MDScreen):
    side = StringProperty("left")
    color = ListProperty([1,1,1,1])
    opened = BooleanProperty(False)
    size_hint_xP = NumericProperty(0.7)

    def on_opened(self,instance,value):
        pass  
    
    def add_widget(self, widget, *args, **kwargs):
        if len(self.children)>1:
            self.ids.pl.add_widget(widget, *args, **kwargs)
        else:
            return super().add_widget(widget, *args, **kwargs)
        
    def disen(self):
        i = 0
        for child in MDApp.get_running_app().root.current_screen.children:
            if i!=0:
                child.disabled = (self.open == True)
            i+=1

    def open(self):
        self.ids.pl.opacity = 1
        self.ids.pl.size_hint = (self.size_hint_xP,1)
        self.opened = True
        anm = Animation(pos_hint = {'center_x': (self.ids.btn.direction == "left")*(self.size_hint_xP/2)+(self.ids.btn.direction == "right")*(1-self.size_hint_xP/2),'center_y': 0.5},duration=.2)
        anm.start(self.ids.pl)
        self.disen()

    def close(self):
        self.opened = False
        anm = Animation(pos_hint = {'center_x': (self.ids.btn.direction == "left")*(-self.size_hint_xP/2)+(self.ids.btn.direction == "right")*(1+self.size_hint_xP/2),'center_y': 0.5},size_hint = (0,1),duration=.2)               
        anm.bind(on_complete=self.hideP)
        anm.start(self.ids.pl)
        self.disen()

    def hideP(self,a,w):
        w.opacity = 0

    def toggle(self):
        if self.opened == False:
            self.open()
        else:
            self.close()

Builder.load_string('''
<PanelButton>:
    padding:[dp(15)]
    BoxLayout:
        size_hint:0.65,None
        height:self.width
        pos_hint:{'center_x':0.5,'center_y':0.5}
        orientation: 'vertical'
        spacing:self.height/3
        MDBoxLayout:
            size_hint: 1, 0.01
            md_bg_color: [0,0,0,1]
            canvas.before:
                PushMatrix
                Rotate:
                    angle:root.angle
                    origin:[self.center_x,self.center_y]
                Translate:
                    x:-root.xT*self.width
                    y:root.yT*self.height
            canvas.after:
                PopMatrix
        MDBoxLayout:
            size_hint: 1, 0.01
            md_bg_color: [0,0,0,1]
        MDBoxLayout:
            size_hint: 1, 0.01
            md_bg_color: [0,0,0,1]
            canvas.before:
                PushMatrix
                Rotate:
                    angle:-root.angle
                    origin:[self.center_x,self.center_y]
                Translate:
                    x:-root.xT*self.width
                    y:-root.yT*self.height
            canvas.after:
                PopMatrix


<MDSidePanel>:
    Panel:
        id:pl
        pos_hint:{'center_x':(-root.size_hint_xP/2)*(root.side == "left")+(root.side == "right")*(1+-root.size_hint_xP/2),'center_y':0.5}
        size_hint:0,0
        left:(root.side == "left")*1
        right:(root.side == "right")*1
        canvas:
            Color:
                rgba:0,0,0,0.5
            BoxShadow:
                offset: self.right*2-self.left*2,0
                pos:self.pos
                size:self.size
                blur_radius: 80
                border_radius:[self.right*dp(25),self.left*dp(25),self.left*dp(25),self.right*dp(25)]
            Color:
                rgba:root.color
            RoundedRectangle:
                pos:self.pos
                size:self.size
                radius:[self.right*dp(25),self.left*dp(25),self.left*dp(25),self.right*dp(25)]
                
    PanelButton:
        id:btn
        size_hint:None,0.065
        width:self.height
        pos_hint: {'center_x': 0.92*(root.side == "right")+(root.side == "left")*0.08,'center_y': 0.95}
        direction:root.side
        on_release:root.toggle()
''')

Factory.register("MDSidePanel",cls="MDSidePanel")