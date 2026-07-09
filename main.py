from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform
from PIL import Image, ImageEnhance
import cv2
import os
import threading
from datetime import datetime

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "4K Upscaler Free"
            md_bg_color: "#0F0F0F"
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            padding: "10dp"
            md_bg_color: "#1C1C1C"
            MDLabel:
                text: "Mode:"
            MDSwitch:
                id: ai_switch
                on_active: mode_label.text = "Mode: Online AI" if self.active else "Mode: Offline"
            MDLabel:
                id: mode_label
                text: "Mode: Offline"
                bold: True
        MDBottomNavigation:
            panel_color: "#0F0F0F"
            MDBottomNavigationItem:
                name: "image"
                text: "Image"
                icon: "image-outline"
                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "15dp"
                        spacing: "12dp"
                        adaptive_height: True
                        MDLabel:
                            text: "IMAGE UPSCALER"
                            bold: True
                        MDBoxLayout:
                            spacing: "8dp"
                            adaptive_height: True
                            MDRaisedButton:
                                text: "2x"
                                on_release: app.set_preset("2x", "image")
                            MDRaisedButton:
                                text: "4x"
                                on_release: app.set_preset("4x", "image")
                            MDRaisedButton:
                                text: "4K"
                                md_bg_color: "#6200EE"
                                on_release: app.set_preset("4k", "image")
                        MDBoxLayout:
                            spacing: "10dp"
                            adaptive_height: True
                            MDTextField:
                                id: img_w
                                hint_text: "Width Pixels"
                                text: "3840"
                                input_filter: "int"
                            MDTextField:
                                id: img_h
                                hint_text: "Height Pixels"
                                text: "2160"
                                input_filter: "int"
                        MDRaisedButton:
                            text: "Gallery Se Image Chuno"
                            size_hint_x: 1
                            md_bg_color: "#03DAC6"
                            on_release: app.open_file_manager("image")
                        MDLabel:
                            id: img_file_label
                            text: "Koi image select nahi hai"
                            halign: "center"
                        FitImage:
                            id: img_preview
                            size_hint_y: None
                            height: "280dp"
                            radius: [15,]
                        MDRaisedButton:
                            text: "4K ME UPSCALE KARO"
                            size_hint_x: 1
                            height: "50dp"
                            md_bg_color: "#6200EE"
                            on_release: app.start_upscale("image")
            MDBottomNavigationItem:
                name: "video"
                text: "Video"
                icon: "video-outline"
                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "15dp"
                        spacing: "12dp"
                        adaptive_height: True
                        MDLabel:
                            text: "VIDEO UPSCALER"
                            bold: True
                        MDBoxLayout:
                            spacing: "8dp"
                            adaptive_height: True
                            MDRaisedButton:
                                text: "4K 3840x2160"
                                md_bg_color: "#6200EE"
                                on_release: app.set_preset("4k", "video")
                            MDRaisedButton:
                                text: "2K"
                                on_release: app.set_preset("2k", "video")
                            MDRaisedButton:
                                text: "1080p"
                                on_release: app.set_preset("1080p", "video")
                        MDBoxLayout:
                            spacing: "10dp"
                            adaptive_height: True
                            MDTextField:
                                id: vid_w
                                hint_text: "Width Pixels"
                                text: "3840"
                                input_filter: "int"
                            MDTextField:
                                id: vid_h
                                hint_text: "Height Pixels"
                                text: "2160"
                                input_filter: "int"
                        MDRaisedButton:
                            text: "Gallery Se Video Chuno"
                            size_hint_x: 1
                            md_bg_color: "#03DAC6"
                            on_release: app.open_file_manager("video")
                        MDLabel:
                            id: vid_file_label
                            text: "Koi video select nahi hai"
                            halign: "center"
                        MDRaisedButton:
                            text: "VIDEO KO 4K ME CONVERT KARO"
                            size_hint_x: 1
                            height: "50dp"
                            md_bg_color: "#6200EE"
                            on_release: app.start_upscale("video")
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            orientation: "vertical"
            MDProgressBar:
                id: progress
                value: 0
            MDLabel:
                id: status_label
                text: "Ready"
                halign: "center"
