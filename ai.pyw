import wx
import os
# os.environ["HTTPS_PROXY"] = "http://user:pass@192.168.1.107:3128"
import wikipedia
import wolframalpha
import pyttsx3
import webbrowser
import winshell
import json
import requests
import ctypes
import random
from urllib.request import urlopen
import speech_recognition as sr
import ssl
import urllib.request
import urllib.parse
import re
from regression import Regression
# Remove SSL error
requests.packages.urllib3.disable_warnings()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


headers = {'''user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)
           AppleWebKit/537.36 (KHTML, like Gecko)
           Chrome/53.0.2785.143 Safari/537.36'''}

#speak = wincl.Dispatch("SAPI.SpVoice")
speak = pyttsx3.init()
voices = speak.getProperty('voices')
voice = voices[1]
speak.setProperty('voice', voice.id)

# Requirements
videos = ['C:\\Users\\nEW u\\Videos\\Um4WR.mkv', 'C:\\Users\\nEW u\\Videos\\Jaatishwar.mkv']
app_id = 'GY6T92-YG5RXA85AV'


# GUI creation
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="Assistant")
        panel = wx.Panel(self)

        #ico = wx.Icon('programming.jpg', type=wx.ICON_ASTERISK, desiredWidth=-1, desiredHeight=-1)
        #self.SetIcon(ico)
    
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
                            label="Hello Sir. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,
                               size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()
        speak.say('''Welcome back Sir, Your assistant at your service.''')
        speak.runAndWait()


    def OnEnter(self, event):
        put = self.txt.GetValue()
        put = put.lower()
        link = put.split()
        r = sr.Recognizer()
        if put == '':
            with sr.Microphone() as src:
                r.adjust_for_ambient_noise(src) 
                speak.say("Yes? How can I help You?")
                speak.runAndWait()
                audio = r.listen(src)
            try:
                put = r.recognize_google(audio)
                put = put.lower()
                link = put.split()
                self.txt.SetValue(put)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google STT; {0}".format(e))
            except:
                print("Unknown exception occurred!")

        # Open a webpage
        if put.startswith('open '):
            try:
                speak.say("opening "+link[1])
                speak.runAndWait()
                webbrowser.open('http://www.'+link[1]+'.com')
            except:
                print('Sorry, No Internet Connection!')
        # Play Song on Youtube
        elif put.startswith('play '):
            try:
                link = '+'.join(link[1:])
                s = link.replace('+', ' ')
                query_string = urllib.parse.urlencode({"search_query" : link})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                print("http://www.youtube.com/watch?v=" + search_results[0])
                speak.say("playing "+s)
                speak.runAndWait()
                webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])
            except:
                print('Sorry, No internet connection!')
        # Google Search
        elif put.startswith('search '):
            try:
                link = '+'.join(link[1:])
                say = link.replace('+', ' ')
                speak.say("searching on google for "+say)
                speak.runAndWait()
                webbrowser.open('https://www.google.co.in/search?q='+link)
            except:
                print('Sorry, No internet connection!')
        # Empty Recycle bin
        elif put.startswith('empty '):
            try:
                winshell.recycle_bin().empty(confirm=False,
                                             show_progress=False, sound=True)
                speak.say("Recycle Bin Empty")
                speak.runAndWait()
            except:
                speak.say("Unknown Error")
                speak.runAndWait()
        # News
        elif put.startswith('science '):
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=new-scientist&sortBy=top&apiKey=your_API_here''')
                data = json.load(jsonObj)
                i = 1
                speak.say('''Here are some top science news from new scientist''')
                speak.runAndWait()
                print('''             ================NEW SCIENTIST=============
                      '''+'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    i += 1
            except:
                print('Sorry, No internet connection')
        elif put.startswith('headlines '):
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=your_API_here''')
                data = json.load(jsonObj)
                i = 1
                speak.say('Here are some top news from the times of india')
                speak.runAndWait()
                print('''             ===============TIMES OF INDIA============'''
                +'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    i += 1
            except Exception as e:
                print(str(e))
        # Lock the device
        elif put.startswith('lock '):
            try:
                speak.say("locking the device")
                speak.runAndWait()
                ctypes.windll.user32.LockWorkStation()
            except Exception as e:
                print(str(e))      
        # Play videos in boredom
        elif put.endswith('bored'):
            try:
                speak.say('''Sir, I\'m playing a video.
                            Hope you like it''')
                speak.runAndWait()
                video = random.choice(videos)
                os.startfile(video)
            except Exception as e:
                print(str(e))  
        # Say Whats up 
        elif put.startswith('whats up'):
            try:
                speak.say('''Nothing much, just trying to become the perfect assistant!''')
                speak.runAndWait()
            except Exception as e:
                print(str(e))  
        #Show stocks
        elif put.startswith('show stocks'):
            try:
               Regression.execute()
            except Exception as e:
                print(str(e))
                
        # Other Cases
        else:
            try:
                # wolframalpha
                client = wolframalpha.Client(app_id)
                res = client.query(put)
                ans = next(res.results).text
                print(ans)
                speak.say(ans)
                speak.runAndWait()

            except:
                # wikipedia/google
                put = put.split()
                put = ' '.join(put[:])
                #print(put)
                print(wikipedia.summary(put))
                speak.say('Searched google for '+put)
                speak.runAndWait()
                webbrowser.open('https://www.google.co.in/search?q='+put)


# Trigger GUI
if __name__ == "__main__":
        app = wx.App(True)
        frame = MyFrame()
        app.MainLoop()