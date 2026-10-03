import requests
from pathlib import Path
import time
from playsound3 import playsound

wait=Path(__file__).parent/ "sounds/wait.mp3"
done=Path(__file__).parent/ "sounds/done.mp3"
next=Path(__file__).parent/ "sounds/next.mp3"
exits=Path(__file__).parent/ "sounds/exit.mp3"
print('''Welcome to the Church Of Random !
        May god save us.
Modes: 
1)Yes or No (yn)
2)Custom Choices (custom)''')

def provider(total_choices):
    choice_url=f"https://www.random.org/integers/?num=1&min=0&max={str(total_choices-1)}&col=5&base=10&format=plain&rnd=new"
    choice=int(requests.get(choice_url).text)
    return choice

yn=["Yes","No"]
custom_choices=list()
cn=1
while True:
    cmd=input("Select a mode: ").strip().lower()
    if cmd=="exit":
        print("Closing the gates of the church..")
        sound=playsound(exits,block=False)
        time.sleep(5)
        break
    elif cmd=="yn":
        c=provider(2)
        sound=playsound(wait,block=False)
        time.sleep(3)
        sound.stop()
        playsound(done)
        print(f"GOD said {yn[c]}")
  
    elif cmd=="custom":
        custom_choices=list()
        print("Write 'done' when finished.")
        while True:
            custom_choice=input(f"Add a custom choice {len(custom_choices)+1}: ")
            if custom_choice.strip().lower()=='done':
                print(f"Total {len(custom_choices)} choices recorded. ")
                break
            custom_choices.append(custom_choice)
            playsound(next)
        c=provider(len(custom_choices))
        print("GOD IS CHOOSING.....")
        sound=playsound(wait,block=False)
        time.sleep(3)
        sound.stop()
        playsound(done)
        print(f"GOD chose {custom_choices[c]}")

    






