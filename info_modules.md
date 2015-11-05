# 9gag
:exclamation: import failed: No module named utils

# bashfr
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# bashorg
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# belotebot
## CmdBelote
Jeu de belote. Si vous voulez être renseigné,                 allez au bureau des renseignements, ils vous renseigneront…
## IqBobBelote
:exclamation: import failed: 'NoneType' object is not callable

# bideetmusique
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# blague
depends:
* sqlalchemy


# botanswers
:exclamation: import failed: cannot import name utils

# botmpd
depends:
* mutagen
* mpd
* BeautifulSoup

:exclamation: import failed: No module named exceptions

# bourse
## CmdBourse
bourse [valeur [historique]]
Affiche le taux de conversion d'une valeur boursière.
Valeurs disponibles: JPY, USD, CHF, CAD

# canalplus
:exclamation: import failed: No module named abstract_modules

# chiffres_lettres
depends:
* chiffresc

## ChiffresCmd
Le module du jeux des chiffres et des lettres
chiffres init : génère une nouvelle partie
chiffres solve : cherche à résoudre le problème
## LettresCmd
:exclamation: import failed: 'LettresCmd' object has no attribute 'dico'

# chuck
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# cmdalacon
:exclamation: import failed: No module named utils

# cmdfu
## CmdCmdFu
Commandline tips
cmdfu : Retourne une commande aléatoire

# coin
## CmdCoin
Shooting ducks

# date
## CmdDate
date : Affiche la date et l'heure actuelle

# date_timezone
depends:
* sqlalchemy
* pytz

