from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import askopenfilenames
import tkinter as tk

SONG_NUM_PLAYS = 1
SONG_START_TIME = 0.0

class MusicPlayer(tk.Frame):
    def __init__(self,master):
        super(MusicPlayer, self).__init__(master)
        self.grid()
        #init variables
        self.song_list = list()
        self.pausing = False
        self.current_song_index = 0

        self._ui_buttons_init()
        self._ui_playlist_init()
        self._ui_current_song_init()

    def _ui_current_song_init(self):
        self.status = tk.Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.status.grid(row=6,column=0)

    def _ui_playlist_init(self):
        self.playlist = tk.Text(self,wrap=tk.WORD,width=60)
        self.playlist.grid(row=8,column=0)

    def _ui_buttons_init(self):
        play_button = tk.Button(self, text="PLAY SONG",command=self._play_song,bg='AntiqueWhite1',width=40)
        play_button.grid(row=2,column=0)
        previous_button = tk.Button(self, text="PREVIOUS SONG",command=self._play_previous_song,bg='AntiqueWhite1',width=40)
        previous_button.grid(row=4,column=0)
        pause_button = tk.Button(self, text="PAUSE/UNPAUSE",command=self._pause_song,bg='AntiqueWhite1',width=40)
        pause_button.grid(row=3,column=0)
        next_button = tk.Button(self, text="NEXT SONG",command=self._play_next_song,bg='AntiqueWhite1',width=40)
        next_button.grid(row=5,column=0)
        add_button = tk.Button(self, text="ADD TO LIST",command=self._add_song_to_queue,bg='AntiqueWhite1',width=40)
        add_button.grid(row=1,column=0)

    def _songs_list_empty(self):

        if not self.song_list:
            self.status['text'] = "There are no songs in the list!"
            return True
        return False

    def _get_song_data(self,item):
        song = EasyID3(item)

        if song.get('title') is not None and song.get('artist') is not None:
            return ' : ' + song['title'][0] + ' -  ' + song['artist'][0]
        else:
            return item

    def _add_song_to_queue(self):
        directory = askopenfilenames()

        for song_dir in directory:
            print(song_dir)
            self.song_list.append(song_dir)
        self.playlist.delete(0.0, tk.END)

        for key, item in enumerate(self.song_list):
            song_data = str(key + 1) + '. ' + self._get_song_data(item)
            self.playlist.insert(tk.END, song_data + '\n')
    #################################################################################
    def _play_song(self):

        if self._songs_list_empty():
            return
        directory = self.song_list[self.current_song_index]

        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(SONG_NUM_PLAYS, SONG_START_TIME)
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        self.pausing = False
        self.status['text'] = "Now playing song number: " + str(self.current_song_index + 1) + " " + self._get_song_data(self.song_list[self.current_song_index])
    #################################################################################
    #################################################################################
    def _pause_song(self):

        if self._songs_list_empty():
            return

        if self.pausing:
            pygame.mixer.music.unpause()
            self.pausing = False
        elif not self.pausing:
            pygame.mixer.music.pause()
            self.pausing = True
    #################################################################################
    def _get_next_song(self):

        if self.current_song_index + 2 <= len(self.song_list):
            return self.current_song_index + 1
        else:
            return 0
    #################################################################################
    def _play_next_song(self):

        if self._songs_list_empty():
            return

        self.current_song_index = self._get_next_song()
        self._play_song()
    #################################################################################
    def _get_previous_song(self):

        if self.current_song_index - 1 >= 0:
            return self.current_song_index - 1
        else:
            return len(self.song_list) - 1
    #################################################################################
    def _play_previous_song(self):

        if self._songs_list_empty():
            return
        self.current_song_index = self._get_previous_song()
        self._play_song()

def start_music_player(window,app):

    while window.children:
        for event in pygame.event.get():
            if event.type == pygame.mixer.music.get_endevent():
                app._play_next_song()

        window.update()

def main():
    pygame.init()
    window = tk.Tk()
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.title("MP3 Music Player")
    app = MusicPlayer(window)

    start_music_player(window,app)

if __name__ == "__main__":
    main()