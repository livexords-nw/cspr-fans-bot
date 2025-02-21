from datetime import datetime, timezone
import json
import time
from colorama import Fore
import requests
import random

class cspr_fans:
    BASE_URL = "https://api.cspr.fans/api/"
    HEADERS = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://cspr.fans",
        "referer": "https://cspr.fans/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.query_list = self.load_query()
        self.config = self.load_config()
        self.token = None

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 CSPR FANS Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
            print(Fore.LIGHTBLACK_EX + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |") + " " + color + message + Fore.RESET)

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Failed to parse config.json. Please check the file format.", Fore.RED)
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []
            
    def login(self, index: int) -> None:
        self.log("🔒 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        # Menggunakan endpoint 'users/me'
        req_url = f"{self.BASE_URL}users/me"
        token = self.query_list[index]
        self.token = token

        self.log(
            f"📋 Using token: {token[:10]}... (truncated for security)",
            Fore.CYAN,
        )

        # Header authorization langsung menggunakan token
        headers = {**self.HEADERS, "authorization": token}

        try:
            self.log("📡 Sending request to fetch user information...", Fore.CYAN)
            
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "user" in data:
                user_info = data["user"]
                username = user_info.get("username", "Unknown")
                user_id = user_info.get("id", "Unknown")
                telegram_uid = user_info.get("telegram_uid", "Unknown")
                joined_at = user_info.get("joined_at", "Unknown")
                onboarded = user_info.get("onboarded", "Unknown")

                self.log("✅ Login successful!", Fore.GREEN)
                self.log(f"👤 Username: {username}", Fore.LIGHTGREEN_EX)
                self.log(f"🆔 User ID: {user_id}", Fore.CYAN)
                self.log(f"📞 Telegram UID: {telegram_uid}", Fore.LIGHTYELLOW_EX)
                self.log(f"📅 Joined At: {joined_at}", Fore.LIGHTBLUE_EX)
                self.log(f"⏰ Onboarded: {onboarded}", Fore.LIGHTMAGENTA_EX)
            else:
                self.log("⚠️ Unexpected response structure.", Fore.YELLOW)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (possible JSON issue): {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

    def task(self) -> None:
        """
        Mengambil daftar tasks dari endpoint {self.BASE_URL}users/me/tasks,
        kemudian untuk setiap task yang belum diklaim, dilakukan:
        - Start task (action = 0)
        - Menunggu acak 20-25 detik
        - Claim task (action = 1)
        Lanjut ke task berikutnya.
        """
        req_url = f"{self.BASE_URL}users/me/tasks"
        headers = {**self.HEADERS, "authorization": self.token}

        self.log("📡 Fetching tasks...", Fore.CYAN)
        try:
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Pastikan data merupakan dictionary
            if not isinstance(data, dict):
                self.log(f"❌ Unexpected data format: expected dict, got {type(data)}", Fore.RED)
                return

            # Tampilkan informasi user (jika ada)
            user_data = data.get("user", {})
            username = user_data.get("username", "Unknown") if isinstance(user_data, dict) else "Unknown"
            self.log(f"👤 User: {username}", Fore.GREEN)

            # Ambil tasks dari objek "tasks"
            tasks_obj = data.get("tasks", {})
            if not isinstance(tasks_obj, dict):
                self.log("⚠️ Tasks format is not as expected.", Fore.YELLOW)
                return

            # Gabungkan semua kategori tasks ke dalam satu list: priority, daily, recruit
            all_tasks = []
            for category in ["daily", "recruit", "priority"]:
                tasks_list = tasks_obj.get(category, [])
                if isinstance(tasks_list, list):
                    for task_obj in tasks_list:
                        if isinstance(task_obj, dict):
                            # Tambahkan kategori ke task_obj agar bisa dilog
                            task_obj["category"] = category
                            all_tasks.append(task_obj)
                        else:
                            self.log(f"⚠️ Unexpected task format in {category} tasks: {task_obj}", Fore.YELLOW)

            if not all_tasks:
                self.log("⚠️ No tasks found.", Fore.YELLOW)
                return

            self.log(f"✅ Total tasks found: {len(all_tasks)}", Fore.GREEN)
            # Proses setiap task
            for task_obj in all_tasks:
                task_name = task_obj.get("task_name")
                if not task_name:
                    self.log("⚠️ Task without task_name found, skipping.", Fore.YELLOW)
                    continue

                # Jika task sudah diklaim, lewati
                if task_obj.get("claimed_at"):
                    self.log(f"ℹ️ Task '{task_name}' (category: {task_obj.get('category')}) already claimed, skipping.", Fore.CYAN)
                    continue

                # --- Start Task ---
                start_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
                payload_start = {
                    "task_name": task_name,
                    "action": 0,
                    "data": {"date": start_time}
                }
                try:
                    self.log(f"📡 Starting task '{task_name}' (category: {task_obj.get('category')})...", Fore.CYAN)
                    response_start = requests.post(req_url, json=payload_start, headers=headers)
                    response_start.raise_for_status()
                    self.log(f"✅ Task '{task_name}' started at {start_time}.", Fore.GREEN)
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to start task '{task_name}': {e}", Fore.RED)
                    self.log(f"📄 Response content: {response_start.text}", Fore.RED)
                    continue

                # Tunggu acak 20-25 detik
                wait_time = random.randint(20, 25)
                self.log(f"⏳ Waiting for {wait_time} seconds before claiming task '{task_name}'...", Fore.CYAN)
                time.sleep(wait_time)

                # --- Claim Task ---
                claim_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
                payload_claim = {
                    "task_name": task_name,
                    "action": 1,
                    "data": {"date": claim_time}
                }
                try:
                    self.log(f"📡 Claiming task '{task_name}' (category: {task_obj.get('category')})...", Fore.CYAN)
                    response_claim = requests.post(req_url, json=payload_claim, headers=headers)
                    response_claim.raise_for_status()
                    self.log(f"✅ Task '{task_name}' claimed at {claim_time}.", Fore.GREEN)
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to claim task '{task_name}': {e}", Fore.RED)
                    self.log(f"📄 Response content: {response_claim.text}", Fore.RED)
                    continue

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch tasks: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error while processing tasks: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
    
    def spin(self) -> None:
        """
        Melakukan proses spin dengan tiga langkah:
        1. Mengambil season calendar (GET ke users/me/season-calendar)
            - Contoh respon: {"data": [1, 0, "spin"]}
        2. Mengambil detail spin (GET ke users/me/season-calendar/spin)
            - Contoh respon:
            {
                "data": [
                1,
                "#880044",
                [ "100", 1, 0, "2", 3, 1, "500", 2, 0, "300", 1, 0, "200", 1, 0, "3", 3, 1, "200", 1, 0, "300", 1, 0 ],
                322,
                3000,
                1,
                "652424744-361369927"
                ]
            }
            - Ambil spin_id dari elemen terakhir (indeks ke-6).
        3. Melakukan spin (POST ke users/me/season-calendar/spin)
            - Payload: [spin_id]
            - Contoh respon: {"data":[[{"unit":"point","balance":650}]]}
        """
        # Langkah 1: Ambil season calendar
        self.log("📡 Fetching season calendar...", Fore.CYAN)
        url_calendar = f"{self.BASE_URL}users/me/season-calendar"
        headers = {**self.HEADERS, "authorization": self.token}

        try:
            response_calendar = requests.get(url_calendar, headers=headers)
            response_calendar.raise_for_status()
            data_calendar = response_calendar.json()
            self.log(f"✅ Season calendar data: {data_calendar}", Fore.GREEN)

            # Langkah 2: Ambil detail spin
            url_spin = f"{self.BASE_URL}users/me/season-calendar/spin"
            self.log("📡 Fetching spin details...", Fore.CYAN)
            response_spin = requests.get(url_spin, headers=headers)
            response_spin.raise_for_status()
            data_spin = response_spin.json()
            self.log(f"✅ Spin details: {data_spin}", Fore.GREEN)

            # Pastikan struktur data sesuai, ambil spin_id dari elemen ke-7 (indeks 6)
            spin_data = data_spin.get("data")
            if not spin_data or len(spin_data) < 7:
                self.log("❌ Unexpected spin details structure.", Fore.RED)
                return
            spin_id = spin_data[6]
            self.log(f"🔑 Spin ID extracted: {spin_id}", Fore.CYAN)

            # Langkah 3: Eksekusi spin dengan POST
            payload = [spin_id]
            self.log(f"📡 Executing spin with payload: {payload}", Fore.CYAN)
            response_post = requests.post(url_spin, json=payload, headers=headers)
            response_post.raise_for_status()
            data_post = response_post.json()
            self.log(f"✅ Spin result: {data_post}", Fore.GREEN)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Spin process failed: {e}", Fore.RED)
            if hasattr(e, 'response') and e.response is not None:
                self.log(f"📄 Response content: {e.response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error during spin process: {e}", Fore.RED)

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.
        
        Args:
            filename (str): The path to the proxy file.
        
        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.
        
        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").
        
        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN)
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)
        
        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session
    
    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

if __name__ == "__main__":
    csp = cspr_fans()
    index = 0
    max_index = len(csp.query_list)
    config = csp.load_config()
    if config.get("proxy", False):
        proxies = csp.load_proxies()


    csp.log("🎉 [LIVEXORDS] === Welcome to CSPR FANS Automation === [LIVEXORDS]", Fore.YELLOW)
    csp.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = csp.query_list[index]
        display_account = current_account[:10] + "..." if len(current_account) > 10 else current_account

        csp.log(f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}", Fore.YELLOW)

        if config.get("proxy", False):
            csp.override_requests()
        else:
            csp.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

        csp.login(index)

        csp.log("🛠️ Starting task execution...")
        tasks = {
            "task": "📝 Auto solve task",
            "spin": "🎰 Auto spin daily",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            csp.log(f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}", Fore.YELLOW if task_status else Fore.RED)

            if task_status:
                csp.log(f"🔄 Executing {task_name}...")
                getattr(csp, task_key)()

        if index == max_index - 1:
            csp.log("🔁 All accounts processed. Restarting loop.")
            csp.log(f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting.")
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            csp.log(f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds.")
            time.sleep(config.get("delay_account_switch", 10))
            index += 1