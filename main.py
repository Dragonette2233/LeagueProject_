import tkinter as tk
import tkinter.messagebox
import gc
import datetime
from time import sleep as cooldown
from os.path import exists
from os import remove
from re import findall as search_all
from re import match
from requests import get as get_
from requests import ConnectionError
from pygame import mixer as song
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import getChampionNameByID as lolconvert
from spectator import bats

# from win32process import CREATE_NO_WINDOW


song.init()
running = True
tk.messagebox.Message(master=None)
Regions = {'br': 'br1', 'tr': 'tr1', 'euw': 'euw1', 'jp': 'jp1', 'na': 'na1',
           'eune': 'eun1', 'oce': 'oc1', 'las': 'la2', 'lan': 'la1', 'ru': 'ru', 'kr': 'kr'}


def run():
    with open('key_song\\key.txt', 'r') as file_k:
        api_k = file_k.readline()

    def convert_classic_entry():

        if len(classic_entry.get()) > 2:
            for r in lolconvert.all_champion_id.values():
                if match(classic_entry.get().lower(), r.lower()):
                    converted_champion = r.lower()
                    if converted_champion == 'wukong':
                        converted_champion = 'monkeyking'
                    print(converted_champion)
                    classic_parser(converted_champion)
                    break
            else:
                featured_label['fg'] = 'white'
                featured_label['bg'] = 'orange'
                featured_label['text'] = 'who?'
        else:
            featured_label['fg'] = 'white'
            featured_label['bg'] = 'red'
            featured_label['text'] = 'Short'

    def classic_parser(converted_champion):

        URL = f"https://porofessor.gg/current-games/{converted_champion}"

        if exists('key_song\\Matches_1.txt'):
            remove('key_song\\Matches_1.txt')

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(
            service=Service("C:\\Program Files\\Google\\Chrome\\driver\\chromedriver.exe"),
            options=options,
            service_log_path='NUL'

        )

        driver.get(url=URL)
        driver.find_elements(by=By.XPATH, value='/html/body/main/div[2]/ul')
        soup = bs(driver.page_source, 'html.parser')
        cooldown(2.5)
        driver.close()

        all_matches = soup.find("ul", class_='cards-list currentGamesGrid no-margin-top').find_all('li')
        for p in range(0, len(all_matches)):
            if p in [0, 1, 2, 4] or all_matches[p].find('span').text:
                region_ = str(all_matches[p].find('a', class_='liveGameLink').get('href')).split('/')

                time_ = all_matches[p].find('span').text

                left_t = all_matches[p].find_all("div", class_='cardTeam')[0].find_all("div",
                                                                                       class_='participant '
                                                                                              'img-align-block'
                                                                                              '-right')
                teams_list = []
                for t in range(0, len(left_t)):
                    left_chars = left_t[t].find("a", class_='liveGameLink').find("img").get('title')
                    teams_list.append(left_chars)

                nick = left_t[0].find("div", class_='name').text.strip()
                elo = left_t[0].find("div", class_='subname').text.strip()

                elo_short = elo[0] + elo[1]

                with open('key_song\\Matches_1.txt', 'a+', encoding='utf8') as file_x:
                    file_x.writelines(
                        f"{elo_short.upper()}-|-{' | '.join(item for item in teams_list)} {time_}-|-"
                        f"{nick}:{(region_[2].strip()).upper()}\n")

        featured_label['text'] = "Done"
        featured_label['bg'] = 'Green'
        featured_label['fg'] = 'white'

        try:
            del URL, options, driver, soup, all_matches, region_, time_, left_t, teams_list, nick
        except UnboundLocalError:
            pass

    def parse_into_excel(team, nick, k):

        if k in ['TR1', 'BR1', 'NA1', 'RU', 'EUW1', 'JP1', 'KR']:
            k = k.replace('1', '')
        elif k in ['OC1', 'EUN1']:
            k = k.replace('1', 'E')
        elif k == "LA1":
            k = k.replace('1', 'N')
        else:
            k = k.replace('2', 'S')

        my_file = open("key_song\\Matches_1.txt", "a+", encoding='utf8')
        my_file.writelines(f"{team}-|-{nick}:{k}\n")
        my_file.close()

        del team, nick, k

    def aram_parser():

        if exists('key_song\\Matches_1.txt'):
            remove('key_song\\Matches_1.txt')

        for r in Regions.values():
            response = get_(f"https://{r}.api.riotgames.com/lol/spectator/v4/featured-games?api_key={api_k}").json()

            if 'gameList' in response.keys() and len(response['gameList']) > 2:
                for s in range(0, 5):
                    champ_dict = []
                    for k in range(0, 5):
                        id_name = int(response['gameList'][s]['participants'][k]['championId'])
                        convert_to_name = format(lolconvert.get_champions_name(id_name))
                        champ_dict.append(convert_to_name)

                    champ_dict = ' | '.join([str(item) for item in champ_dict])
                    parse_into_excel(champ_dict,
                                     str(response['gameList'][s]['participants'][0]['summonerName']),
                                     str(response['gameList'][s]['platformId']))

            else:
                continue

        featured_label['text'] = 'Done'
        featured_label['bg'] = 'Green'
        featured_label['fg'] = 'White'

    def test_xlsx():

        def button_create(btn_, champion_, name_, y_value):
            btn_['command'] = lambda: [copy_to_entry(name_), buttons_destroying()]
            btn_['bg'] = 'blue'
            btn_['text'] = champion_
            btn_['fg'] = 'white'
            btn_['font'] = ('Calibri', 9)
            btn_['borderwidth'] = 1
            btn_['relief'] = 'ridge'
            btn_.place(x=300, y=y_value)

        def copy_to_entry(name_reg):

            summoner_region_entry.insert(0, name_reg)

        def elo_parameters(elo_pl, elo_rank):

            """Label параметры ранга в лиге"""
            elo_pl['text'] = elo_rank
            elo_pl['fg'] = lolconvert.get_fg_elo(elo_rank)
            elo_pl['bg'] = lolconvert.get_bg_elo(elo_rank)
            elo_pl['width'], elo_pl['height'] = 3, 1
            elo_pl['font'], elo_pl['relief'] = ('Arial', 20, 'bold'), 'ridge'
            elo_pl.place(x=13, y=260)

            buttons_destroying()

        def buttons_destroying():

            try:
                '''btn_1.destroy()
                btn_2.destroy()
                btn_3.destroy()
                btn_4.destroy()
                btn_5.destroy()
                btn_6.destroy()'''
                btn_1.place_forget()
                btn_2.place_forget()
                btn_3.place_forget()
                btn_4.place_forget()
                btn_5.place_forget()
                btn_6.place_forget()
            except NameError:
                pass

        with open("key_song\\Matches_1.txt", 'r', encoding='utf8') as file_r:
            wb = set(file_r.readlines())

        champion_list = []
        names_list = []
        elo_list = []

        for s in wb:

            if search_all(f"{str.capitalize(champion_entry.get())}", s):
                try:
                    s = s.split('-|-')  # массив из персов и ника
                    if len(s) == 2:
                        champion_list.append(s[0])
                        names_list.append(s[1].strip())
                    else:
                        elo_list.append(s[0])
                        champion_list.append(s[1])
                        names_list.append(s[2].strip())

                except IndexError:
                    pass

        if len(names_list) in [1, 2, 3, 4, 5, 6]:

            try:

                button_create(btn_1, champion_list[0], names_list[0], 145)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_1 = tk.Label(root)
                    btn_1['command'] = lambda: [copy_to_entry(names_list[0]), elo_parameters(elo_label_1, elo_list[0])]


                button_create(btn_2, champion_list[1], names_list[1], 170)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_2 = tk.Label(root)
                    btn_2['command'] = lambda: [copy_to_entry(names_list[1]), elo_parameters(elo_label_2, elo_list[1])]


                button_create(btn_3, champion_list[2], names_list[2], 195)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_3 = tk.Label(root)
                    btn_3['command'] = lambda: [copy_to_entry(names_list[2]), elo_parameters(elo_label_3, elo_list[2])]


                button_create(btn_4, champion_list[3], names_list[3], 220)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_4 = tk.Label(root)
                    btn_4['command'] = lambda: [copy_to_entry(names_list[3]), elo_parameters(elo_label_4, elo_list[3])]


                button_create(btn_5, champion_list[4], names_list[4], 245)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_5 = tk.Label(root)
                    btn_5['command'] = lambda: [copy_to_entry(names_list[4]), elo_parameters(elo_label_5, elo_list[4])]


                button_create(btn_6, champion_list[5], names_list[5], 270)

                if len(elo_list) in [1, 2, 3, 4, 5, 6]:
                    elo_label_6 = tk.Label(root)
                    btn_6['command'] = lambda: [copy_to_entry(names_list[5]), elo_parameters(elo_label_6, elo_list[5])]
            except IndexError:
                pass
        elif len(names_list) > 6:
            tk.messagebox.showinfo(title='Error', message='Try another character')

        # del champion_list, names_list, elo_list

    def request_end_game():
        # temp values for testing
        # global_region, i, request_id = 'europe', 'euw1', '5942324637'

        check_state = get_(f"https://{global_region}.api.riotgames.com/lol/match/v5/matches/"
                           f"{i.upper()}_{request_id}?api_key={api_k}")

        if check_state == 403:
            api_check_on_start()

        elif check_state.status_code == 200:
            response = check_state.json()

            state_lable['bg'] = 'grey'
            state_lable['fg'] = 'white'
            spec_btn['state'] = 'disabled'
            game_state.destroy()

            kills = 0

            for k in range(0, 10):
                kills += int(response['info']['participants'][k]['kills'])

            time_stamp = list(divmod(response['info']['gameDuration'], 60))

            song.music.play(0)
            if time_stamp[1] < 10:
                time_stamp[1] = f"0{time_stamp[1]}"

            state_lable['text'] = f"Time {time_stamp[0]}:{time_stamp[1]}"

            win_label = tk.Label(root, fg='white', font=('Arial', 24, 'bold'), relief='ridge', width=14, height=3)

            if response['info']['teams'][0]['win']:
                win_label['text'] = f"BLUE SIDE (П1)\n-----Kills-----\n{kills} "
                win_label['bg'] = 'blue'
            else:
                win_label['text'] = f"RED SIDE (П2)\n-----Kills-----\n{kills} "
                win_label['bg'] = 'red'

            win_label.place(x=171, y=105)

        else:

            state_lable.after(1500, lambda: [active_state_change(), request_end_game()])

    def show_active(reg_show, response_json2):
        reg_lable = tk.Label(root)
        gamemode_lable = tk.Label(root)

        names = []
        for p in range(0, 5):
            id_champ = int(response_json2['participants'][p]['championId'])
            champ_name = format(lolconvert.get_champions_name(id_champ))
            names.append(champ_name)

        reg_lable['text'] = reg_show
        reg_lable['bg'] = 'grey'
        reg_lable['fg'] = 'yellow'
        reg_lable['font'] = ('Arial', 9, 'bold')
        reg_lable.place(x=53, y=198)

        gamemode_lable['text'] = response_json2['gameMode']
        gamemode_lable['font'] = ('Calibri', 8, 'bold')
        gamemode_lable['bg'] = 'grey'
        gamemode_lable['fg'] = 'white'
        gamemode_lable.place(x=90, y=162)
        y_val = 223
        for inf in range(0, 5):
            tk.Label(root,
                     text=f"|  {names[inf]}  |",
                     font=('Arial', 8, 'bold'),
                     bg='blue', fg='yellow').place(x=76, y=y_val)
            y_val += 21

    def main_parser():

        global global_region, i, request_id

        try:
            summoner_name = (summoner_region_entry.get()).split(':')

            i = Regions.get(summoner_name[1].lower())

            try:
                '''Запрос на игрока по нику'''
                response_json = (get_(f"https://{i}.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
                                      f"{summoner_name[0]}?api_key={api_k}")).json()
                '''Запрос активной игры'''
                response_json2 = (
                    get_(f"https://{i}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
                         f"{response_json['id']}?api_key={api_k}")).json()

                request_id = str(response_json2['gameId'])
                show_active(summoner_name[1].upper(), response_json2)

                if i in ["tr1", "ru", "eun1", "euw1"]:
                    global_region = "europe"
                elif i in ["jp1", "kr"]:
                    global_region = "asia"
                elif i in ["br1", "la1", "la2", "oc1", "na1"]:
                    global_region = "americas"

                port = summoner_name[1].lower()
                i = i.upper()

                run_btn.place(x=210, y=270)
                spec_btn['command'] = lambda: [bats(port, response_json2, request_id, i)]
                spec_btn.place(x=210, y=220)

            except KeyError:
                tk.messagebox.showerror(title='Error', message='Check region or nickname and try again\n'
                                                               '* or may be game has been finished')
            except ConnectionError:
                tk.messagebox.showerror(title='Error', message='Wrong region typing. Available regions:\n'
                                                               'BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR')
        except IndexError:
            tk.messagebox.showerror(title='Error', message='Wrong typing name and region. Use ":" between its')

    '''Функции для работы с лейблами'''

    def classic_label_changing():

        featured_label['bg'] = 'Yellow'
        featured_label['fg'] = 'Black'
        featured_label['text'] = 'Wait'
        featured_label['font'] = ('Calibri', 10)
        featured_label.place(x=560, y=61)
        featured_label.after(1, convert_classic_entry)

    def aram_label_changing():

        featured_label['bg'] = 'Yellow'
        featured_label['fg'] = 'Black'
        featured_label['text'] = 'Wait'
        featured_label['font'] = ('Calibri', 10)
        featured_label.place(x=560, y=86)
        featured_label.after(1, aram_parser)

    def labels_state_changing():

        run_btn['state'] = 'disabled'
        game_state['fg'] = 'white'
        game_state['bg'] = 'grey'
        game_state['text'] = f"GameID: {i.upper()}_{request_id}"
        game_state.place(x=320, y=300)

        state_lable['text'] = 'Active'
        state_lable['bg'] = 'yellow'
        state_lable['fg'] = 'black'

    def active_state_change():

        if state_lable['bg'] == 'yellow':
            state_lable['bg'] = 'green'
            state_lable['fg'] = 'white'
        else:
            state_lable['bg'] = 'yellow'
            state_lable['fg'] = 'black'

    def reload():
        global running
        running = True
        root.destroy()

    def refresh():
        classic_entry.delete(0, 'end')
        champion_entry.delete(0, 'end')
        summoner_region_entry.delete(0, 'end')
        btn_1.place_forget()
        btn_2.place_forget()
        btn_3.place_forget()
        btn_4.place_forget()
        btn_5.place_forget()
        btn_6.place_forget()
        
    def api_label_black():

        api_label['bg'] = 'black'

    def api_label_green():

        api_label['bg'] = 'green'
        api_label.after(150, api_label_black)

    root = tk.Tk()
    root.title('League MCF')
    icon = tk.PhotoImage(file='ap_packs\\icon_f.png')

    kindred_image = tk.PhotoImage(file='ap_packs\\pg4.png')
    kindred_lable = tk.Label(root, image=kindred_image)
    width = 600
    height = 330
    root.geometry(f"{width}x{height}+300+400")
    root.resizable(False, False)
    root.iconphoto(False, icon)
    kindred_lable.place(x=0, y=0, relwidth=1, relheight=1)

    '''Entry для ввода ника и региона'''
    summoner_region_entry = tk.Entry(root)
    summoner_region_entry.place(x=90, y=99)

    '''Entry для поиска нормал / ранкед по персу'''
    classic_entry = tk.Entry(root, width=9)
    classic_entry.place(x=445, y=62)

    '''Entry для поиска игры по Matches_1.txt'''
    champion_entry = tk.Entry(root, width=12)
    champion_entry.place(x=470, y=112)

    '''Label который показывает зеленым Done'''
    featured_label = tk.Label(root)

    '''Labels для состояния'''
    state_lable = tk.Label(root, text='Inactive', fg='white', bg='red', font=('Arial', 9, 'bold'))
    state_lable.place(x=510, y=300)

    game_state = tk.Label(root, font=('Arial', 9, 'bold'))

    '''Label действия API ключа'''
    api_expiring = open('ap_packs\\time_expiring.txt', 'r')
    api_label = tk.Label(root, text=api_expiring.readline(), bg='black', fg='white', relief='ridge')
    api_label.place(x=235, y=1)

    '''Все кнопки'''

    # tk.Button(root, text='Reload', bg='green', fg='white', command=reload).place(x=270, y=30)
    tk.Button(root, text='Search', command=lambda: [main_parser(), summoner_region_entry.delete(0, 'end')]).place(x=90,
                                                                                                                  y=120)
    '''Получить игры summnoers rift'''
    tk.Button(root, text='Get', width=5, command=classic_label_changing).place(x=515, y=60)
    '''Получить ARAM игры'''
    tk.Button(root, text='Get', width=5, command=aram_label_changing).place(x=515, y=86)
    run_btn = tk.Button(root, text='Run', width=7, height=2, bg='grey', command=lambda: [labels_state_changing(),
                                                                                      request_end_game()])
    '''Кнопки найденных игр'''
    btn_1 = tk.Button(root)
    btn_2 = tk.Button(root)
    btn_3 = tk.Button(root)
    btn_4 = tk.Button(root)
    btn_5 = tk.Button(root)
    btn_6 = tk.Button(root)
    # run_btn.place(x=210, y=270)

    spec_btn = tk.Button(root, text='Spectate', width=7, height=2)
    tk.Button(root, text='Show', command=test_xlsx).place(x=560, y=110)


    '''Menu ПКМ'''

    menu_rmc = tk.Menu(tearoff=0)
    menu_rmc.add_command(label='Reload', command=reload)
    # menu_rmc.add_command(label='Refresh', command=refresh)
    menu_rmc.add_command(label='Update API', command=lambda: [api_check_on_start(), api_label_green()])

    root.bind("<Button 3>", lambda event: menu_rmc.post(event.x_root, event.y_root))

    root.mainloop()


