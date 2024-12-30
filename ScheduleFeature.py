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
            name: "screen_schedules"
            icon: "calendar"
            text: "My Classes"

        MDBottomNavigationItem:
            name: "screen_todo"
            icon: "check-circle"
            text: "To-Do's"

        MDBottomNavigationItem:
            name: "screen_home"
            icon: "home"
            text: "Home"

        MDBottomNavigationItem:
            name: "screen_contacts"
            icon: "contacts"
            text: "Contacts"
"""


# AVL Tree Node
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.height = 1
        self.left = None
        self.right = None


# AVL Tree Implementation
class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key, data):
        if not root:
            return AVLNode(key, data)
        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancing the tree
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def in_order(self, root):
        if not root:
            return []
        return self.in_order(root.left) + [(root.key, root.data)] + self.in_order(root.right)


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
            md_bg_color: "seagreen"
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
            name: "screen_schedules"
            icon: "calendar"
            text: "My Classes"

        MDBottomNavigationItem:
            name: "screen_todo"
            icon: "check-circle"
            text: "To-Do's"

        MDBottomNavigationItem:
            name: "screen_home"
            icon: "home"
            text: "Home"

        MDBottomNavigationItem:
            name: "screen_contacts"
            icon: "contacts"
            text: "Contacts"
"""


# AVL Tree Node
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.height = 1
        self.left = None
        self.right = None


# AVL Tree Implementation
class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key, data):
        if not root:
            return AVLNode(key, data)
        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancing the tree
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def in_order(self, root):
        if not root:
            return []
        return self.in_order(root.left) + [(root.key, root.data)] + self.in_order(root.right)


class SubjectInfoDialog(MDDialog):
    def __init__(self, subject, subject_data, **kwargs):
        self.subject = subject
        self.subject_data = subject_data

        details = f"""
        Units: {self.subject_data['units']}
        Meetings: {self.subject_data['meetings']}
        Instructor: {self.subject_data['instructor']}
        Room: {self.subject_data['room']}
        Course Code: {self.subject_data['course_code']}
        """

        # Add a done button
        super().__init__(
            title=f"Subject Info: {self.subject}",
            text=details,
            buttons=[
                MDIconButton(icon="check",
                             md_bg_color = "seagreen",

                on_release=self.dismiss),
            ],
            md_bg_color = "mediumseagreen",
            **kwargs,
        )


class MainApp(MDApp):
    def build(self):
        self.tree = AVLTree()
        self.root_node = None
        return Builder.load_string(KV)

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        units = self.root.ids.units_input.text
        meetings = self.root.ids.meetings_input.text
        instructor = self.root.ids.instructor_input.text
        room = self.root.ids.room_input.text
        course_code = self.root.ids.course_code_input.text

        if subject and units and meetings and instructor and room and course_code:
            data = {
                "units": int(units),
                "meetings": int(meetings),
                "instructor": instructor,
                "room": room,
                "course_code": course_code,
            }

            self.root_node = self.tree.insert(self.root_node, subject, data)
            self.display_subjects()

            self.root.ids.subject_input.text = ""
            self.root.ids.units_input.text = ""
            self.root.ids.meetings_input.text = ""
            self.root.ids.instructor_input.text = ""
            self.root.ids.room_input.text = ""
            self.root.ids.course_code_input.text = ""
        else:
            print("Please fill all fields.")

    def display_subjects(self):
        self.root.ids.subject_stack.clear_widgets()
        for subject, data in self.tree.in_order(self.root_node):
            card = MDCard(
                orientation="horizontal",
                padding=dp(10),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(60),
                md_bg_color="mediumseagreen",  # Green background
            )
            label = MDLabel(text=subject, halign="left", size_hint_x=0.8)
            info_button = MDIconButton(
                icon="information-outline",
                size_hint_x=0.2,
                on_release=lambda instance, subject=subject: self.show_subject_info_dialog(subject),
            )
            card.add_widget(label)
            card.add_widget(info_button)
            self.root.ids.subject_stack.add_widget(card)

    def show_subject_info_dialog(self, subject):
        for key, data in self.tree.in_order(self.root_node):
            if key == subject:
                dialog = SubjectInfoDialog(subject=subject, subject_data=data)
                dialog.open()
                break


if __name__ == "__main__":
    MainApp().run()