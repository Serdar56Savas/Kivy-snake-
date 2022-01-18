from kivy.app import App
from kivy.uix.label import Label

class ilkUygulama(App):
    def build(self):
        self.title="Serdar Savaş"
        return Label(text="Merhaba kivy")

ilkUygulama().run()