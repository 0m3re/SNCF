#!/usr/bin/python3

# import files
from email.mime.text import MIMEText
# from credentials import mypassword, myphone, sncfemail

# Path
import subprocess

# GUI Application
import gi
import gettext
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf

# os for secret.py
import os

# Firefox Webbot
from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import re

# check string
import string

# variables
options = webdriver.FirefoxOptions()
options.headless = True
url = "https://www.digital.sncf.com/startup/api/token-developpeur"
APP = 'token'
_ = gettext.gettext
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# get relative path
rel_path_icon = subprocess.run(['find', '-name', 'token.svg'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
rel_path_glade = subprocess.run(['find', '-name', 'sncf.ui'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

# get absolute path
# it's possible to just use the relative path but the absolute path is better
abs_path_folder = subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')
abs_path_icon = rel_path_icon.replace('./', abs_path_folder + '/').replace('\n', '')
abs_path_glade = rel_path_glade.replace('./', abs_path_folder + '/').replace('\n', '')

# Code for Webbot
def get_token(self, sncf):
    driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    driver.get(url)
    wait = WebDriverWait(driver, 2)


    while True:
        try:
            wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"]')))
            cookie = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"]')
            cookie.click()
        except TimeoutException:
            time.sleep(1) # retry after 1 second
            continue
        break

    firstname = driver.find_element(By.XPATH, '//*[@id="edit-field-user-name-und-0-value"]')
    firstname.send_keys(sncf[0])

    name = driver.find_element(By.XPATH, '//*[@id="edit-field-user-surname-und-0-value"]')
    name.send_keys(sncf[1])

    name = driver.find_element(By.XPATH, '//*[@id="edit-field-api-email-und-0-email"]')
    name.send_keys(sncf[2])

    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    check = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[6]/div/label')
    check.click()


    submit = driver.find_element(By.XPATH, '//*[@id="edit-submit"]')
    submit.click()
    def finderror(self):
        if driver.find_element(By.XPATH, '/html/body/section[1]/dl/dd'):
            error = driver.find_element(By.XPATH, '/html/body/section[1]/dl/dd')
            error = error.text
        
            if "There was a problem with your form submission. Please wait" in error:
                timer = list(map(int, re.findall(r'\d+', error)))
                time.sleep(timer[0] + 1)
                submit = driver.find_element(By.XPATH, '//*[@id="edit-submit"]')
                submit.click()
                finderror(self)
            elif "Veuillez renseigner un email valide." in error:
                MainWindow.errorlabel(self, "Please provide a valid email.")
                driver.quit()
            elif "Votre email existe déjà." in error:
                MainWindow.errorlabel(self, "Your email already exists.")
                driver.quit()    
            else:
                with open('error.txt', 'a') as file:
                    file.write("\n")
                    file.write(str(error))
                # erroremail()
        else:
            driver.quit()
    finderror(self)

# Code to verify if string contains numbers or symbols
def is_number_symbol(word):
    invalidChars = set(string.punctuation.replace("-", "") + string.digits)
    if any(char in invalidChars for char in word):
        return True
    else:
        return False

def check(email):
     
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return False
    else:
        return True

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
            window.show()
        else:
            window = MainWindow(self)
            self.add_window(window.window)
            window.window.show()
            
class SidebarRow(Gtk.ListBoxRow):
    
    def __init__(self, page_widget, page_name, icon_name):
        Gtk.ListBoxRow.__init__(self)
        self.page_widget = page_widget
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_border_width(6)
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        box.pack_start(image, False, False, 0)
        label = Gtk.Label()
        label.set_text(page_name)
        box.pack_start(label, False, False, 0)
        self.add(box)


class MainWindow():
    def __init__(self, application):
        
        Gtk.Window.set_default_icon_from_file(abs_path_icon)
        self.application = application
        
        # Set the Glade file
        self.builder = Gtk.Builder()
        gladefile = abs_path_glade
        self.builder.add_from_file(gladefile)
        self.window = self.builder.get_object("main_window")
        self.window.set_icon_name("token")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Create variables to quickly access dynamic widgets
        self.close_button = self.builder.get_object("close_button")
        self.close_button2 = self.builder.get_object("close_button2")
        self.submit_button = self.builder.get_object("submit_button")
        self.token_button = self.builder.get_object("token_button")
        
        # Widget signals
        self.close_button.connect("clicked", self.on_close_button)
        self.close_button2.connect("clicked", self.on_close_button)
        self.submit_button.connect("clicked", self.on_submit_button)
        self.token_button.connect("clicked", self.on_token_button)

        # Entry Widget
        self.surname_entry = self.builder.get_object("surname_entry")
        self.name_entry = self.builder.get_object("name_entry")
        self.mail_entry = self.builder.get_object("mail_entry")
        self.token_entry = self.builder.get_object("token_entry")
        
        # Setup the main stack
        self.stack = Gtk.Stack()
        self.builder.get_object("center_box").pack_start(self.stack, True, True, 0)
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(150)
        
        # Construct the stack switcher
        list_box = self.builder.get_object("list_navigation")
        
        # Construct the stack switcher
        list_box = self.builder.get_object("list_navigation")

        page = self.builder.get_object("page_home")
        self.stack.add_named(page, "page_home")
        list_box.add(SidebarRow(page, _("Welcome"), "go-home-symbolic"))
        self.stack.set_visible_child(page)

        page = self.builder.get_object("page_token")
        self.stack.add_named(page, "page_token")
        list_box.add(SidebarRow(page, _("Token"), "org.x.Warpinator-symbolic"))

        page = self.builder.get_object("page_secret")
        self.stack.add_named(page, "page_secret")
        list_box.add(SidebarRow(page, _("Secret"), "status-nm-device-wired-secureoffline-symbolic"))

        list_box.connect("row-activated", self.sidebar_row_selected_cb)
        
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

    def open_about(self, widget):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self.window)
        dialog.set_title(_("About"))
        dialog.set_program_name("SNCF Setup")
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
        dialog.set_icon_name("token")
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(abs_path_icon))
        dialog.set_website('https://github.com/0m3re/SNCF')
        dialog.set_authors(['David Glaser', 'Victor Plage'])
        def close(w, res):
            if res == Gtk.ResponseType.CANCEL or res == Gtk.ResponseType.DELETE_EVENT:
                w.destroy()
        dialog.connect("response", close)
        dialog.show()
    
    def on_menu_quit(self, widget):
        self.application.quit()
        
    def sidebar_row_selected_cb(self, list_box, row):
        self.stack.set_visible_child(row.page_widget)
    
    def on_close_button(self, widget):
        self.application.quit()
    
    def on_submit_button(self, widget):
        surname = self.surname_entry.get_text()
        name = self.name_entry.get_text()
        mail = self.mail_entry.get_text()
        sncf = [surname, name, mail]
        if surname == '' or name == '' or mail == '':
            self.errorlabel("You must fill in all the fields.")
        elif is_number_symbol(surname) or is_number_symbol(name):
            self.errorlabel("You can't use this characters in your name or surname.")
        elif check(mail):
            self.errorlabel("This mail is not valid.")
        else:
            get_token(self, sncf)
            
    def on_token_button(self, widget):
        token = self.token_entry.get_text()
        os.chdir('background/')
        with open('secret2.py', 'w') as f:
            f.write('def token():\n')
            f.write('    return "' + token + '"\n')
        os.chdir('..')
        self.application.quit()
    
    def errorlabel(self, msg):
        self.builder.get_object("errorlabel").set_label(_(msg))
    
if __name__ == "__main__":
    application = MyApplication("org.x.token", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()
