#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

#variables

sncf = []


class EntryWindow(Gtk.Window):
    def __init__(self):
        super(EntryWindow, self).__init__()
        
        self.init_ui()

    def init_ui(self):    

        #self.set_icon_from_file("web.png")
        self.set_border_width(10)
        self.set_title("Token")
        self.set_default_size(400, 300)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("Prénom")
        self.entry.set_halign(Gtk.Align.CENTER)
        self.entry.set_valign(Gtk.Align.CENTER)
        vbox.pack_start(self.entry, True, True, 0)
        
        self.entry2 = Gtk.Entry()
        self.entry2.set_text("Nom")
        self.entry2.set_halign(Gtk.Align.CENTER)
        self.entry2.set_valign(Gtk.Align.CENTER)
        vbox.pack_start(self.entry2, True, True, 0)
        
        self.entry3 = Gtk.Entry()
        self.entry3.set_text("Mail")
        self.entry3.set_halign(Gtk.Align.CENTER)
        self.entry3.set_valign(Gtk.Align.CENTER)
        vbox.pack_start(self.entry3, True, True, 0)


        self.button = Gtk.Button(label="Submit")
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_valign(Gtk.Align.CENTER)
        self.button.connect("clicked", self.on_button_clicked)
        vbox.pack_start(self.button, True, True, 0)
        
        #self.set_icon_from_file("web.png")
        self.set_border_width(10)
        self.set_title("Token")
        self.set_default_size(400, 300)
        self.connect("destroy", Gtk.main_quit)

    def on_button_clicked(self):
        sncf.append(self.entry.get_text())
        sncf.append(self.entry2.get_text())
        sncf.append(self.entry3.get_text())
        return sncf


win = EntryWindow()
win.show_all()
Gtk.main()
E = EntryWindow()

url = "https://www.digital.sncf.com/startup/api/token-developpeur"

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
driver.get(url)
wait = WebDriverWait(driver, 2)

while True:
    try:
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"]')))
        cookie = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"]')
        cookie.click()
    except TimeoutException:
        print("timed-out, retry in 1 sec")
        time.sleep(1)
        continue
    break

firstname = driver.find_element(By.XPATH, '//*[@id="edit-field-user-name-und-0-value"]')
firstname.send_keys(win.on_button_clicked()[0])

name = driver.find_element(By.XPATH, '//*[@id="edit-field-user-surname-und-0-value"]')
name.send_keys(win.on_button_clicked()[1])

name = driver.find_element(By.XPATH, '//*[@id="edit-field-api-email-und-0-email"]')
name.send_keys(win.on_button_clicked()[2])

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

check = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[6]/div/label')
check.click()


submit = driver.find_element(By.XPATH, '//*[@id="edit-submit"]')
submit.click()