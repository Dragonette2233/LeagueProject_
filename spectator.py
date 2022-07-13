from os import remove, startfile, popen
from os.path import exists
import re

ports_dict = {'euw': 'euw1', 'jp': 'jp1', 'na': 'na1',
              'oce': 'oc1', 'eune': 'eu', 'las': 'la2',
              'lan': 'la1', 'tr': 'tr', 'ru': 'ru',
              'kr': 'kr', 'br': 'br'}


# re.findall('League of Legends', subprocess.getoutput('tasklist')) == ['League of Legends']
# re.findall('League of', os.popen('tasklist').read()) == ['League of Legends']

def bats(port, response_json2, request_id, i):
    if re.findall('League of Legends', popen('tasklist').read()) == ['League of Legends']:

        print('Game running. Stop it now')

    else:
        if exists('ap_packs\\spectate.bat'):
            remove('ap_packs\\spectate.bat')

        port = ports_dict.get(port)
        print(port)

        '''if port == 'euw' or port == 'jp' or port == 'na':
            port = str(port + '1')
        elif port == 'oce':
            port = str(port[:(len(port) - 1)] + '1')
        elif port == 'eune':
            port = 'eu'
        elif port == 'las':
            port = str(port.replace('s', '2'))
        elif port == 'lan':
            port = str(port.replace('n', '1'))'''

        spectate = open('spectate.bat', 'w', encoding='utf-8')
        spectate.write(f'''@echo off
        setlocal enabledelayedexpansion

        :start
        set LOL_PATH=""

        if exist "%APPDATA%\LoG_lolinstallpath.txt" (
            set /p LOL_PATH0=< "%APPDATA%\LoG_lolinstallpath.txt"
            call :Trim LOL_PATH !LOL_PATH0!
            echo Manually set Path found: "!LOL_PATH!"

            IF EXIST "!LOL_PATH!" (
                goto runSpectate
            )
        )

        for /F "delims=" %%R in ('
            tasklist /FI "ImageName eq LeagueClient.exe" /FI "Status eq Running" /FO CSV /NH
        ') do (
            set "FLAG1=" & set "FLAG2="
            for %%C in (%%R) do (
                if defined FLAG1 (
                    if not defined FLAG2 (
                        set LOL_PID=%%~C
                        IF NOT "%LOL_PID%"=="" goto pidFound
                    )
                    set "FLAG2=#"
                )
                set "FLAG1=#"
            )
        )

        FOR %%G IN ("HKLM\SOFTWARE\WOW6432Node\Riot Games, Inc\League of Legends") DO (
        	for /f "usebackq skip=2 tokens=1,2*" %%a in (`%systemroot%\system32\REG.EXE QUERY %%G /v "Location"`) do  (
        		set LOL_PATH=%%c
        		echo "Path found: !LOL_PATH!
        		goto runSpectate
        	)
        )

        IF EXIST "E:\Riot Games\League of Legends" (
        	set LOL_PATH="E:\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "D:\Riot Games\League of Legends" (
        	set LOL_PATH="D:\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "C:\Program Files\Riot Games\League of Legends" (
        	set LOL_PATH="C:\Program Files\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "C:\Program Files (x86)\Riot Games\League of Legends" (
        	set LOL_PATH="C:\Program Files (x86)\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "C:\Program Files\League of Legends" (
        	set LOL_PATH="C:\Program Files\League of Legends"
        	goto runSpectate
        )
        IF EXIST "C:\Program Files (x86)\League of Legends" (
        	set LOL_PATH="C:\Program Files (x86)\League of Legends"
        	goto runSpectate
        )
        IF EXIST "D:\Program Files\Riot Games\League of Legends" (
        	set LOL_PATH="D:\Program Files\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "D:\Program Files (x86)\Riot Games\League of Legends" (
        	set LOL_PATH="D:\Program Files (x86)\Riot Games\League of Legends"
        	goto runSpectate
        )
        IF EXIST "D:\Program Files\League of Legends" (
        	set LOL_PATH="D:\Program Files\League of Legends"
        	goto runSpectate
        )
        IF EXIST "D:\Program Files (x86)\League of Legends" (
        	set LOL_PATH="D:\Program Files (x86)\League of Legends"
        	goto runSpectate
        )
        IF EXIST "E:\Riot Games\League of Legends" (
        	set LOL_PATH="E:\Riot Games\League of Legends"
        	goto runSpectate
        )

        goto notfound

        :pidFound
        set "lcpath="
        for /f "skip=1delims=" %%a in (
        	'wmic process where "ProcessID=%LOL_PID%" get ExecutablePath'
        ) do if not defined lcpath set "lcpath=%%a"

        For %%A in ("%lcpath%") do (
            Set LOL_PATH=%%~dpA
        )

        goto runSpectate

        :runSpectate
        cls
        for /f "tokens=* delims= " %%a in ("%LOL_PATH%") do set LOL_PATH=%%a
        for /l %%a in (1,1,100) do if "!LOL_PATH:~-1!"==" " set LOL_PATH=!LOL_PATH:~0,-1!
        cd /D %LOL_PATH%

        for /f "tokens=1,* delims=" %%i in ('type Config\LeagueClientSettings.yaml ^| find /i "locale:"') do (
            set line=%%i
            call :Trim trimmed !line!
            SET locale=!trimmed:~9,-1!
        )


        cd Game
        if exist "League of Legends.exe" (
        	goto start
        )

        goto notfound

        :start
        @start "" "League of Legends.exe" "spectator spectator.{port}.lol.riotgames.com:80 {response_json2['observers']['encryptionKey']} {request_id} {i.upper()}" -UseRads -GameBaseDir=.. "-Locale=%locale%" -SkipBuild -EnableCrashpad=true -EnableLNP
        goto exit

        :Trim
        SetLocal EnableDelayedExpansion
        set Params=%*
        for /f "tokens=1*" %%a in ("!Params!") do EndLocal & set %1=%%b
        exit /b

        :notfound
        cls
        echo Cannot find your League of Legends installation. (If the issue persists, contact trebonius@wargraphs.gg)
        set /p manualFolder="Please enter your League of Legends installation path: "

        call :Trim manualFolder !manualFolder!
        IF "!manualFolder!" NEQ "" (
            echo !manualFolder! > "%APPDATA%\LoG_lolinstallpath.txt"
        )
        goto start

        :exit''')
        spectate.close()
        startfile('spectate.bat')
