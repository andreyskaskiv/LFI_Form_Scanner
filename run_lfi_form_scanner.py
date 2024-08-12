import asyncio
import os
import threading
import urllib.parse as urlparse
from itertools import product
from random import choice
from typing import List, Tuple, Set

import aiohttp
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

from handlers.check_type import check_type
from handlers.file_handler import read_data_from_file, write_target_links
from handlers.utils import setup_logger
from handlers.write_target import Writer

headers = {
    'User-Agent': choice(list(map(str.rstrip, open("_user_agent_pc.txt").readlines()))),
    'Accept': 'text/html,application/xhtml',
}

files = ["PAYLOADS_LFI.txt", "PAYLOADS_ANSWERS_LFI.txt"]
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))

data = {
    name: set(map(str.rstrip, open(os.path.join(project_root, "wordlist", name), 'r', encoding='utf-8')))
    for name in files
}
PAYLOADS, ANSWERS = data["PAYLOADS_LFI.txt"], data["PAYLOADS_ANSWERS_LFI.txt"]

MAX_RETRIES = 2  # повтора неудачных запросов с задержкой между попытками
RETRY_DELAY = 2  # seconds


async def test_command_execution_in_form(self, form: str, url: str, max_concurrent_requests: int) -> List[
    Tuple[bool, str]]:
    results = []
    total_requests = len(ANSWERS) * len(PAYLOADS)
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def bounded_submit_form(payload: str, answer: str):
        async with semaphore:
            for attempt in range(MAX_RETRIES):
                try:
                    async with aiohttp.ClientSession() as session:
                        return await self.submit_form_async(session, form, payload, url, answer)
                except asyncio.TimeoutError:
                    print(f"{Fore.RED}TimeoutError for payload: {payload}{Style.RESET_ALL}")
                except aiohttp.ClientError as e:
                    print(f"{Fore.RED}ClientError: {e} for payload: {payload}{Style.RESET_ALL}")
                await asyncio.sleep(RETRY_DELAY)
            return (False, payload)

    tasks = [bounded_submit_form(payload, answer) for answer, payload in product(ANSWERS, PAYLOADS)]

    completed_tasks = 0
    for future in asyncio.as_completed(tasks):
        result = await future
        if result[0]:
            results.append((True, result[1]))
        completed_tasks += 1
        print(
            f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}\rProgress: {completed_tasks}/{total_requests} requests completed{Style.RESET_ALL}",
            end='')

    print()
    return results


class Scanner:
    def __init__(self, submit_form_post: str, verbose: str):
        self.logger = setup_logger()
        self.session = requests.Session()
        self.submit_form_post = submit_form_post
        self.verbose = verbose
        self.target_links_COMMAND = []
        self.target_forms_COMMAND = []
        self.all_forms = []
        self.target_forms_not_vulnerable = []
        self.file_lock = threading.Lock()

    def extract_forms(self, url: str):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content, features='lxml')
        return parsed_html.findAll("form")

    async def submit_form_async(self, session, form, value: str, url: str, answer: str) -> Tuple[bool, str]:
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")

        inputs_list = form.findAll("input")

        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")

            if input_type in {"text", "TEXT", None}:
                input_value = value

            if input_name:
                post_data[input_name] = input_value

        post_data = {k: v for k, v in post_data.items() if v is not None}

        if method == 'post' and check_type(self.submit_form_post):
            if check_type(self.verbose):
                print(f" \n====> POST_url: {post_url} | post_data: {post_data}")
            async with session.post(post_url, data=post_data) as response:
                text = await response.text(errors="ignore")
                return (answer in text, value)

        if check_type(self.verbose):
            print(f" \n====> GET_url: {post_url} | GET_data: {post_data}")
        async with session.get(post_url, params=post_data) as response:
            text = await response.text(errors="ignore")
            return (answer in text, value)

    async def run_scanner_async(self, case: Set[str], links_to_crawler, max_concurrent_requests: int):
        target_links = links_to_crawler
        total_links = len(target_links)

        for link_number, link in enumerate(target_links):

            forms = self.extract_forms(link)
            total_forms = len(forms)

            for form_number, form in enumerate(forms):
                if not any(form == existing_form for _, existing_form in self.all_forms):
                    self.all_forms.append((link, form))

                if "command_in_form" in case:
                    print(
                        f"[{link_number + 1}/{total_links}] COMMAND Testing Form [{form_number + 1}/{total_forms}] in: {link}")
                    is_vulnerable_to_command_exec = await test_command_execution_in_form(self, form=form, url=link,
                                                                                         max_concurrent_requests=max_concurrent_requests)
                    if any(result[0] for result in is_vulnerable_to_command_exec):
                        self.target_forms_COMMAND.append((link, form, is_vulnerable_to_command_exec))
                        self.logger.warning(f"\n[+] 💉 Discovered in: {link}\n"
                                            f"{form}\n{'-' * 80}\n"
                                            f"[***] 💉 Payload:{is_vulnerable_to_command_exec}\n{'=' * 80}\n\n")

        target_forms_COMMAND_set = set(form for _, form, _ in self.target_forms_COMMAND)

        for link, form in self.all_forms:
            if (form not in target_forms_COMMAND_set):
                self.target_forms_not_vulnerable.append((link, form))

    def run_scanner(self, case: Set[str], links_to_crawler, max_concurrent_requests: int):
        asyncio.run(self.run_scanner_async(case, links_to_crawler, max_concurrent_requests))

    def get_all_lists(self):
        return {
            "target_forms_COMMAND": self.target_forms_COMMAND,
            "target_forms_not_vulnerable": self.target_forms_not_vulnerable,
        }

    def write_link_to_file(self, link: str, category: str):
        with self.file_lock:
            if category == "links":
                write_target_links("LINKS_success", link)


def run_scanner(case, path_to_links_to_crawler, submit_form_post, verbose, max_concurrent_requests):
    links_to_crawler = sorted(set(read_data_from_file(path_to_links_to_crawler)))
    vulnerability_scanner = Scanner(submit_form_post, verbose)

    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}\nVulnerability Scanner Starts 🧐 ==> {Style.RESET_ALL}\n")
    vulnerability_scanner.run_scanner(case=case,
                                      links_to_crawler=links_to_crawler,
                                      max_concurrent_requests=max_concurrent_requests)

    all_lists = vulnerability_scanner.get_all_lists()
    writer = Writer(all_lists)
    writer.write_target_success()


if __name__ == '__main__':
    run_scanner(case={'command_in_form'},
                path_to_links_to_crawler="input_data/LINKS_TO_CRAWLER.txt",
                submit_form_post="Y",
                verbose="N",
                max_concurrent_requests=20)