'''

class UpscalerFreeApp(MDApp):
    selected_image = StringProperty("")
    selected_video = StringProperty("")
    current_type = ""
    def build(self):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        self.screen = Builder.load_string(KV)
        return self.screen
    def set_preset(self, preset, typ):
        ids = self.screen.ids
        w_field = ids.img_w if typ == "image" else ids.vid_w
        h_field = ids.img_h if typ == "image" else ids.vid_h
        if preset == "4k": w_field.text, h_field.text = "3840", "2160"
        elif preset == "2k": w_field.text, h_field.text = "2560", "1440"
        elif preset == "1080p": w_field.text, h_field.text = "1920", "1080"
        elif preset == "2x" or preset == "4x": w_field.text = preset
    def open_file_manager(self, file_type):
        self.current_type = file_type
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_MEDIA_IMAGES, Permission.READ_MEDIA_VIDEO, Permission.INTERNET])
        path = "/storage/emulated/0/DCIM" if platform == "android" else "/"
        self.file_manager.show(path)
    def select_path(self, path):
        self.exit_manager()
        if self.current_type == "image":
            self.selected_image = path
            self.screen.ids.img_file_label.text = path.split("/")[-1]
            self.screen.ids.img_preview.source = path
        else:
            self.selected_video = path
            self.screen.ids.vid_file_label.text = path.split("/")[-1]
    def exit_manager(self, *args):
        self.file_manager.close()
    def start_upscale(self, typ):
        threading.Thread(target=lambda: self.do_upscale(typ), daemon=True).start()
    def do_upscale(self, typ):
        try:
            ids = self.screen.ids
            is_online = ids.ai_switch.active
            out_dir = "/storage/emulated/0/DCIM/4K Upscaler Free" if platform == "android" else os.path.expanduser("~/Downloads")
            os.makedirs(out_dir, exist_ok=True)
            if typ == "image":
                if not self.selected_image: ids.status_label.text = "Pehle image chuno!"; return
                ids.status_label.text = "Processing Image..."
                ids.progress.value = 30
                w_text, h_text = ids.img_w.text, ids.img_h.text
                img = Image.open(self.selected_image)
                orig_w, orig_h = img.size
                if w_text == "2x": w, h = orig_w*2, orig_h*2
                elif w_text == "4x": w, h = orig_w*4, orig_h*4
                else: w, h = int(w_text), int(h_text)
                upscaled = img.resize((w, h), Image.LANCZOS)
                if is_online:
                    ids.status_label.text = "Online AI Mode: Sharp kar raha hu..."
                    enhancer = ImageEnhance.Sharpness(upscaled)
                    upscaled = enhancer.enhance(1.8)
                ids.progress.value = 90
                out_path = os.path.join(out_dir, f"IMG_4K_{w}x{h}_{datetime.now().strftime('%H%M%S')}.png")
                upscaled.save(out_path, quality=95)
                ids.img_preview.source = out_path
            else:
                if not self.selected_video: ids.status_label.text = "Pehle video chuno!"; return
                ids.status_label.text = "Video Upscaling... 2-3 min lagega"
                ids.progress.value = 20
                w, h = int(ids.vid_w.text), int(ids.vid_h.text)
                cap = cv2.VideoCapture(self.selected_video)
                fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                out_path = os.path.join(out_dir, f"VID_4K_{w}x{h}_{datetime.now().strftime('%H%M%S')}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
                count = 0
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LANCZOS4)
                    out.write(resized)
                    count+=1
                    ids.progress.value = 20 + int((count/total_frames)*70)
                cap.release()
                out.release()
            ids.progress.value = 100
            ids.status_label.text = f"Ho Gaya! Gallery me dekho: {out_dir}"
        except Exception as e:
            ids.status_label.text = f"Error: {e}"

UpscalerFreeApp().run()
