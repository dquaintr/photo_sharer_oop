from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filestack import Client
import time
import webbrowser

Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        """Starts cmaera and changes Button text"""
        self.ids.camera.opacity = 1
        self.ids.camera_id.play = True
        self.ids.camera_button_id.text = "Stop Camera"
        self.ids.camera_id.texture = self.ids.camera_id._camera.texture

    def stop(self):
        """Stops Camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera_id.play = False
        self.ids.camera_button_id.text = "Start Camera"
        self.ids.camera_id.texture = None

    def capture(self):
        """Creates a filename with the current time
        and captures and saves a photo image under that filename"""
        filename= time.strftime("%Y%m%d-%H%M%S")
        self.filepath = f"files/{filename}.png"
        self.ids.camera_id.export_to_png(self.filepath)
        self.manager.current = "image_screen"
        self.manager.current_screen.ids.img.source = self.filepath



class FileSharer:

    def __init__(self, filepath, api_key="AA3gSNDpNRCKrRI1mTMQ2z"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)

        new_filelink = client.upload(file="path/to/file")
        return(new_filelink.url)

class ImageScreen(Screen):
    link_message = "Create a Link First"
    def create_link(self):
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        fileshare = FileSharer(filepath = file_path)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message
class RootWidget(ScreenManager):
    pass
class MainApp(App):

    def build(self):
        return RootWidget()
    #initalises object defined above

MainApp().run()
