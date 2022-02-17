import sys # umožní čtení argumentů z příkazové řádky
import re # umožní práci s regulérními výrazy
from markdown import markdown # umožní práci s markdownem
import nltk # umožní tokenizaci do vět

# Definice

chyby = ["\sA\svýsledek\?", "absolutn\w{1,3}\s\wjistot\w{1,3}", "během", "bitv\w{1,4}\so\s\w{1,10}", "bobřík\w{,3}", "brous\w{1,4}\szuby", "cel\w{1,3}\sřad\w{1,3}", "cel\w{,3}\sinterne\w{1,3}", "co se týče", "čas ukáže", "časovan\w{1,3}\sbomb\w{1,3}", "časov\w{1,3}\shorizont\w{1,3}", "člověčenství", "člověčin\w{1,3}", "dál\w{,1}\sprohlub\w{1,7}", "daňov\w{1,3}\spoplatní\w{1,4}", "dedik\w{1,8}", "diskur\w{1,7}", "\w{,2}dojde k", "domác\w{1,4}\smazlíč\w{1,4}", "doslova", "došlo\s\w{,5}\s{,1}\w{,5}\s{,1}k\s{,}\w{,15}", "drtiv\w{1,3}\světšin\w{1,3}", "druhak", "\w{,5}financov\w{1,6}", "finančn\w{1,3}\sprostředk\w{1,4}", "hlavní\w{,4}\sprotagonist\w{1,4}", "jablk\w{1,3}\ssváru", "jak\w{,1}\spo\smásle", "\w{,3}kontrover\w{1,7}", "kostliv\w{1,5}\sskřín\w{1,2}", "křišťálov\w{1,3}\skoul\w{1,3}", "kudy běží zajíc", "kultovn\w{1,6}", "kvituji", "kvitova\w{1,4}", "lidsk\w{1,3}\sfakto\w{1,3}", "manuálw\{1,2}\szručn\w{1,4}", "medvědí\sslužb\w{1,3}", "mráz po zádech", "muž\w{1,4}\szákona", "na dlouhou trať", "na kobereček", "na poli", "na půdě", "na pořadu dne", "na pravém místě", "na svém místě", "napříč spektrem", "následně", "nic snazšího než", "nepřizpůsobiv\w{1,5}", "nervy v kýblu", "n\wž\w{1,2}\sna\skrk\w{,1}", "o čem přemýšlet", "olej do ohně", "ostře kritiz\w{1,6}","ostr\w{1,5} kritik\w{1,10}", "paradigm\w{1,5}", "part\w{1,3}\snadšenců", "platform\w{1,5}", "pod taktovkou", "pojďme", "posvě\w{1,6}", "prask\w{1,7}\sve\sšvech", "projekt\w{,3}", "prostě", "prý", "přehrš\w{1,2}", "rasov\w{1,4}\spodtext\w{,3}", "realiz\w{1,6}", "s kůží na trh", "sněhov\w{1,3}\s\nadílk\w{1,3}", "státn\w{1,3}\skas\w{1,5}", "souboj\w{,3}\stitánů", "svým způsobem", "širok\w{1,3}\s\veřejnos\w{1,3}", "špičk\w{1,3}\sledovc{1,3}", "tah\w{,2}\sna\sbranku", "totiž", "třešničk\w{1,3}\sna\sdortu", "tuzem\w{1,5}", "údajně", "úheln\w{1,3}\sk\wmen\w{,3}", "v neposlední řadě", "v podstatě", "v pravý čas", "v průběhu", "v rámci", "v současnosti", "větší jak\s", "víc jak\s", "více jak\s", "vlajkov\w{1,3}\slo\w{1,4}", "vlastně", "volnočasov\w{1,3}\saktivi\w{1,5}", "\w{,2}vykomuni\w{1,8}", "vymalováno", "z našich daní", "z pochopitelných důvodů", "zainvestov\w{1,5}", "\w{,2}zajímav\w{1,6}", "zelené razítko", "ztrá\w{1,4}\sna\sživotech", "želíz\w{1,5}\sv\sohni"]
kontextovky = ["[\s\S]{25}kvůli[\s\S]{44}", "[\s\S]{25}díky[^!,\.][\s\S]{45}", "[\s\S]{24}\sšanc[\s\S]{45}", "[\s\S]{24}\sČech[\s\S]{45}", "[\s\S]{25}Holandsk[\s\S]{45}", "[\s\S]{25}Holanďan[\s\S]{45}"]
typochyby = ["\.\.\.", "--", "\d{1,8}-{,1}ti\w{,10}", "\d{1,12}x", "\"\w{1,}", "\w{1,}[\.,\?!]{,1}\"", ",[^\W\d_]{1,12}", "\w{1,12}\'"]

