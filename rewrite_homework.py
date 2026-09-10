#!/usr/bin/env python3
"""Rewrite homework sections to theory/explanation type (no Linux needed)."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
FILES = [
    ROOT / "index.html",
    ROOT / "_fragments" / "block1rest.html",
    ROOT / "_fragments" / "block2.html",
    ROOT / "_fragments" / "block3.html",
    ROOT / "_fragments" / "block4.html",
    ROOT / "_fragments" / "block5.html",
    ROOT / "_fragments" / "block6.html",
    ROOT / "_fragments" / "block7.html",
    ROOT / "_fragments" / "block7rest.html",
]

HOMEWORK = {
    "lesson-1": [
        "Vysvetli vlastnými slovami: čo je jadro (kernel) a čo je distribúcia.",
        "Nakresli strom hlavných adresárov (<code>/</code>, <code>/home</code>, <code>/etc</code>, <code>/var</code>, <code>/usr</code>) a ku každému pripíš, na čo slúži.",
        "Prečo je na učenie bezpečnejšie používať VM ako reálny počítač? Napíš aspoň dva dôvody.",
        "Rozhodni sa, ktorú distribúciu (Debian, Fedora alebo Mint) chceš inštalovať, a napíš, prečo si vybral práve ju.",
    ],
    "lesson-2": [
        "Napíš postup inštalácie VM v 5 krokoch vlastnými slovami, ako keby si ho vysvetľoval spolužiakovi.",
        "Vysvetli rozdiel medzi host a guest počítačom.",
        "Čo je ISO obraz a na čo slúži pri inštalácii?",
        "Prečo je pre začiatočníka bezpečné zvoliť pri inštalácii automatické rozdelenie disku?",
    ],
    "lesson-3": [
        "Rozlúšti prompt <code>student@debian:~$</code> - čo znamená každá časť?",
        "Napíš spamäti aspoň 3 príkazy z hodiny a čo robia.",
        "Prečo začínajú skryté súbory bodkou a ako ich zobrazíš?",
        "Vysvetli, na čo slúži tab completion a prečo šetrí čas.",
    ],
    "lesson-4": [
        "Vysvetli rozdiel medzi absolútnou a relatívnou cestou. Uveď príklad oboch.",
        "Nakresli strom adresárov <code>/home/student/Dokumenty</code> a ukáž šípkami, kam sa dostaneš príkazmi <code>cd /</code>, <code>cd ..</code> a <code>cd -</code>.",
        "Čo vypíše <code>pwd</code> po príkazoch <code>cd /etc</code> a potom <code>cd -</code>? Vysvetli, prečo.",
        "Prečo sa oplatí poznať <code>ls -lh</code> namiesto obyčajného <code>ls</code>?",
    ],
    "lesson-5": [
        "Vysvetli rozdiel medzi príkazmi <code>cp</code> a <code>mv</code>. Kedy použiť ktorý?",
        "Napíš, čo sa stane: <code>mkdir pokus && cd pokus && touch a.txt && ls</code> - čo postupne spraví každý príkaz?",
        "Prečo je <code>rm -rf</code> nebezpečný príkaz? Rozlúšti, čo znamená <code>-r</code> a <code>-f</code>.",
        "Na čo slúži príkaz <code>file</code> a kedy sa ti môže hodiť?",
    ],
    "lesson-6": [
        "Vysvetli rozdiel medzi <code>cat</code> a <code>less</code>. Kedy použiť ktorý?",
        "Kedy použiješ <code>head</code> a kedy <code>tail</code>? Uveď príklad použitia <code>tail -f</code>.",
        "Máš súbory <code>ahoj.txt</code>, <code>obraz.png</code>, <code>test.txt</code>, <code>skript.sh</code>. Čo vypíše <code>ls *.txt</code> a čo <code>ls ?est.*</code>?",
        "Vysvetli vlastnými slovami, čo rozširuje wildcards - shell alebo program?",
    ],
    "lesson-7": [
        "Prečo je dôležité vedieť čítať manuálové stránky (<code>man</code>) aj bez internetu?",
        "Čo znamená <code>!!</code> a <code>!42</code>? Kedy by si ich použil a kedy by si musel byť opatrný?",
        "Vysvetli, ako funguje vyhľadávanie v histórii cez <kbd>Ctrl</kbd>+<kbd>R</kbd>.",
        "Napíš aspoň 2 klávesové skratky na navigáciu v man stránke (napr. vyhľadávanie, ukončenie).",
    ],
    "lesson-8": [
        "Vysvetli rozdiel medzi <code>&gt;</code> a <code>&gt;&gt;</code> pri presmerovaní výstupu.",
        "Nakresli, ako pretekajú dáta cez rúru v príkaze <code>ls -la | grep txt</code>. Ktorý výstup ide kam?",
        "Vysvetli rozdiel medzi stdout a stderr. Uveď príklad, kedy sa ti zobrazí stderr.",
        "Prečo je kombinácia <code>history | grep apt</code> užitočná? Čo presne robí?",
    ],
    "lesson-9": [
        "Vysvetli rozdiel medzi bežným používateľom a rootom. Napíš 3 veci, ktoré môže len root.",
        "Prečo sa neodporúča pracovať stále ako root? Uveď aspoň 2 dôvody.",
        "Čo robí <code>sudo</code> a aké heslo ťa pri ňom systém pýta?",
        "Vysvetli rozdiel medzi <code>sudo</code> a <code>su</code>.",
    ],
    "lesson-10": [
        "Rozlúšti práva <code>-rwxr-xr-x</code> znak po znaku: čo v jednotlivých skupinách znamená r, w, x?",
        "Vysvetli číselný zápis práv: prečo <code>r=4</code>, <code>w=2</code>, <code>x=1</code> a koľko je teda <code>chmod 755</code>?",
        "Čo sa stane, keď skript nemá právo <code>x</code> a ako to opravíš?",
        "Prečo musí mať adresár právo <code>x</code>, aby si doňho mohol vojsť (<code>cd</code>)?",
    ],
    "lesson-11": [
        "Vysvetli, čo robí <code>chown student:dokumenty subor.txt</code> - čo sa zmení a pre koho.",
        "Prečo majú nové súbory predvolene práva ako <code>-rw-r--r--</code> a nie <code>-rwxr-xr-x</code>? Čo s tým má spoločné <code>umask</code>?",
        "Kedy by si súboru nastavil práva <code>600</code> a kedy <code>644</code>? Uveď príklad pre každý prípad.",
        "Prečo je nebezpečné meniť <code>chown</code> na systémových súboroch?",
    ],
    "lesson-12": [
        "Nakresli štruktúru priečinku <code>firma</code> (dokumenty, skripty, verejne) a ku každému pripíš, aké práva by si nastavil a prečo.",
        "Vysvetli na príklade, prečo je kombinácia <code>755</code> pre adresár bezpečná, ale <code>777</code> nie.",
        "Zhrň 3 najdôležitejšie veci, ktoré si sa naučil v blokoch 1-3.",
    ],
    "lesson-13": [
        "Vysvetli rozdiel medzi <code>'$meno'</code> a <code>\"$meno\"</code> - v ktorom prípade sa premenná rozšíri na hodnotu?",
        "Čo je shebang <code>#!/bin/bash</code> a prečo sa dáva na začiatok skriptu?",
        "Napíš na papier malý skript: pozdraví používateľa menom zadaným cez <code>read</code> a vypíše dnešný dátum. Bez počítača, len syntax.",
        "Prečo pri priradení <code>meno=Jano</code> nesmú byť medzery okolo <code>=</code>?",
    ],
    "lesson-14": [
        "Nakresli vetviaci diagram <code>if</code> / <code>else</code> pre skript, ktorý skontroluje, či súbor existuje.",
        "Vysvetli rozdiel medzi <code>[ \"$a\" = \"b\" ]</code> a <code>[ \"$a\" -gt 5 ]</code> - na čo sa porovnáva v oboch.",
        "Prečo sú medzery okolo <code>[</code> a <code>]</code> povinné? Čo by sa stalo bez nich?",
        "Vysvetli, kedy použiješ <code>elif</code> namiesto ďalšieho samostatného <code>if</code>.",
    ],
    "lesson-15": [
        "Čo vypíše tento cyklus? <code>for i in 1 2 3; do echo \"Pokus $i\"; done</code> - rozpíš každý krok.",
        "Kedy použiješ <code>for</code> a kedy <code>while</code>? Uveď príklad pre oba.",
        "Vysvetli, čo robí <code>break</code> a <code>continue</code> v cykle - aký je medzi nimi rozdiel?",
        "Napíš hlavičku cyklu <code>for</code>, ktorý prejde všetky súbory <code>*.txt</code> v aktuálnom adresári.",
    ],
    "lesson-16": [
        "Čo znamenajú <code>$1</code>, <code>$2</code>, <code>$#</code> a <code>$0</code> pri skripte?",
        "Napíš na papier funkciu, ktorá prijíma 2 čísla a vypíše ich súčet, plus volanie funkcie. Bez počítača.",
        "Čo znamená návratová hodnota <code>$?</code> a čo ti prezradí o minulom príkaze?",
        "Prečo je <code>$?</code> rovný 0, keď príkaz prešiel, a 1 alebo viac, keď zlyhal?",
    ],
    "lesson-17": [
        "Rozlúšti prepínače <code>tar -czf</code>: čo robí <code>c</code>, <code>z</code> a <code>f</code>?",
        "Prečo je dobré dávať do názvu zálohy dátum? Aké problémy by nastali bez neho?",
        "Nakresli postup zálohovacieho skriptu ako flowchart (kontrola priečinka → tvorba archívu → výpis výsledku).",
        "Prečo je lepšie zálohovať do archívu (tar.gz) ako len kopírovať priečinok?",
    ],
    "lesson-18": [
        "Naplánuj na papier, aké sekcie by mal mať <code>report.sh</code> a ktorý príkaz v každej sekcii bude.",
        "Prečo sa oplatí rozdeliť skript na menšie funkcie namiesto jedného dlhého kódu?",
        "Vysvetli, čo robí <code>date +%F</code> a ako by si ho využil v skripte.",
        "Ktorá časť shell scriptingu ti doteraz robí najväčší problém a prečo?",
    ],
    "lesson-19": [
        "Vysvetli rozdiel medzi <code>apt update</code> a <code>apt upgrade</code>.",
        "Čo je repozitár a čo sa stane, keď balík, ktorý chceš nainštalovať, v repozitári nie je?",
        "Čo sú závislosti balíka a prečo je dobré, že ich systém rieši automaticky?",
        "Vysvetli, prečo je na Debiane/Minte <code>apt</code> a na Fedore <code>dnf</code> - v čom je princíp rovnaký?",
    ],
    "lesson-20": [
        "Vysvetli, čo je proces a čo znamená PID a PPID.",
        "Aký je rozdiel medzi <code>kill</code> a <code>kill -9</code>? Prečo sa <code>-9</code> neodporúča ako prvá voľba?",
        "Čo sa stane, keď spustíš príkaz s <code>&amp;</code> na konci? A čo spraví <kbd>Ctrl</kbd>+<kbd>Z</kbd>?",
        "Vysvetli, na čo slúži <code>ps aux</code> a čo v ňom vidíš pri svojom používateľovi.",
    ],
    "lesson-21": [
        "Vysvetli rozdiel medzi <code>systemctl start</code> a <code>systemctl enable</code> - kedy sa čo použije?",
        "Čo je systemd unit a aké typy jednotiek poznáš (okrem služieb)?",
        "Na čo slúži <code>journalctl -u sluzba</code> a kedy pridáš <code>-f</code>?",
        "Prečo sa <code>enable</code> nevzťahuje len na aktuálny beh, ale aj na štart systému?",
    ],
    "lesson-22": [
        "Rozlúšti cron riadok: <code>30 7 * * 1 /usr/local/bin/zaloha.sh</code> - kedy presne sa spustí?",
        "Vymenuj 5 polí cron riadku a čo každé znamená.",
        "Napíš cron riadok, ktorý spustí skript každý deň o 18:00.",
        "Prečo je cron na serveroch dôležitý? Uveď aspoň 2 reálne príklady použitia.",
    ],
    "lesson-23": [
        "Vysvetli vlastnými slovami, čo je IP adresa, gateway a DNS - na čo slúžia?",
        "Prečo je <code>localhost</code> vždy <code>127.0.0.1</code> a na čo je dobrý?",
        "Čo znamená riadok <code>default via 192.168.1.1</code> z výpisu <code>ip route</code>?",
        "Kedy by si použil <code>ping</code> a čo ti odpoveď (alebo jej absencia) prezradí?",
    ],
    "lesson-24": [
        "Prečo je komunikácia cez SSH šifrovaná a čo by sa mohlo stať, keby nebola?",
        "Vysvetli rozdiel medzi súkromným a verejným kľúčom pri SSH. Ktorý nikdy nikomu nedávaš?",
        "Prečo je prihlasovanie cez kľúče bezpečnejšie ako cez heslá?",
        "Akou formou sa zadáva vzdialené pripojenie? Napíš príklad <code>ssh ...</code> a rozlúšti jednotlivé časti.",
    ],
    "lesson-25": [
        "Vysvetli vlastnými slovami, čo je mount a čo súborový systém.",
        "Aký je rozdiel medzi <code>df -h</code> a <code>du -sh</code>? Kedy použiť ktorý?",
        "Prečo je <code>/etc/fstab</code> dôležitý a prečo by si ho bez uváženia nemeňoval?",
        "Čo je swap a na čo slúži?",
    ],
    "lesson-26": [
        "Prečo sa vôbec učíme editovať text v termináli, keď existujú grafické editory? Uveď 2 dôvody.",
        "Vysvetli rozdiel medzi módom insert a normal vo vime. Ktorou klávesou sa medzi nimi prepínaš?",
        "Kedy by si použil <code>nano</code> a kedy <code>vim</code>? Na čo je <code>vimtutor</code>?",
        "Napíš spamäti 3 užitočné klávesové skratky pre nano a 3 pre vim.",
    ],
    "lesson-27": [
        "Prečo proces spustený na popredí zomrie, keď sa odpojíš cez SSH? Čo s tým spraví tmux?",
        "Vysvetli, čo znamená detach a attach v tmux - aký je medzi nimi rozdiel?",
        "Kedy sa ti v reálnej administrácii oplatí tmux? Uveď 2 príklady.",
        "Prečo je pri dlhých príkazoch (napr. inštalácia) nebezpečné jednoducho zavrieť terminál?",
    ],
    "lesson-28": [
        "Prečo by firewall nemal mať otvorené všetky porty? Čo sa môže stať pri zle nastavenom serveri?",
        "Vysvetli pravidlo „povoliť len to, čo naozaj potrebuješ\u201c na príklade SSH a web servera.",
        "Napíš 3 bezpečnostné pravidlá, ktoré by si dodržal na vlastnom serveri.",
        "Prečo sú pravidelné aktualizácie systému dôležité pre bezpečnosť?",
    ],
    "lesson-29": [
        "Vysvetli model klient-server na príklade vlastnej web stránky z hodiny.",
        "Čo znamená port 80 a port 443? Aký je medzi nimi rozdiel?",
        "Ako overíš z terminálu, že web server beží? Prečo <code>curl localhost</code> stačí ako test?",
        "Kde leží obsah stránok nginx a prečo doň musíš písať ako root?",
    ],
    "lesson-30": [
        "Čo robí <code>ExecStart</code> a čo <code>Restart=always</code> v unit súbore?",
        "Prečo je <code>daemon-reload</code> povinný po zmene unit súboru?",
        "Načrtni, čo všetko treba na vlastný servis: skript, unit súbor, príkazy. Napíš postup v 5 krokoch.",
        "Čo sa stane, keď máš <code>Restart=always</code> a skript okamžite skončí s chybou? Aké je riziko?",
    ],
    "lesson-31": [
        "Prečo sú logy pre správcu systému také dôležité? Uveď príklad situácie, keď ťa log zachráni.",
        "Vysvetli, čo robí <code>journalctl -u sluzba</code>, <code>-n 50</code> a <code>-f</code> - čo každý prepínač pridá?",
        "Prečo existuje logrotate a čo by sa stalo, keby logy rotované neboli?",
        "Vymenuj aspoň 3 príkazy na monitoring systému a čo každý ukazuje.",
    ],
    "lesson-32": [
        "Naplánuj záverečný projekt na papier: 4 časti v poradí a ako každú otestuješ.",
        "Ktorá časť projektu je podľa teba najťažšia a ako ju chceš zvládnuť?",
        "Priprav si 2-minútovú prezentáciu: čo ukážeš a v akom poradí?",
        "Prečo je lepšie dokončiť a otestovať každú časť hneď, ako nechať všetko na koniec?",
    ],
    "lesson-33": [
        "Napíš 5 vecí, ktoré ťa na krúžku najviac bavili alebo prekvapili.",
        "Napíš 1 vec, ktorú chceš v Linuxe vyskúšať ďalej, a prečo práve to.",
        "Ktorá hodina ti dala najviac a čo by si poradil budúcim študentom krúžku?",
    ],
}

SECTION_RE = re.compile(
    r'(<section class="lesson" id="(%s)">.*?<div class="homework">\s*<div class="homework-title">[^<]*</div>\s*)<ol>.*?</ol>(?=\s*</div>\s*</section>)'
    % "|".join(re.escape(k) for k in HOMEWORK),
    re.S,
)


def build_ol(items):
    lis = "\n".join(f"      <li>{item}</li>" for item in items)
    return f"    <ol>\n{lis}\n    </ol>"


def rewrite(content):
    def repl(m):
        lid = m.group(2)
        return m.group(1) + build_ol(HOMEWORK[lid])

    new, n = SECTION_RE.subn(repl, content)
    return new, n


total = 0
for f in FILES:
    if not f.exists():
        continue
    content = f.read_text(encoding="utf-8")
    new, n = rewrite(content)
    if n:
        f.write_text(new, encoding="utf-8")
        print(f"{f.name}: {n} homeworks rewritten")
        total += n

print(f"\nTotal: {total} homeworks rewritten")
missing = [k for k in HOMEWORK if total == 33 and k not in ""]