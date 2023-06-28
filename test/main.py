from kivymd.app import MDApp
from sidepanel import MDSidePanel
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder

class MyScreen(Screen):
    pass

class MyApp(MDApp):

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MyScreen(name = "test"))
        return self.sm
    
Builder.load_string('''
<MyScreen>:
    Label:
        color:0,0,0,1
        text:"Test of using side panel widget"

    Button:
        pos_hint:{'center_x':0.5,'center_y':0.2}
        size_hint:0.5,0.1
        text:"Push me"
        on_press:print("pressed")

    MDSidePanel:
        size_hint_xP:0.8
        side:"left"
        color:[1,1,1,1]

''')


if __name__ == "__main__":
    MyApp().run()