# Načtení souboru

file = open(sys.argv[1], encoding="utf8") # otevře soubor volaný argumentem z příkazové řádky
content = file.read() # načte obsah souboru

# Konverze formátu

html = markdown(content) # převede markdown na html
plaintext = re.sub("<(/)?br(/)?>", "\n", html) # odstraní z html tag <br> a nahradí ho zalomením řádky
plaintext = re.sub("<[^>]*>", "", plaintext) # odstraní z html ostatní tagy
plaintextoneline = re.sub ("\n", " ", plaintext) # verze na jedné řádce, bude se hodit pro hledání kontextovek
titulek = plaintext.partition('\n')[0] # vybere první řádek jako titulek (pro výpis statistik)

# Počet slov a nejdelší slovo

slova = re.sub("https?:\/\/\S*", "", plaintext) # odstraní všechny url adresy
slova = re.sub("[,\.:;!?„“…'\"\']", "", slova) # vymaže interpunkci
slova = re.sub("(-|–|—)", " ", slova) # dlouhá-sousloví se nebudou počítat jako jedno slovo
slova = slova.split() # rozdělí předchystaný obsah na slova
pocetslov = len(slova) # počet slov v dokumentu
pocetznaku = len(plaintext) # počet znaků v dokumentu
ns = round(pocetznaku / 1800, 1) # vydělí počet znaků 1800 a zaokrouhlí na 1 desetinné místo
ns = str(ns) # převede počet normostran na string
ns = ns.replace(".", ",") # vymění anglickou desetinnou tečku za českou desetinnou čárku
minutycteni = round(pocetslov/200) # průměrný čtenář přečte za minutu 200 slov (zdroj: internet)
nejdelsislovo = max(slova, key=len) # najde nejdelší slovo
nejdelsislovodelka = len(nejdelsislovo) # počet znaků v nejdelším slově

# Nejdelší věta

sentences = re.sub("[„“]", "", plaintext) # odstraní uvozovky
sentences = re.sub("\s+\n", "\n", sentences) # odstraní mezery z konců odstavců
sentences = re.sub("(\w)\n", "\\1.\n", sentences) # doplní tečku za neohraničené odstavce (např. mezititulky)
sentences = nltk.sent_tokenize(sentences) # tokenizuje předchystaný obsah na věty
nejdelsiveta = max(sentences, key=len) # najde nejdelší větu
nejdelsivetaznaky = len(nejdelsiveta) # počet znaků v nejdelší větě
nejdelsivetaslova = len(nejdelsiveta.split()) # počet slov v nejdelší větě

# Slova za uvozovkami

citace = re.split("[,\?\!]“[^\n]", plaintext) # rozdělí dokument v místech, kde jdou po sobě čárka, otazník nebo vykřičník a uvozovky, a za nimi nenásleduje konec řádku
del citace[0] # smaže, co předchází konci první citace
slovapouvozovkach = [x.split()[0] for x in citace] # najde první slovo v každém řetězci
slovapouvozovkach = [re.sub("[\.,\?:;]", "", x) for x in slovapouvozovkach] # odstraní bordýlek

