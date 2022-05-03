#!/usr/bin/python3

#
import random
from loadgui import load, city_time, city_lat_lon
from loadmap import photo
import numpy

# Path
import os
import datetime

# GUI Application
import gi
import gettext
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf

# variables
_ = gettext.gettext
dir = 'calculus'
date = datetime.date.today() - datetime.timedelta(1)
lst_color = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']



# create date list
date_list = []
for f in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, f)):
        begin, end = f.split('.')
        date_list.append(begin)

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
        
        #Gtk.Window.set_default_icon_from_file(abs_path_icon)
        Gtk.Window.set_default_icon_from_file('visuel/icons/visuel.svg')
        self.application = application
        
        # Set the Glade file
        self.builder = Gtk.Builder()
        # gladefile = abs_path_glade
        #self.builder.add_from_file(gladefile)
        self.builder.add_from_file('visuel/visuel.ui')
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
        
        # Create variables to quickly access dynamic widgets
        self.reload_button = self.builder.get_object("reload_img")
        
        # Widget signals
        self.reload_button.connect("clicked", self.on_reload_button)
         
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
        
        self.window.show_all()
        
        self.load_files(date)
    
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
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file('visuel/icons/visuel.py'))
        dialog.set_website('https://github.com/0m3re/SNCF')
        dialog.set_authors(['David Glaser', 'Victor Plage'])
        def close(w, res):
            if res == Gtk.ResponseType.CANCEL or res == Gtk.ResponseType.DELETE_EVENT:
                w.destroy()
        dialog.connect("response", close)
        dialog.show()
        
    def on_app_changed(self, widget):
        jour = date_list[self.app_combo.get_active()]
        self.load_files(str(jour))
        return jour
    
    def on_menu_quit(self, widget):
        self.application.quit()
    
    def img_time(self, jour):
        lst_lat_time, lst_long_time, lst_lat_number, lst_long_number = city_lat_lon(jour)
        color = numpy.random.choice(lst_color)
        photo(jour, lst_lat_time, lst_long_time, color)
    
    def on_reload_button(self, widget):
        jour = date_list[self.app_combo.get_active()]
        self.img_time(jour)
        
    def load_files(self, jour):
        a, b, c, d, e, f, g, n, u = load(jour)
        phrase = f"During the day of {jour}, there were a total of {a} trains running. These trains passed through {b} stations. Naturally, there were some late trains. There were nearly {c} trains late, which corresponds to nearly {d} % of all the trains running. {e} stations have been crossed by these late trains. This corresponds to {f}% of all stations visited during the same day. These late trains also had an impact on the lines open during the day of {jour}, because on the {g} lines open, nearly {u} % had at least one train late. There were only {round(g-(g*u)/100)} lines without delay, namely {round(100-u,2)} %. At this stage you are probably saying to yourself : But the accumulated time must be enormous ! No it's only {n}."
        self.builder.get_object("info_label").set_label(_(phrase))
        
        lst_data_time, lst_value_time, lst_data_number, lst_value_number = city_time(jour)
        for i in range(10):
            self.builder.get_object(f"gare{i}").set_label(_(lst_data_time[i]))
            self.builder.get_object(f"time{i}").set_label(_(lst_value_time[i]))
            self.builder.get_object(f"gare_{i}").set_label(_(str(lst_data_number[i])))
            self.builder.get_object(f"number{i}").set_label(_(str(lst_value_number[i])))
        
        self.img_time(jour)
        
        self.builder.get_object("gare_img").set_from_file(f"visuel/img/{jour}.png")
            
          
if __name__ == "__main__":
    application = MyApplication("org.x.visuel", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()
