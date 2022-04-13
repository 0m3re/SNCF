#!/usr/bin/python3

# import files
from emailpassword import password

# Path
import subprocess

# GUI Application
import gi
import gettext
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf

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

# send email with error
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# variables
options = webdriver.FirefoxOptions()
options.headless = True
url = "https://www.digital.sncf.com/startup/api/token-developpeur"
APP = 'token'
_ = gettext.gettext

# get relative path
rel_path_icon = subprocess.run(['find', '-name', 'token.svg'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
rel_path_glade = subprocess.run(['find', '-name', 'sncf.ui'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

# get absolute path
# it's possible to just use the relative path but the absolute path is better
abs_path_folder = subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')
abs_path_icon = rel_path_icon.replace('./', abs_path_folder + '/').replace('\n', '')
abs_path_glade = rel_path_glade.replace('./', abs_path_folder + '/').replace('\n', '')

# Code for Webbot
def get_token(sncf):
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
    def finderror():
        if driver.find_element(By.XPATH, '/html/body/section[1]/dl/dd'):
            error = driver.find_element(By.XPATH, '/html/body/section[1]/dl/dd')
            error = error.text
        
            if "There was a problem with your form submission. Please wait" in error:
                timer = list(map(int, re.findall(r'\d+', error)))
                time.sleep(timer[0] + 1)
                submit = driver.find_element(By.XPATH, '//*[@id="edit-submit"]')
                submit.click()
                finderror()
            # elif error == "Votre email existe déjà.":
            #     print("Votre email existe déjà.")
            #     finderror()
            else:
                with open('error.txt', 'w') as f:
                    f.write(str(error))
                erroremail()
        else:
            driver.quit()
    finderror()

# Code for sending email with error
def erroremail():
    sender_email = "sncferror@gmail.com"
    receiver_emails = ['d2ave@gmx.de', 'vi03pl@gmail.com']
    message = MIMEMultipart()
    message["From"] = sender_email
    message['To'] = ", ".join(receiver_emails)
    message['Subject'] = "Not referenced Error"
    file = "error.txt"
    attachment = open(file,'rb')
    obj = MIMEBase('application','octet-stream')
    obj.set_payload((attachment).read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition',"attachment; filename= " + file)
    message.attach(obj)
    my_message = message.as_string()
    email_session = smtplib.SMTP('localhost', 1025)
    email_session.starttls()
    email_session.login(sender_email, password())
    email_session.sendmail(sender_email, receiver_emails, my_message)
    email_session.quit()

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


class MainWindow():
    def __init__(self, application):
        
        Gtk.Window.set_default_icon_from_file(abs_path_icon)
        self.application = application
        
        # Set the Glade file
        gladefile = abs_path_glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.window = self.builder.get_object("main_window")
        self.window.set_title(_("Token..."))
        self.window.set_icon_name("token")
        
        # Create variables to quickly access dynamic widgets
        self.close_button = self.builder.get_object("close_button")
        self.submit_button = self.builder.get_object("submit_button")
        
        # Widget signals
        self.close_button.connect("clicked", self.on_close_button)
        self.submit_button.connect("clicked", self.on_submit_button)

        # Entry Widget
        self.surname_entry = self.builder.get_object("surname_entry")
        self.name_entry = self.builder.get_object("name_entry")
        self.mail_entry = self.builder.get_object("mail_entry")
        
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
        
        self.load_files()
    
    def open_about(self, widget):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self.window)
        dialog.set_title(_("About"))
        dialog.set_program_name("Get Token")
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
        
    def on_close_button(self, widget):
        self.application.quit()
    
    def on_submit_button(self, widget):
        surname = self.surname_entry.get_text()
        name = self.name_entry.get_text()
        mail = self.mail_entry.get_text()
        sncf = [surname, name, mail]
        if surname == '' or name == '' or sncf == '':
            print('You have to enter something')
        else:
            get_token(sncf)
                
        
    def load_files(self):
        self.builder.get_object("headerbar").set_title(_("Get Token"))
        self.builder.get_object("headerbar").set_subtitle(_("Get the Token for SNCF"))
         
if __name__ == "__main__":
    application = MyApplication("org.x.token", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()