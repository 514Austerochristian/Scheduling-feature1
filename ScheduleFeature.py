
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton, MDIconButton
from kivy.config import Config
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard

# Set screen size to a range suitable for 4.7" to 9.7" devices
Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Config.set('graphics', 'resizable', 0)

KV = """
Screen:
    auto_keyboard: True

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        pos_hint: {'top': 1}

        MDTextField:
            id: subject_input
            hint_text: "Enter Subject Name"
            mode: "rectangle"
            multiline: False

        MDFloatingActionButton:
            icon: "plus"
            md_bg_color: "green"
            pos_hint: {'x': 0.85, 'y': 0.1}
            on_release: app.add_subject()

        ScrollView:
            MDList:
                id: subject_stack
                padding: dp(10)
                spacing: dp(5)
"""

class SubjectInfoDialog(MDDialog):
    def __init__(self, subject, subject_data, **kwargs):
        self.subject = subject
        self.subject_data = subject_data

        main_layout = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
        )

        self.units_input = MDTextField(hint_text="Enter Units", mode="rectangle", input_filter="int")
        self.meetings_input = MDTextField(hint_text="Enter Number of Meetings", mode="rectangle", input_filter="int")
        self.instructor_input = MDTextField(hint_text="Enter Instructor's Name", mode="rectangle")
        self.room_input = MDTextField(hint_text="Enter Room Number", mode="rectangle")
        self.course_code_input = MDTextField(hint_text="Enter Course Code", mode="rectangle")

        main_layout.add_widget(self.units_input)
        main_layout.add_widget(self.meetings_input)
        main_layout.add_widget(self.instructor_input)
        main_layout.add_widget(self.room_input)
        main_layout.add_widget(self.course_code_input)

        buttons_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10),
        )
        cancel_button = MDRectangleFlatButton(text="CANCEL", on_release=self.dismiss)
        save_button = MDRectangleFlatButton(text="SAVE", on_release=self.save_subject_info)
        buttons_layout.add_widget(cancel_button)
        buttons_layout.add_widget(save_button)
        main_layout.add_widget(buttons_layout)

        super().__init__(
            title=f"Edit Subject: {self.subject}",
            type="custom",
            content_cls=main_layout,
            **kwargs,
        )

        if self.subject_data:
            self.units_input.text = str(self.subject_data.get("units", ""))
            self.meetings_input.text = str(self.subject_data.get("meetings", ""))
            self.instructor_input.text = self.subject_data.get("instructor", "")
            self.room_input.text = self.subject_data.get("room", "")
            self.course_code_input.text = self.subject_data.get("course_code", "")

    def save_subject_info(self, *args):
        units = self.units_input.text
        meetings = self.meetings_input.text
        instructor = self.instructor_input.text
        room = self.room_input.text
        course_code = self.course_code_input.text

        try:
            units = int(units)
            meetings = int(meetings)
            MainApp.get_running_app().root.add_subject_info(
                self.subject, units, meetings, instructor, room, course_code
            )
            self.dismiss()
        except ValueError:
            print("Please enter valid numbers for units and meetings.")

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.root.subjects = {}
        self.root.add_subject_info = self.add_subject_info

    def show_subject_info_dialog(self, subject):
        subject_data = self.root.subjects.get(subject, {})
        dialog = SubjectInfoDialog(subject=subject, subject_data=subject_data)
        dialog.open()

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        if subject:
            if subject not in self.root.subjects:
                self.root.subjects[subject] = {}
                card = MDCard(
                    orientation='horizontal',
                    padding=dp(10),
                    spacing=dp(5),
                    size_hint_y=None,
                    height=dp(60),
                    md_bg_color=(0, 1, 0, 0.5)
                )
                label = MDLabel(text=subject, halign="left", size_hint_x=0.8)
                info_button = MDIconButton(
                    icon="information-outline",
                    size_hint_x=0.2,
                    on_release=lambda instance, subject=subject: self.show_subject_info_dialog(subject)
                )
                card.add_widget(label)
                card.add_widget(info_button)
                self.root.ids.subject_stack.add_widget(card)
                self.root.ids.subject_input.text = ""
            else:
                print("Subject already exists.")
        else:
            print("Please enter a subject.")

    def add_subject_info(self, subject, units, meetings, instructor, room, course_code):
        self.root.subjects[subject]["units"] = units
        self.root.subjects[subject]["meetings"] = meetings
        self.root.subjects[subject]["instructor"] = instructor
        self.root.subjects[subject]["room"] = room
        self.root.subjects[subject]["course_code"] = course_code

if __name__ == "__main__":
    MainApp().run()