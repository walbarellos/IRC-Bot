import socket
import sqlite3
import time
import re
import random
import os

SERVER = "irc.rizon.life"
PORT = 6667
NICK = "AcreBot"
CHANNEL = "#Acre"

ADMINS = ["walbarellos"]

sock = socket.socket()
sock.connect((SERVER, PORT))

sock.send(f"NICK {NICK}\r\n".encode())
sock.send(f"USER {NICK} 0 * :Acre Bot\r\n".encode())

db = sqlite3.connect("bot.db")
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS karma (nick TEXT PRIMARY KEY, score INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS commands (name TEXT PRIMARY KEY, response TEXT)")
db.commit()

flood_tracker = {}
link_tracker = {}

os.makedirs("logs", exist_ok=True)

def log(msg):
    with open("logs/acre.log","a") as f:
        f.write(msg+"\n")

def send(msg):
    sock.send((msg + "\r\n").encode())

def privmsg(target, msg):
    send(f"PRIVMSG {target} :{msg}")

def add_karma(nick,val):
    cur.execute("SELECT score FROM karma WHERE nick=?",(nick,))
    r=cur.fetchone()
    if r:
        cur.execute("UPDATE karma SET score=? WHERE nick=?",(r[0]+val,nick))
    else:
        cur.execute("INSERT INTO karma VALUES (?,?)",(nick,val))
    db.commit()

def get_karma(nick):
    cur.execute("SELECT score FROM karma WHERE nick=?",(nick,))
    r=cur.fetchone()
    return r[0] if r else 0

def top_karma():
    cur.execute("SELECT nick,score FROM karma ORDER BY score DESC LIMIT 5")
    return cur.fetchall()

def get_cmd(name):
    cur.execute("SELECT response FROM commands WHERE name=?",(name,))
    r=cur.fetchone()
    return r[0] if r else None

connected=False

while True:

    data=sock.recv(4096).decode(errors="ignore")

    for line in data.split("\r\n"):

        if not line:
            continue

        print(line)

        if line.startswith("PING"):
            send(line.replace("PING","PONG"))

        if " 001 " in line and not connected:
            connected=True
            send(f"JOIN {CHANNEL}")

        if " JOIN " in line:
            nick=line.split("!")[0][1:]
            if nick!=NICK:
                privmsg(CHANNEL,f"🌿 Bem-vindo ao #Acre, {nick}! Amazônia brasileira.")

        if "PRIVMSG" in line:

            nick=line.split("!")[0][1:]
            msg=line.split(" :",1)[1]

            log(f"{nick}: {msg}")

            now=time.time()

            flood_tracker.setdefault(nick,[])
            flood_tracker[nick].append(now)
            flood_tracker[nick]=[t for t in flood_tracker[nick] if now-t<5]

            if len(flood_tracker[nick])>6:
                send(f"KICK {CHANNEL} {nick} :Flood detectado")
                continue

            if "http://" in msg or "https://" in msg:
                link_tracker.setdefault(nick,0)
                link_tracker[nick]+=1
                if link_tracker[nick]>4:
                    send(f"KICK {CHANNEL} {nick} :Spam de links")
                    continue

            for u in re.findall(r"(\w+)\+\+",msg):
                add_karma(u,1)

            for u in re.findall(r"(\w+)--",msg):
                add_karma(u,-1)

            if msg.startswith("!help"):
                privmsg(CHANNEL,"Comandos: !dado !moeda !numero !escolhe !karma !top")

            elif msg.startswith("!dado"):
                privmsg(CHANNEL,f"{nick} rolou {random.randint(1,6)}")

            elif msg.startswith("!moeda"):
                privmsg(CHANNEL,random.choice(["cara","coroa"]))

            elif msg.startswith("!numero"):
                privmsg(CHANNEL,f"Número sorteado: {random.randint(1,100)}")

            elif msg.startswith("!escolhe"):
                opts=msg.split()[1:]
                if opts:
                    privmsg(CHANNEL,"Escolhi: "+random.choice(opts))

            elif msg.startswith("!karma"):
                p=msg.split()
                user=p[1] if len(p)>1 else nick
                privmsg(CHANNEL,f"Karma de {user}: {get_karma(user)}")

            elif msg.startswith("!top"):
                ranking=top_karma()
                out="Top karma: "
                for n,s in ranking:
                    out+=f"{n}({s}) "
                privmsg(CHANNEL,out)

            elif msg.startswith("!addcmd") and nick in ADMINS:
                p=msg.split(maxsplit=2)
                if len(p)==3:
                    cur.execute("INSERT OR REPLACE INTO commands VALUES (?,?)",(p[1],p[2]))
                    db.commit()
                    privmsg(CHANNEL,"comando salvo")

            elif msg.startswith("!delcmd") and nick in ADMINS:
                p=msg.split()
                if len(p)>1:
                    cur.execute("DELETE FROM commands WHERE name=?",(p[1],))
                    db.commit()
                    privmsg(CHANNEL,"comando removido")

            elif msg.startswith("!op") and nick in ADMINS:
                send(f"MODE {CHANNEL} +o {msg.split()[1]}")

            elif msg.startswith("!kick") and nick in ADMINS:
                send(f"KICK {CHANNEL} {msg.split()[1]} :kickado por {nick}")

            else:
                cmd=msg.split()[0][1:] if msg.startswith("!") else None
                if cmd:
                    r=get_cmd(cmd)
                    if r:
                        privmsg(CHANNEL,r)
