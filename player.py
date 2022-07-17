from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *

pygame.init()
class MusicPlayer(Frame):
    def __init__(self,master):
        super(MusicPlayer, self).__init__(master)
        #init variables
        self.list1 = list()
        self.pausing = False
        self.list_index = 0
        self.SONG_END = pygame.USEREVENT + 1
        self.text1 = Text(self,wrap=WORD,width=60)
        self.text1.grid(row=8,column=0)
        self.label1 = Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.label1.grid(row=6,column=0)

        #init gui
        self.grid()
        b1 = Button(self, text="PLAY SONG",command=self.button2,bg='AntiqueWhite1',width=40)
        b1.grid(row=2,column=0)
        b2 = Button(self, text="PREVIOUS SONG",command=self.button4,bg='AntiqueWhite1',width=40)
        b2.grid(row=4,column=0)
        b3 = Button(self, text="PAUSE/UNPAUSE",command=self.button3,bg='AntiqueWhite1',width=40)
        b3.grid(row=3,column=0)
        b4 = Button(self, text="NEXT SONG",command=self.button5,bg='AntiqueWhite1',width=40)
        b4.grid(row=5,column=0)
        b5 = Button(self, text="ADD TO LIST",command=self.button1,bg='AntiqueWhite1',width=40)
        b5.grid(row=1,column=0)

    def songs_list_empty(self):
        if not self.list1:
            self.label1['text'] = "There are no songs in the list!"
            return True
        return False
    def check_song_data(self,item):
        song = EasyID3(item)

        if song.get('title') is not None and song.get('artist') is not None:
            return ' : ' + song['title'][0] + ' -  ' + song['artist'][0]
        else:
            return item

    def button1(self):
        directory = askopenfilenames()
        for song_dir in directory:
            print(song_dir)
            self.list1.append(song_dir)
        self.text1.delete(0.0, END)

        for key, item in enumerate(self.list1):
            song_data = str(key + 1) + '. ' + self.check_song_data(item)
            self.text1.insert(END, song_data + '\n')
    #################################################################################
    def song_data(self):
        song_data = "Now playing song number: " + str(self.list_index + 1) + " " + self.check_song_data(self.list1[self.list_index])
        return song_data
    #################################################################################
    def button2(self):
        if self.songs_list_empty():
            return
        directory = self.list1[self.list_index]

        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.pausing = False
        self.label1['text'] = self.song_data()
    #################################################################################
    def check_music(self):
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.button5()
    #################################################################################
    def button3(self):
        if self.songs_list_empty():
            return

        if self.pausing:
            pygame.mixer.music.unpause()
            self.pausing = False
        elif not self.pausing:
            pygame.mixer.music.pause()
            self.pausing = True
    #################################################################################
    def get_next_song(self):
        if self.list_index + 2 <= len(self.list1):
            return self.list_index + 1
        else:
            return 0
    #################################################################################
    def button5(self):
        if self.songs_list_empty():
            return

        self.list_index = self.get_next_song()
        self.button2()
    #################################################################################
    def get_previous_song(self):
        if self.list_index - 1 >= 0:
            return self.list_index - 1
        else:
            return len(self.list1) - 1
    #################################################################################
    def button4(self):
        if self.songs_list_empty():
            return
        self.list_index = self.get_previous_song()
        self.button2()

window = Tk()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.title("MP3 Music Player")
app = MusicPlayer(window)

window.mainloop()