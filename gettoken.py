#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from urllib3 import Retry
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
'''import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import Notify

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Token")
        Gtk.Window.set_default_size(self, 800, 500)
        Notify.init("Simple GTK3 Application")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")
        vbox.pack_start(self.entry, True, True, 0)
       
        self.button = Gtk.Button(label="Submit")
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_valign(Gtk.Align.CENTER)
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

    def on_button_clicked(self, widget):
        n = Notify.Notification.new("Simple GTK3 Application", "Hello World !!")
        n.show()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()'''

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
firstname.send_keys("John")

name = driver.find_element(By.XPATH, '//*[@id="edit-field-user-surname-und-0-value"]')
name.send_keys("Doe")

name = driver.find_element(By.XPATH, '//*[@id="edit-field-api-email-und-0-email"]')
name.send_keys("d2ave@gmx.de")

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

check = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[6]/div/label')
check.click()


submit = driver.find_element(By.XPATH, '//*[@id="edit-submit"]')
submit.click() 