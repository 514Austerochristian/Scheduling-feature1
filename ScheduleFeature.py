from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDTextField:
        id: subject_input
        hint_text: "Enter subject"
    MDRaisedButton:
        text: "Add Subject"
        on_release: app.add_subject()
    ScrollView:
        MDBoxLayout:
            id: subject_stack
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
'''

class SubjectInfoDialog(BoxLayout):
    def __init__(self, subject, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.subject = subject
        self.add_widget(MDTextField(hint_text="Units", id="units_input"))
        self.add_widget(MDTextField(hint_text="Meetings", id="meetings_input"))
        self.add_widget(MDTextField(hint_text="Instructor", id="instructor_input"))
        self.add_widget(MDTextField(hint_text="Room", id="room_input"))
        self.add_widget(MDTextField(hint_text="Course Code", id="course_code_input"))
        self.add_widget(MDRaisedButton(text="Save", on_release=self.save_subject_info))

    def save_subject_info(self, *args):
        units = self.ids.units_input.text
        meetings = self.ids.meetings_input.text
        instructor = self.ids.instructor_input.text
        room = self.ids.room_input.text
        course_code = self.ids.course_code_input.text

        try:
            units = int(units)
            meetings = int(meetings)
            app = MDApp.get_running_app()
            app.add_subject_info(self.subject, units, meetings, instructor, room, course_code)
            self.parent.parent.dismiss()
        except ValueError:
            print("Please enter valid numbers for units and meetings.")

class MainApp(MDApp):
    def build(self):
        print("Building the application...")
        return Builder.load_string(KV)

    def on_start(self):
        print("Application started.")
        self.root.subjects = {}

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        if subject:
            if subject not in self.root.subjects:
                self.root.subjects[subject] = {} # Initialize empty dictionary
                card = MDCard(
                    orientation='horizontal',
                    padding=dp(10),
                    spacing=dp(5),
                    size_hint_y=None,
                    height=dp(60),
                )
                label = MDLabel(text=subject)
                info_button = MDRaisedButton(text="i", on_release=lambda x: self.show_subject_info_dialog(subject))
                card.add_widget(label)
                card.add_widget(info_button)
                self.root.ids.subject_stack.add_widget(card)
                self.root.ids.subject_input.text = ""
                self.root.ids.subject_stack.height = len(self.root.ids.subject_stack.children) * dp(70)
            else:
                print("Subject already exists.")
        else:
            print("Please enter a subject.")

    def show_subject_info_dialog(self, subject):
        dialog_content = SubjectInfoDialog(subject=subject)
        self.dialog = MDDialog(
            title="Enter Subject Info",
            type="custom",
            content_cls=dialog_content,
        )
        self.dialog.open()

    def add_subject_info(self, subject, units, meetings, instructor, room, course_code):
        self.root.subjects[subject]["units"] = units
        self.root.subjects[subject]["meetings"] = meetings
        self.root.subjects[subject]["instructor"] = instructor
        self.root.subjects[subject]["room"] = room
        self.root.subjects[subject]["course_code"] = course_code
        print(self.root.subjects)

if __name__ == "__main__":
    print("Starting the application...")
    MainApp().run()