## CmdDateTimeZone
date : show the actual date for the server and the sender
date set <timezone> : set your actual timezone (see http://pastebin.com/XbLSvZhY)
date all : show the actual date for all register users
date <timezone> : show the actual date and time for <timezone>date <user> : show the actual date and time for <user>

# ddg
depends:
* duckduckgo
* BeautifulSoup
* simplejson

:exclamation: import failed: No module named utils

# dette
depends:
* sqlalchemy

## CmdDette
Gestionnaire de dettes

|Command|Description|
|-------|-----------|
|list|dette list [name] : Liste les dettes de [name1]|
|add|dette add [name1] [amount] [name2] [reason] : Ajoute une dette de [amount] que doit payer [name1] à [name2] à cause de [reason]
dette add [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent tous [amount] à [name3] à cause de [reason]|
|multiple|dette multiple [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent se partager la dette [amount] à payer à [name3] à cause de [reason]|
|remove|dette remove [id1], [id2], [id3] : Supprime les dettes dont les id sont [id1], [id2], [id3]|


# dns

# doge
## CmdDoge
doge <message>: dogifies your <message>

# dok
## CmdDok
:exclamation: import failed: 'CmdDok' object has no attribute 'url'

# exa
depends:
* BeautifulSoup

## CmdExa
exa [mots clefs]
Effectue une recherche sur le web et affiche les 4 premiers résultats

# excuse
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# getjid
## CmdGetjid
getjid [nom]
Affiche le jid pour découvrir qui se cache derrière un pseudo

# google
depends:
* simplejson

:exclamation: import failed: No module named utils

# gore
depends:
* sqlalchemy

## CmdGore
gore <pseudo>
Ajoute un point gore à <pseudo> (10 s minimum d'intervalle)

# haddock
## Haddock
Les insultes du capitaine haddock :p.

# hg
depends:
* yaml
* mercurial

:exclamation: import failed: No module named exceptions

# hidden_word
depends:
* sqlalchemy

:exclamation: import failed: cannot import name utils

# hl
depends:
* sqlalchemy

## HighLight
hl <people>: Highligh <people> (whom can be registerd users, pseudos or list of people)
hl <people> :<message>: Highligh <people>, and shows <message>
hl show [<list>]: Shows list of people
hl set|add <list> <people>: Add <people> to <list>
hl rm|del <list> [<people>]: Remove <list>, or <people> from <list>

# kaamelott
:exclamation: import failed: No module named utils

# kick
:exclamation: import failed: No module named utils

# kickstarter
depends:
* requests
* sqlalchemy

## CmdKickStarter
kickstarter : show this help
kickstarter list: list known projects
kickstarter all: show the status of all known projects
kickstarter add <project-owner>/<project-name>: add a project
kickstarter rm <project-name>: remove a project
kickstarter <project-name>: show the status of the project

# link
:exclamation: import failed: No module named utils

# mail
depends:
* pyinotify


# mute
depends:
* xmpp

:exclamation: import failed: No module named utils

# nextprev
## CmdNextPrev


# ola
## Ola
Fait la ola.

# pendu
## CmdPendu
Un superbe jeu de pendu
pendu init : lance une partie avec un mot aléatoire (to be coded...)
pendu init [word] : lance une partie avec 'word' comme mot à trouver
pendu reset : pour interrompre une partie en cours
pendu try [letter] : propose la lettre 'letter'
pendu played : affiche la liste des lettres déjà jouées

# pingpong
## CmdPingPong


# pioche
## CmdPioche
pioche
Pioche une carte au hasard dans un jeu de 52 cartes

# raced
depends:
* sqlalchemy
* lib

## CmdRaced
raced pseudo
Ajoute un point raced à /me envers pseudo

# reminder
depends:
* sqlalchemy

:exclamation: import failed: No module named abstract_modules

# roll
## CmdRoll
Le jugement des dieux !... Enfin de Pipo !
roll [entier] : renvoie un entier entre 1 et [entier]
roll [x,y,z] : renvoie un choix aléatoire entre x, y et z

# rps
## CmdRPS
Rock Paper Scissors:
rps init <n> : lance une nouvelle partie avec <n> joueurs
rps bot : pour se mesurer au bot !!!
rps (Rock|Paper|Scissor) : pour jouer

# rpsls
## CmdRPSLS
Rock Paper Scissors Lizard Spock:
rpsls init <someone> : Pour défier quelqu'un.
rpsls accept <someone> : Accèpte le défi de quelqu'un.
rpsls (Rock|Paper|Scissor|Lizard|Spock) : pour jouer

# rss
depends:
* html2text
* feedparser
* twitter
* sqlalchemy
* BeautifulSoup

:exclamation: import failed: No module named abstract_modules

# scmb
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# scores
## CmdScores
score [module] [params]
Consulte les scores pour le module [module]

# sos_bides
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# spell
depends:
* enchant

## CmdSpell
Correction orthographique
spell check : vérifie si un mot existe ou pas
spell suggest : donne les mots approchants

# t2a
## CmdText2Ascii
!t2a texte : transforme le texte en ascii art

# taggle
## CmdTaggle
Ta gueule [nom]
Dit taggle à nom (valeur par défaut à mettre dans le fichier de configuration)

# todo
depends:
* sqlalchemy

## CmdTodo
Gestion des TODO-lists

|Command|Description|
|-------|-----------|
|search|todo search [element]: recherche un TODO qui contient [element]|
|add|todo add [name] [msg] : crée le nouveau todo [msg] dans la liste [name]|
|list|todo list : affiche la liste des todolist existantes.
todo list [name] : affiche les todo de la liste [name]|
|remove/delete/rm|todo remove [n,...] : supprime les todos d'id [n,...]|


# trac
## CmdTrac
trac [num]
Liste les tickets trac actifs ou en affiche un en détail

# troll
:exclamation: import failed: No module named utils

# tv
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# twitter
depends:
* twython
* sqlalchemy


# unicode
## CmdUnicode
Unicode caractère
    Affiche des informations sur le caractère unicode « caractère »
unicode nom
    Recherche le caractère unicode donc le nom ressemble à « nom »


# urbandict
## UrbanDict
urban [result] [query] : displays the [result]-th response to the [query]
urban : displays a random urban dictionary entry

# url
depends:
* sqlalchemy
* hyperlinks_scanner

:exclamation: import failed: No module named utils

# vdm
depends:
* BeautifulSoup

:exclamation: import failed: No module named utils

# wiki
:exclamation: import failed: No module named utils

# wr
depends:
* simplejson

## CmdWordRef
wr in out expression: traduit [expression] de la langue [in] vers la langue [out]

# xhtml
:exclamation: import failed: No module named utils