def set_api(key_set):
    with open('key_song\\key.txt', 'w+') as file_0:
        file_0.write(key_set)
        file_0.close()

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    timefile = open("ap_packs\\time_expiring.txt", "w+", encoding="utf-8")
    if datetime.datetime.now().minute < 10:
        timefile.writelines(
            tomorrow.strftime(f'API term %d.%m | {datetime.datetime.now().hour}:0{datetime.datetime.now().minute}'))
    else:
        timefile.writelines(
            tomorrow.strftime(f'API term %d.%m | {datetime.datetime.now().hour}:{datetime.datetime.now().minute}'))
    timefile.close()

    api_status = True
    while api_status:
        check_status = get_(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
                            f"MyLoveIsAfterYou?api_key={key_set}").status_code
        if check_status == 200:
            api_status = False
            tk.messagebox.showinfo(title='API info', message="API updated. Press 'Reload'")


def api_check_on_start():
    try:
        a_key = (open('key_song\\key.txt', 'r')).readline()
        song.music.load("key_song\\song.mp3")
        check_api = get_(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
                         f"MyLoveIsAfterYou?api_key={a_key}").status_code
        if check_api in [403, 401]:
            api_tk = tk.Tk()
            api_tk.title('Last API-key expired. Provide new API')
            tk.Label(api_tk, bg='black').place(x=0, y=0, relwidth=1, relheight=1)
            api_tk.geometry('500x100+300+400')
            api_tk.resizable(False, False)
            api_entry = tk.Entry(api_tk, width=60)
            api_entry.place(relx=0.14, rely=0.4)
            api_btn = tk.Button(api_tk, text='SET', width=20)
            api_btn['command'] = lambda: [set_api((api_entry.get()).strip()),
                                          api_tk.destroy()]
            api_btn.place(relx=0.38, rely=0.7)
            api_entry.mainloop()

    except FileNotFoundError:
        tk.messagebox.showerror(title='Error', message='api.txt not found. Create api.txt with valid API key')

    except RuntimeError:
        tk.messagebox.showerror(title='Error',
                                message='song.mp3 not defined. Copy song.mp3 in ap_packs folder and restart program')


api_check_on_start()

while running:
    running = False
    run()
    gc.collect()
