from tkinter import *
import tkinter.filedialog as file
import Image as image
import Video as video
import threading


class Win:
    def __init__(self, win):
        self.win = win
        self.stop_button = Button(self.win, text="영상 정지하기(필수)", background='red', foreground='white',
                                  command=self.stop)
        self.load_image_Button = Button(self.win, text="사진 불러오기", command=self.paint)
        self.load_video_Button = Button(self.win, text="영상 불러오기", command=self.play)
        self.size_up_Button = Button(self.win, text="사이즈 업", command=self.size_up)
        self.size_down_Button = Button(self.win, text="사이즈 다운", command=self.size_down)
        self.canvas = Canvas(self.win, background="black")
        self.font_size = 5
        self.file_path = str()
        self.file_path_temp = str()
        self.image_string = str()
        self.data = list()
        self.thread = None
        self.thread_flag = False
        self.canvas_id = None

    def reg_component(self):
        self.stop_button.place(relx=0.0, y=5, relwidth=0.2)
        self.size_up_Button.place(relx=0.6, y=5, relwidth=0.1)
        self.size_down_Button.place(relx=0.7, y=5, relwidth=0.1)
        self.load_image_Button.place(relx=0.8, y=5, relwidth=0.1)
        self.load_video_Button.place(relx=0.9, y=5, relwidth=0.1)
        self.canvas.place(x=0, y=30, relwidth=1, relheight=1)
        self.canvas_id = self.canvas.create_text((0, 0), anchor="nw", font=("Courier", self.font_size),
                                                 text=self.image_string, fill="white")

    def stop(self):
        self.thread_flag = False

    def paint(self):
        self.file_path_temp = file.askopenfilename(filetypes=[
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".jpg"),
                ])

        if self.file_path_temp == "":
            return

        else:
            self.file_path = self.file_path_temp

        self.data = image.get_image(self.file_path)
        self.image_string = ''

        for i in range(0, len(self.data)):
            for j in range(0, 120):
                self.image_string += self.data[i][j]

            self.image_string += "\n"

        self.canvas.itemconfig(self.canvas_id, text=self.image_string)
        self.canvas.update()

    def re_paint(self):
        self.data = image.get_image(self.file_path)
        self.image_string = ''

        for i in range(0, len(self.data)):
            for j in range(0, 120):
                self.image_string += self.data[i][j]

            self.image_string += "\n"

        self.canvas.itemconfig(self.canvas_id, text=self.image_string, font=("Courier", self.font_size))
        self.canvas.update()

    def play(self):
        if not self.thread_flag:
            self.thread_flag = True
            self.file_path_temp = file.askopenfilename(filetypes=[
                    ("all video format", ".mp4"),
                    ("all video format", ".flv"),
                    ("all video format", ".avi"),
                ])

            if self.file_path_temp == "":
                return

            else:
                self.file_path = self.file_path_temp

            video.get_video(self.file_path)
            self.thread = threading.Thread(target=self.play_thread)
            self.thread.start()

    def play_thread(self):
        while True:
            self.data = get_video_capture()
            self.image_string = ''

            for i in range(0, len(self.data)):
                for j in range(0, 120):
                    self.image_string += self.data[i][j]

                self.image_string += "\n"

            self.canvas.itemconfig(self.canvas_id, text=self.image_string, font=("Courier", self.font_size))
            self.canvas.update()
            set_video_capture()

            if video.flag is False:
                self.thread_flag = False
                break

            if self.thread_flag is False:
                video.flag = False
                break

    def size_up(self):
        self.font_size += 1
        if not self.thread_flag:
            self.re_paint()

    def size_down(self):
        if self.font_size <= 1:
            return
        self.font_size -= 1
        if not self.thread_flag:
            self.re_paint()


data = None


def get_video_capture():
    global data
    data, evt = video.q.get()
    return data


def set_video_capture():
    video.evt.set()
    video.q.task_done()


# 폰트 사이즈가 날뛴다. 어떡하지 --> 고정폭 글꼴로 해결:Courier
def run():
    root = Tk()
    root.title("ImageForCmd")
    root.geometry("1000x700+50+50")
    root.resizable(True, True)
    root.configure(background="royal blue")

    win = Win(root)
    win.reg_component()
    root.mainloop()


if __name__ == '__main__':
    run()
