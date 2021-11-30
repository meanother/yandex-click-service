import os
import random
import re
import time
import traceback

import undetected_chromedriver.v2 as uc
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from src.utils import get_work_time, logger, ua_list


class Driver:
    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument("user-agent=%s" % random.choice(ua_list))
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--remote-debugging-port=9222")
        self.default_url = "https://yandex.ru/"
        self.chrome = None
        self.result_list = []
        self.action = None

    def _initialize(self) -> None:
        # self.chrome = uc.Chrome(options=self.options, version_main=86)
        self.chrome = uc.Chrome(options=self.options)
        self.chrome.implicitly_wait(120)
        time.sleep(2)

    @get_work_time
    def _quit_driver_and_reap_children(self) -> None:
        logger.warning("Quitting session: %s" % self.chrome.session_id)
        self.chrome.quit()
        try:
            pid = True
            while pid:
                pid = os.waitpid(-1, os.WNOHANG)
                logger.warning("Reaped child: %s" % str(pid))
        except ChildProcessError:
            pass

    def _close(self) -> None:
        try:
            logger.warning("Prepare to close driver")
            self.chrome.quit()
            # self._quit_driver_and_reap_children()
        except (InvalidSessionIdException, WebDriverException) as e:
            logger.error("closed driver was broken %s" % e)

    def _get_urls_from_main_page(self, search_query: str) -> str:
        self.chrome.get(self.default_url)
        time.sleep(2)
        self.chrome.find_element_by_xpath('//*[@id="text"]').send_keys(
            "%s\n" % search_query
        )
        logger.info("yandex search keyword is %s" % search_query)
        time.sleep(2.5)
        return self.chrome.page_source

    @staticmethod
    def _parse_data_from_main_page(html: str) -> list:
        temp_list = []
        tree = bs(html, "lxml")
        try:
            links = tree.find("div", class_="content__left").find("ul").find_all("li")
            for element in links:
                if (
                    element.get("data-cid") is not None
                    and element.find("div", class_="organic__url-text") is not None
                ):
                    temp_list.append(element)
        except Exception as e:
            logger.error(
                "Some error with parsing page %s" % (str(e) + traceback.format_exc())
            )
            with open("test.html", "w") as f:
                f.write(html)
        return temp_list

    @get_work_time
    def test_run(self, keywords) -> None:
        self._initialize()
        for query in keywords:
            data = self._get_urls_from_main_page(query)
            raw_array = self._parse_data_from_main_page(data)
            self.filter_lst(raw_array)
            time.sleep(3.5)
        self._close()

    def clean_only_yandex_yabs(self, lst: list):
        for item in lst:
            if "yabs.yandex.ru" in item.find("div").find("a").get("href"):
                url = item.find("div").find("a").get("href")
                self.result_list.append(url)
        self.result_list.append("https://finvestpaper.ru/main/statistics/")
        self.result_list.append("https://artydev.ru/")
        self.result_list.append("https://artydev.ru/posts/bankiru-analytics/")

    def filter_lst(self, lst: list):
        temp_list = [i for i in lst if "fl-bankrotstvo.ru" not in i.find("div").text]
        self.clean_only_yandex_yabs(temp_list)

    def move_cursor_with_driver(self, item):
        try:
            self.action.move_to_element(item).perform()
            time.sleep(0.15)
        except Exception as e:
            pass

    @staticmethod
    def scroll_page(html):
        html.send_keys(Keys.ESCAPE)
        for _ in range(40):
            html.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.05)
        for _ in range(6):
            html.send_keys(Keys.PAGE_UP)
            time.sleep(0.1)

    @staticmethod
    def get_domain(url: str):
        try:
            domain = re.search(
                r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]",
                url,
            )
            return domain.group()
        except Exception as e:
            logger.error(e)
            return "-"

    @get_work_time
    def imitation_actions(self, url: str):
        self.action = ActionChains(self.chrome)
        try:
            self.chrome.get(url)
            logger.info("Page title: %s" % self.chrome.title)
            logger.info("Page URL: %s" % self.get_domain(self.chrome.current_url))
            if (
                "yandex.ru/uslugi/" not in self.chrome.current_url
                and "docs.google.com/forms/" not in self.chrome.current_url
            ):
                if (
                    "403 Forbidden" not in self.chrome.page_source
                    and "502 Bad Gateway" not in self.chrome.page_source
                ):
                    page = self.chrome.find_element_by_tag_name("html")
                    page_elements = self.chrome.find_elements_by_css_selector(
                        "div[class]"
                    )

                    self.scroll_page(page)
                    random.shuffle(page_elements)
                    for element in page_elements[:15]:
                        self.move_cursor_with_driver(element)
        except InvalidSessionIdException as e:
            logger.error(
                f"cant get page info, pass it with ERROR: {str(e) + traceback.format_exc()}"
            )

    @get_work_time
    def run_imitation(self, urls: list):
        self._initialize()
        for url in urls:
            logger.info("Imitation actions in %s" % url)
            self.imitation_actions(url)
        self._close()
