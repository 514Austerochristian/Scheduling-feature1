from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.config import Config
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.graphics import Rectangle

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

        MDTextField:
            id: units_input
            hint_text: "Enter Units"
            mode: "rectangle"
            input_filter: "int"
            multiline: False

        MDTextField:
            id: meetings_input
            hint_text: "Enter Number of Meetings"
            mode: "rectangle"
            input_filter: "int"
            multiline: False

        MDTextField:
            id: instructor_input
            hint_text: "Enter Instructor's Name"
            mode: "rectangle"
            multiline: False

        MDTextField:
            id: room_input
            hint_text: "Enter Room Number"
            mode: "rectangle"
            multiline: False

        MDTextField:
            id: course_code_input
            hint_text: "Enter Course Code"
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

    MDBottomNavigation:
        size_hint_y: None
        height: dp(56)

        MDBottomNavigationItem:
            name: "screen_home"
            icon: "home"
            text: "Home"

        MDBottomNavigationItem:
            name: "screen_schedules"
            icon: "calendar"
            text: "Schedules"

        MDBottomNavigationItem:
            name: "screen_contacts"
            icon: "contacts"
            text: "Contacts"

        MDBottomNavigationItem:
            name: "screen_todo"
            icon: "check-circle"
            text: "To-Do's"
"""


class SubjectInfoDialog(MDDialog):
    def __init__(self, subject, subject_data, **kwargs):
        self.subject = subject
        self.subject_data = subject_data

        # Create the background using Canvas (without color)
        background_box = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(375), dp(380)),
            pos_hint={'center_x': 0.5},
        )

        with background_box.canvas.before:
            self.rect = Rectangle(size=background_box.size, pos=background_box.pos)

        # "Subject Info:" title at the top
        title_label = MDLabel(
            text="Subject Info:",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(40),
        )
        background_box.add_widget(title_label)

        # Display the subject name as the next label
        subject_label = MDLabel(
            text=self.subject,
            theme_text_color="Primary",
            font_style="H4",
            size_hint_y=None,
            height=dp(50),
        )
        background_box.add_widget(subject_label)

        # Display the details of the subject with a custom font size for better readability
        details = f"""
        Units: {self.subject_data['units']}
        Meetings: {self.subject_data['meetings']}
        Instructor: {self.subject_data['instructor']}
        Room: {self.subject_data['room']}
        Course Code: {self.subject_data['course_code']}
        """

        # Set font size for the details (slightly larger than default)
        detail_label = MDLabel(
            text=details,
            theme_text_color="Secondary",
            font_style="Body1",  # This will be larger than default font size
            size_hint_y=None,
            height=dp(200),
            halign="left"
        )

        background_box.add_widget(detail_label)

        # Done button to close the dialog and return to the main screen, positioned at bottom-right
        done_button = MDFloatingActionButton(
            icon="check",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            pos_hint={'right': 0.9, 'bottom': 0},  # Move button to the left by reducing the 'right' value
            on_release=self.dismiss,
            md_bg_color=(0, 0.5, 0, 1)  # Dark green color
        )

        background_box.add_widget(done_button)

        # Adjust the dialog size to make the background bigger
        super().__init__(
            title="",  # Removing the title here since it's already in the dialog content
            type="custom",
            content_cls=background_box,
            size_hint=(None, None),
            size=(dp(375), dp(400)),  # Increased size for the dialog to match canvas size
            **kwargs,
        )


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.root.subjects = {}

    def show_subject_info_dialog(self, subject):
        subject_data = self.root.subjects.get(subject, {})
        dialog = SubjectInfoDialog(subject=subject, subject_data=subject_data)
        dialog.open()

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        units = self.root.ids.units_input.text
        meetings = self.root.ids.meetings_input.text
        instructor = self.root.ids.instructor_input.text
        room = self.root.ids.room_input.text
        course_code = self.root.ids.course_code_input.text

        # Check if all inputs are filled
        if subject and units and meetings and instructor and room and course_code:
            # Add subject to the dictionary
            if subject not in self.root.subjects:
                self.root.subjects[subject] = {
                    "units": int(units),
                    "meetings": int(meetings),
                    "instructor": instructor,
                    "room": room,
                    "course_code": course_code,
                }

                # Create a card to show the subject name in the list
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

                # Add card to the stack (subject list)
                self.root.ids.subject_stack.add_widget(card)

                # Clear input fields
                self.root.ids.subject_input.text = ""
                self.root.ids.units_input.text = ""
                self.root.ids.meetings_input.text = ""
                self.root.ids.instructor_input.text = ""
                self.root.ids.room_input.text = ""
                self.root.ids.course_code_input.text = ""
            else:
                print("Subject already exists.")
        else:
            print("Please fill all the fields.")


if __name__ == "__main__":
    MainApp().run()