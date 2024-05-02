import pathlib

import time
import zipfile

from selenium.webdriver.common.by import By
import random
from selenium import webdriver

from settings import *
from utils import read_account

account = read_account()
email = account.split('\t')[0]
password = account.split('\t')[1]

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


class Google:
    def __init__(self):
        self.driver = None
        self.create_driver()
        random.seed(time.time())

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--remote-debugging-port=9222")  # this
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        script_directory = pathlib.Path().absolute()
        chrome_options.add_argument(f"--user-data-dir={script_directory}\\chrome-data")

        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)

        self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.get('https://httpbin.org/ip')
        body = self.driver.find_element(By.TAG_NAME, "body")
        print(body.text)

    def swap_proxy(self):
        self.close()
        self.create_driver()

    def block_handle(self):
        self.swap_proxy()

    def process(self, search_keywords, ad_site):
        driver = self.driver
        driver.get("https://google.com")
        time.sleep(2)
        sign_in = driver.find_elements(By.XPATH, "//a[@aria-label='Sign in']")
        sign_in_2 = driver.find_elements(By.XPATH, "//a[contains(@href,'accounts.google.com/ServiceLogin')]")
        print(sign_in[0])
        sign_in[0].click()

        email_input = driver.find_elements(By.XPATH, "//input[@id='identifierId']")
        # email_input = driver.find_element_by_id('identifierId')
        # print(email_input[0])
        email_input[0].send_keys(email)

        next_div = driver.find_elements(By.XPATH, "//div[@id='identifierNext']")
        print(next_div)
        next_div[0].click()

        if (len(sign_in_2)+len(sign_in)) > 0:
            input("Please sign in and press enter here in the terminal: ")
        while True:
            try:
                driver.get("https://google.com")
                search_box = driver.find_element(By.TAG_NAME, "textarea")
                search_keyword = random.choice(search_keywords)
                search_box.send_keys(search_keyword)
                search_box.send_keys("\n")
                break
            except Exception as e:
                print(e)
                print("Unable to type into serach bar")
                print("Blocked by google")
                print("starting with new proxy")
                time.sleep(5)
                self.block_handle()
                driver = self.driver
        time.sleep(4)

        ad_links = []

        sponsered1 = driver.find_elements(By.XPATH, '//span[text()="Sponsored"]')
        print(f"Sponsered elements found {len(sponsered1)}")
        sponsered2 = driver.find_elements(By.XPATH, '//span[text()="Gesponsert"]')
        print(f"Gesponsert elements found {len(sponsered2)}")

        sponsered = sponsered1 + sponsered2

        for s in sponsered:
            s_up = s.find_element(By.XPATH, "./..")
            a_el = s_up.find_element(By.TAG_NAME, "a")
            ad_links.append(a_el)

        print(f"Total ad links obtained {len(ad_links)}")
        ad_found = None

        if ad_site is not None:
            for ad in ad_links:
                ad_up = ad.find_element(By.XPATH, "./..")
                print("---------------------------------------")
                print(ad_up.text)
                print("---------------------------------------")
                if ad_site in ad_up.text:
                    ad_found = ad
                    break
        else:
            if len(ad_links) == 0:
                ad_found = None
            else:
                ad_found = random.choice(ad_links)

        if ad_found is None:
            print("Target website's ad was not found")
            return

        ad_found.click()

        time.sleep(2)

        for _ in range(5):
            driver.execute_script("window.scrollBy(0, %s)" % random.randint(-1000, 10000))
            time.sleep(random.uniform(1, 2))

        driver.execute_script("window.history.go(-1)")
        time.sleep(random.uniform(1, 2))

    def close(self):
        self.driver.close()
        time.sleep(5)
