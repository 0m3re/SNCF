#!/usr/bin/python3

from loadgui import *
from loadmap import photo
from piechart import pie_chart
from hex_to_gdkrgba import hex_to_gdkrgba
from gdkrgba_to_hex import gdkrgba_to_hex
from colorsave import colorsave

# Path
import os
import datetime
import json 

# GUI Application
import gi
import gettext
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk

# variables
_ = gettext.gettext
dir = 'calculus'
#date = datetime.date.today() - datetime.timedelta(1)
date = '2022-05-11'
lst_color = ['ποΈ', 'ποΈ', 'π΅', 'π', 'π₯ οΈ', 'πΎοΈ', 'ποΈ', 'π§ οΈ', 'ποΈ', 'πΈοΈ', 'ποΈ', 'β«οΈ', 'π¦οΈ', 'ποΈ']
dict_color = { '0' : 'red', '1' : 'lightred', '2' : 'green', '3' : 'orange', '4' : 'beige', '5': 'darkblue', '6': 'darkpurple', '7': 'pink', '8': 'lightblue', '9': 'lightgreen', '10': 'lightgray', '11': 'black', '12': 'gray', '13': 'cadetblue'}



# create date list
date_list = []
for f in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, f)):
        begin, end = f.split('.')
        date_list.append(begin)
        date_list.sort(reverse=True)

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
        
        #load colors
        self.color_model = Gtk.ListStore(str)
        for i in lst_color:
            self.color_model.append([i])
        
        self.combo = [f"self.combo{i}" for i in range(20)]
        for i in range(20):
            self.combo[i] = self.builder.get_object(f"combo{i}")
            self.renderer = Gtk.CellRendererText()
            self.combo[i].pack_start(self.renderer, True)
            self.combo[i].add_attribute(self.renderer, "text", 0)
            self.combo[i].set_model(self.color_model)
            
        # Widget signals
        self.app_combo.connect("changed", self.on_app_changed)
        
        # Create variables to quickly access dynamic widgets
        self.reload_button1 = self.builder.get_object("reload_img1")
        self.reload_button2 = self.builder.get_object("reload_img2")
        self.reload_pie = self.builder.get_object("reload_pie")
        
        # Widget signals
        self.reload_button1.connect("clicked", self.on_reload_button1)
        self.reload_button2.connect("clicked", self.on_reload_button2)
        self.reload_pie.connect("clicked", self.on_reload_pie)
         
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
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file('visuel/icons/visuel.svg'))
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
        lst_lat_time, lst_long_time = city_lat_lon_1(jour)
        one = 1
        choosen_color1 = []
        for i in range(10):     
            choosen_color1.append(dict_color.get(str(self.combo[i].get_active()), str(self.combo[i].get_active())))
        photo(jour, lst_lat_time, lst_long_time, choosen_color1, one)
    
    def img_number(self, jour): 
        lst_lat_number, lst_long_number = city_lat_lon_2(jour)
        two = 2
        choosen_color2 = []
        for i in range(10,20):   
            choosen_color2.append(dict_color.get(str(self.combo[i].get_active()), str(self.combo[i].get_active())))
        photo(jour, lst_lat_number, lst_long_number, choosen_color2, two)
    
    def img_pie(self, jour):
        colors = []
        for i in range(10):
            self.color_button = self.builder.get_object(f"colorbt{i}")
            rgba = self.color_button.get_rgba()
            colors.append(gdkrgba_to_hex(rgba))
        pie_chart(jour, colors)
    
    def on_reload_button1(self, widget):
        jour = date_list[self.app_combo.get_active()]
        self.img_time(jour)
        self.builder.get_object("gare_img1").set_from_file(f"visuel/img/{jour}1.png")
        self.save_to_file()
        
    
    def on_reload_button2(self, widget):
        jour = date_list[self.app_combo.get_active()]
        self.img_number(jour)
        self.builder.get_object("gare_img2").set_from_file(f"visuel/img/{jour}2.png")
        self.save_to_file()
    
    def on_reload_pie(self, widget):
        jour = date_list[self.app_combo.get_active()]
        self.img_pie(jour)
        self.builder.get_object("pie_chart").set_from_file(f"visuel/img/{jour}_pie_chart.png")
        self.save_to_file()

    def save_to_file(self):
        jour = date_list[self.app_combo.get_active()]
        
        # data map colors
        choosen_color1 = []
        for i in range(10):
            choosen_color1.append(self.combo[i].get_active())
        
        #number map colors
        choosen_color2 = []
        for i in range(10,20):   
            choosen_color2.append(self.combo[i].get_active())
            
        #pie chart colors
        colors = []
        for i in range(10):
            self.color_button = self.builder.get_object(f"colorbt{i}")
            rgba = self.color_button.get_rgba()
            colors.append(gdkrgba_to_hex(rgba))
        
        colorsave(jour, choosen_color1, choosen_color2, colors)
    
    def load_files(self, jour):
        a, b, c, d, e, f, g, n, u = load(jour)
        phrase = f"During the day of {jour}, there were a total of {a} trains running. These trains passed through {b} stations. Naturally, there were some late trains. There were nearly {c} trains late, which corresponds to nearly {d} % of all the trains running. {e} stations have been crossed by these late trains. This corresponds to {f}% of all stations visited during the same day. These late trains also had an impact on the lines open during the day of {jour}, because on the {g} lines open, nearly {u} % had at least one train late. There were only {round(g-(g*u)/100)} lines without delay, namely {round(100-u,2)} %. At this stage you are probably saying to yourself : But the accumulated time must be enormous ! No it's only {n}."
        self.builder.get_object("info_label").set_label(_(phrase))
        
        text0 = f""
        self.builder.get_object("text_0").set_label(_(text0))
        text1 = f""
        self.builder.get_object("text_0").set_label(_(text1))
        text2 = f""
        self.builder.get_object("text_0").set_label(_(text2))
        text3 = f""
        self.builder.get_object("text_0").set_label(_(text3))
        
        lst_data_time, lst_value_time, lst_data_number, lst_value_number = city_time(jour)
        lst_problems, lst_pourcentage = problems(jour)
        for i in range(10):
            self.builder.get_object(f"gare{i}").set_label(_(lst_data_time[i]))
            self.builder.get_object(f"time{i}").set_label(_(lst_value_time[i]))
            self.builder.get_object(f"gare_{i}").set_label(_(str(lst_data_number[i])))
            self.builder.get_object(f"number{i}").set_label(_(str(lst_value_number[i])))
            self.builder.get_object(f"pb_{i}").set_label(_(lst_problems[i]))
        
        if not os.path.exists(f"visuel/colors/colors_{jour}.json"):
            colors = ['#ff0000ff', '#ff7f00ff', '#00ffffff', '#096a09ff', '#24445cff', '#ffff00ff', '#2e006cff', '#f056ffff', '#1b019bff', '#6c0277ff']
            choosen_color1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            choosen_color2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            
        else:
            with open(f"visuel/colors/colors_{jour}.json") as json_color:
                data = json.load(json_color)
                colors = []
                choosen_color1 = []
                choosen_color2 = []
                for j in range(10):
                    colors.append(data[f"pie_{j}"])
                    choosen_color1.append(data[f"map1_{j}"])
                    choosen_color2.append(data[f"map2_{j}"])
        
        for i in range(10):
            self.builder.get_object(f"colorbt{i}").set_rgba(hex_to_gdkrgba(colors[i]))
            self.combo[i].set_active(choosen_color1[i])
            self.combo[i+10].set_active(choosen_color2[i])
            
        if not os.path.exists(f"visuel/img"):
            os.mkdir(f"visuel/img")

        
        if not os.path.exists(f"visuel/img/{jour}1.png") or not os.path.exists(f"visuel/img/{jour}2.png"):
            self.img_time(jour)
            self.img_number(jour)
        
        
        if not os.path.exists(f"visuel/img/{jour}_pie_chart.png"):
            pie_chart(jour, colors)

        self.builder.get_object("gare_img1").set_from_file(f"visuel/img/{jour}1.png")
        self.builder.get_object("gare_img2").set_from_file(f"visuel/img/{jour}2.png")
        
        self.builder.get_object("pie_chart").set_from_file(f"visuel/img/{jour}_pie_chart.png")
            
          
if __name__ == "__main__":
    application = MyApplication("org.x.visuel", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()
