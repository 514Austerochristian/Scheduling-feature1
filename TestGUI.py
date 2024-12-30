from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config

# Enable debug logging
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_enable', 1)

KV = '''
FloatLayout:
    MDTextField:
        id: subject_input
        hint_text: "Enter subject"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint: 0.8, None
        height: dp(40)
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0, 1, 0, 1
        pos_hint: {'x': 0.05, 'y': 0.05}
        on_release: app.add_subject()
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        if subject:
            print(f"Subject added: {subject}")
        else:
            print("Please enter a subject.")

if __name__ == "__main__":
    MainApp().run()