# Ošklivé fráze

nalezenechyby = [] # vytvoří prázdný seznam pro nalezené chyby
for chyby in chyby: # jedna chyba za druhou
	nalezenachyba = re.findall(chyby, plaintext, re.IGNORECASE) # vyhledá všechny výskyty chyb
	nalezenechyby.append(nalezenachyba) # každou nalezenou chybu doplní do seznamu

# Jedno slovo dvakrát po sobě

opakovani = re.findall("\\b(\\w+)\\s\\1\\b", plaintext, re.IGNORECASE) # vyhledá duplikáty
opakovani = [re.sub("(\\w+)", "\\1 \\1", x) for x in opakovani] # zduplikuje duplikáty (asi by to mělo jít i lepším regexem v předchozím řádku)

# Pojmy v uvozovkách

uvozovky = re.findall("„\\w+\\s*\\w*\\s*\\w*“", plaintext, re.IGNORECASE) # 1-3 slova mezi uvozovkami

# Typografické chyby

nalezenetypochyby = [] # vytvoří prázdný seznam pro nalezené chyby
for typochyby in typochyby: # jedna chyba za druhou
	nalezenatypochyba = re.findall(typochyby, plaintext, re.IGNORECASE) # vyhledá všechny výskyty chyb
	nalezenetypochyby.append(nalezenatypochyba) # každou nalezenou chybu doplní do seznamu

# Slova, u kterých je nutné pohlídat kontext

nalezenekontextovky = []
for kontextovky in kontextovky:
	nalezenakontextovka = re.findall(kontextovky, plaintextoneline, re.IGNORECASE)
	nalezenekontextovky.append(nalezenakontextovka)
				
# Úprava seznamů pro pěkný výstup

nalezenechyby = list(filter(None, nalezenechyby)) # vymaže prázdné subsety
nalezenechyby = sum(nalezenechyby, []) # spojí subsety do jednoho setu
	
nalezenetypochyby = list(filter(None, nalezenetypochyby)) # vymaže prázdné subsety
nalezenetypochyby = sum(nalezenetypochyby, []) # spojí subsety do jednoho setu

nalezenekontextovky = sum(nalezenekontextovky, []) # vymaže prázdné subsety

# Výpis

print ("*** KIKI POMÁHÁ S EDITOVÁNÍM {-_-} ***\n")
print (titulek, "\n- titulek:", len(titulek), "znaků s mezerami\n- dokument:", pocetznaku, "znaků s mezerami,", pocetslov, "slov,", ns, "NS,", minutycteni, "min čtení\n")
print ("Nejdelší slovo:\n- " + str(nejdelsislovo) + " (" + str(nejdelsislovodelka) + " znaků)\n")
print ("Nejdelší věta:\n- " + str(nejdelsiveta) + " ("+ str(nejdelsivetaslova) + " slov, " + str(nejdelsivetaznaky) + " znaků)\n")
if len(slovapouvozovkach)!= 0:
	print ("Pořadí slov po citacích:")
	print ("-", ", ".join(slovapouvozovkach), "\n")
if len(nalezenechyby) != 0:
	print ("Problematická slova a obraty:")
	print ("-", ", ".join(nalezenechyby), "\n")
if len(opakovani) != 0:
	print ("Zduplikovaná slova:")
	print ("-", ", ".join(opakovani), "\n")
if len(nalezenetypochyby) != 0:
	print ("Typografické chyby:")
	for x in nalezenetypochyby:
		print ("-", x)
	print ("Správná znaménka ke zkopírování: … „ “ ‚ ‘ ×\n")
if len(uvozovky) != 0:
	print ("Termity v uvozovkách:")
	print ("-", ", ".join(uvozovky), "\n")
if len(nalezenekontextovky) != 0:
	print ("Pohlídat význam:           ▼")
	for x in nalezenekontextovky:
		print ("-", x)
