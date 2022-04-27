#!/usr/bin/python3

# Path
import subprocess
import os

# GUI Application
import gi
import gettext
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf

# variables
_ = gettext.gettext
dir = 'gettoken'

# create date list
date_list = []
for f in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, f)):
        begin, end = f.split('.')
        date_list.append(begin)

# get relative path
rel_path_icon = subprocess.run(['find', '-name', 'visuel.svg'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
rel_path_glade = subprocess.run(['find', '-name', 'visuel.ui'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

# get absolute path
# it's possible to just use the relative path but the absolute path is better
abs_path_folder = subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')
abs_path_icon = rel_path_icon.replace('./', abs_path_folder + '/').replace('\n', '')
abs_path_glade = rel_path_glade.replace('./', abs_path_folder + '/').replace('\n', '')


# Code GUI Application
class MyApplication(Gtk.Application):
    # Main initialization routine
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.activate)

    def activate(self, application):
        windows = self.get_windows()
        if (len(windows) > 0):
            window = windows[0]
            window.present()
            window.show_all()
        else:
            window = MainWindow(self)
            self.add_window(window.window)
            window.window.show_all()

class MainWindow():
    def __init__(self, application):
        
        Gtk.Window.set_default_icon_from_file(abs_path_icon)
        self.application = application
        
        # Set the Glade file
        self.builder = Gtk.Builder()
        gladefile = abs_path_glade
        self.builder.add_from_file(gladefile)
        self.window = self.builder.get_object("main_window")
        self.window.set_icon_name("visuel")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Load dates
        self.app_model = Gtk.ListStore(str)
        for i in date_list:
            self.app_model.append([i])

        # Combo
        self.app_combo = self.builder.get_object("app_combo")
        self.renderer = Gtk.CellRendererText()
        self.app_combo.pack_start(self.renderer, True)
        self.app_combo.add_attribute(self.renderer, "text", 0)
        self.app_combo.set_model(self.app_model)
        self.app_combo.set_active(0) # Select 1st app
            
        # Widget signals
        self.app_combo.connect("changed", self.on_app_changed)
         
        # Menubar
        accel_group = Gtk.AccelGroup()
        self.window.add_accel_group(accel_group)
        menu = self.builder.get_object("main_menu")
        item = Gtk.ImageMenuItem()
        item.set_image(Gtk.Image.new_from_icon_name("help-about-symbolic", Gtk.IconSize.MENU))
        item.set_label(_("About"))
        item.connect("activate", self.open_about)
        key, mod = Gtk.accelerator_parse("F1")
        item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        item = Gtk.ImageMenuItem(label=_("Quit"))
        item.set_image(Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.MENU))
        item.connect('activate', self.on_menu_quit)
        key, mod = Gtk.accelerator_parse("<Control>Q")
        item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        key, mod = Gtk.accelerator_parse("<Control>W")
        item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        menu.show_all()
        
        self.window.set_default_size(800, 500)
        self.window.show_all()
        
        self.load_files()
    
    def open_about(self, widget):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self.window)
        dialog.set_title(_("About"))
        dialog.set_program_name("Visuel")
        dialog.set_comments(_(""))
        try:
            h = open('LICENSE', encoding="utf-8")
            s = h.readlines()
            gpl = ""
            for line in s:
                gpl += line
            h.close()
            dialog.set_license(gpl)
        except Exception as e:
            print (e)

        dialog.set_version("1.0.0")
        dialog.set_icon_name("visuel")
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(abs_path_icon))
        dialog.set_website('https://github.com/0m3re/SNCF')
        dialog.set_authors(['David Glaser', 'Victor Plage'])
        def close(w, res):
            if res == Gtk.ResponseType.CANCEL or res == Gtk.ResponseType.DELETE_EVENT:
                w.destroy()
        dialog.connect("response", close)
        dialog.show()
        
    def on_app_changed(self, widget):
        print("on_app_changed")
    
    def on_menu_quit(self, widget):
        self.application.quit()
    
    # def on_close_button(self, widget):
    #     self.application.quit()
    
    def load_files(self):
        self.builder.get_object("headerbar").set_title(_("Visuel"))
        self.builder.get_object("headerbar").set_subtitle(_("Analytics for SNCF"))
  
if __name__ == "__main__":
    application = MyApplication("org.x.visuel", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()