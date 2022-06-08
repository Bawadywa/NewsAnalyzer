from tkinter import *
import main
import asynctkinter as at
import multiprocessing


at.patch_unbind()

white, black, red, green = '#ffffff', '#000000', '#FF0000', '#00FF00'


class FrontEnd:
    def __init__(self):
        self.root = Tk()
        self.root.title('Система моніторингу та прогнозування активності соціальних новин')
        self.root.wm_minsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.wm_maxsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.state('zoomed')

        self.colors = ('#003cff', '#336dff', '#765bfc', '#ba81fc')
        self.frame_names = ('parsing', 'extracting', 'analyzing', 'bar_analyzing')
        self.titles = ('Парсинг', 'Отримання даних', 'Аналіз МНК', 'Аналіз стовпчастий')
        self.frames = {}
        self.main_font = 'Consolas'
        self.button_relief = 'flat'
        self.button_cursor = 'hand2'

    def make_stages(self):
        for i in range(4):
            border = Frame(self.root, bg=black, padx=1, pady=0)
            frame = Frame(border, bg=white)
            border.place(relx=0.25*i, relwidth=0.25, relheight=1, anchor='nw')
            frame.place(relwidth=1, relheight=1)
            title = Label(frame, fg=white, text=self.titles[i], bg=self.colors[i])
            title.config(font=('Arial', 25))
            title.place(rely=0.07, relx=0.5, anchor='center', relwidth=1, relheight=0.15)
            self.frames[self.frame_names[i]] = frame

    @staticmethod
    def make_border(parent, color):
        return Frame(parent, bg=color, padx=2, pady=2)

    @staticmethod
    async def delete_message(message):
        await at.sleep(3000, after=message.after)
        message['text'] = ''

    async def parse(self, message):
        await at.sleep(1000, after=message.after)
        if not main.process.is_alive():
            message['text'] = 'Парсинг завершено!'
            message['fg'] = green
            self.root.update()
            at.start(self.delete_message(self.parse_message))
            main.process = multiprocessing.Process(target=main.parse)
            return
        await self.parse(message)

    def parse_wrapper(self):
        self.parse_message['fg'] = black
        self.parse_message['text'] = 'Парсинг триває...'
        self.root.update()
        main.process.start()
        at.start(self.parse(self.parse_message))

    def clean_wrapper(self):
        main.clean()
        self.analyzing_listbox.delete(0, END)
        self.clean_message['text'] = 'Дані очищено!'
        self.root.update()
        at.start(self.delete_message(self.clean_message))
        # clean listbox with words

    def extract_wrapper(self):
        self.extracting_message['text'] = 'Збір триває...'
        self.extracting_message['fg'] = black
        self.root.update()
        data = main.extract()
        if data:
            self.var.set(main.get_data())
            self.extracting_message['text'] = 'Збір завершено!'
            self.extracting_message['fg'] = green
            self.root.update()
            at.start(self.delete_message(self.extracting_message))
        else:
            self.extracting_message['text'] = 'Дані відсутні!'
            self.extracting_message['fg'] = red
            self.root.update()
            at.start(self.delete_message(self.extracting_message))

    def analyze_wrapper(self):
        selected_index = self.analyzing_listbox.curselection()
        if selected_index:
            selected_word = self.analyzing_listbox.get(selected_index)
            if not main.analyze(selected_word):
                self.analyzing_message['text'] = 'Збір статистики має тривати мінімум 20 днів.'
                self.analyzing_message['fg'] = black
                self.root.update()
                at.start(self.delete_message(self.analyzing_message))
            self.parsing_frame.focus()
        else:
            if not self.var.get():
                self.analyzing_message['text'] = 'Дані відсутні!'
                self.analyzing_message['fg'] = red
                self.root.update()
                at.start(self.delete_message(self.analyzing_message))
            else:
                self.analyzing_message['text'] = 'Слово не обрано!'
                self.analyzing_message['fg'] = black
                self.root.update()
                at.start(self.delete_message(self.analyzing_message))
            self.parsing_frame.focus()

    def bar_analyze_wrapper(self):
        selected_index = self.bar_analyzing_listbox.curselection()
        if selected_index:
            selected_count = self.bar_analyzing_listbox.get(selected_index)
            if not main.bar_analyze(selected_count):
                self.bar_analyzing_message['text'] = 'Дані відсутні!'
                self.root.update()
                at.start(self.delete_message(self.bar_analyzing_message))
            self.parsing_frame.focus()
        else:
            self.bar_analyzing_message['text'] = 'Кількість не обрано!'
            self.bar_analyzing_message['fg'] = black
            self.root.update()
            at.start(self.delete_message(self.bar_analyzing_message))
            self.parsing_frame.focus()

    def start(self):
        # Parsing
        self.parsing_frame = self.frames[self.frame_names[0]]

        border_button = self.make_border(self.parsing_frame, self.colors[0])
        parse_button = Button(border_button, text='Парсити новини', font=(self.main_font, 15), relief=self.button_relief, bg=white,
                              fg=self.colors[0], padx=10, pady=5, cursor=self.button_cursor,
                              activeforeground=white, activebackground=self.colors[0])
        self.parse_message = Label(self.parsing_frame, text='', font=(self.main_font, 15), fg=black, bg=white)

        self.parse_message.place(rely=0.4, relx=0.5, anchor='center')
        parse_button.config(command=self.parse_wrapper)
        border_button.place(rely=0.3, relx=0.5, anchor='center')
        parse_button.pack()

        border_button = self.make_border(self.parsing_frame, self.colors[0])
        open_news_button = Button(border_button, text='Показати новини', font=(self.main_font, 15), relief=self.button_relief, bg=white,
                                  fg=self.colors[0], padx=10, pady=5, cursor=self.button_cursor,
                                  activeforeground=white, activebackground=self.colors[0])

        border_button.place(rely=0.5, relx=0.5, anchor='center')
        open_news_button.config(command=main.open_news)
        open_news_button.pack()

        border_button = self.make_border(self.parsing_frame, red)
        clean_button = Button(border_button, text='Очистити існуючі дані', font=(self.main_font, 15), relief=self.button_relief, bg=white,
                              fg=red, padx=10, pady=5, cursor=self.button_cursor,
                              activeforeground=white, activebackground=red)
        self.clean_message = Label(self.parsing_frame, text='', font=(self.main_font, 15), fg=black, bg=white)

        border_button.place(rely=0.7, relx=0.5, anchor='center')
        clean_button.pack()
        clean_button.config(command=self.clean_wrapper)
        self.clean_message.place(rely=0.8, relx=0.5, anchor='center')

        # Extracting
        extracting_frame = self.frames[self.frame_names[1]]
        border_button = self.make_border(extracting_frame, self.colors[1])
        extract_button = Button(border_button, text='Зібрати статистику', font=(self.main_font, 15), relief=self.button_relief,
                                bg=white,
                                fg=self.colors[1], padx=10, pady=5, cursor=self.button_cursor,
                                activeforeground=white, activebackground=self.colors[1])
        self.extracting_message = Label(extracting_frame, text='', font=(self.main_font, 15), fg=black, bg=white)

        self.extracting_message.place(rely=0.4, relx=0.5, anchor='center')
        extract_button.config(command=self.extract_wrapper)
        border_button.place(rely=0.3, relx=0.5, anchor='center')
        extract_button.pack()

        border_button = self.make_border(extracting_frame, self.colors[1])
        open_stats_button = Button(border_button, text='Показати статистику', font=(self.main_font, 15),
                                   relief=self.button_relief,
                                   bg=white, fg=self.colors[1], padx=10, pady=5, cursor=self.button_cursor,
                                   activeforeground=white, activebackground=self.colors[1])

        border_button.place(rely=0.5, relx=0.5, anchor='center')
        open_stats_button.config(command=main.open_stat)
        open_stats_button.pack()

        # Analyzing
        analyzing_frame = self.frames[self.frame_names[2]]
        listbox_label = Label(analyzing_frame, text='Оберіть слово:', font=(self.main_font, 21), fg=self.colors[2], bg=white)
        listbox_frame = Frame(analyzing_frame)

        words = main.get_data()
        self.var = StringVar(value=words)
        self.analyzing_listbox = Listbox(listbox_frame, listvariable=self.var, height=10, relief=self.button_relief,
                                    font=(self.main_font, 20),
                                    fg=self.colors[2], border=0, activestyle='none', selectbackground=self.colors[2])
        self.root.update()
        self.analyzing_message = Label(analyzing_frame, text='', font=(self.main_font, 15), fg=black, bg=white,
                                  wraplength=analyzing_frame.winfo_width())

        listbox_frame.place(rely=0.45, relx=0.5, anchor='center')
        listbox_label.place(rely=0.225, relx=0.5, anchor='center')
        self.analyzing_listbox.pack(side=LEFT, fill=BOTH)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        self.analyzing_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.analyzing_listbox.yview)


        border_button = self.make_border(analyzing_frame, self.colors[2])
        analyzing_button = Button(border_button, text='Показати аналіз МНК', font=(self.main_font, 15), relief=self.button_relief,
                                  bg=white, fg=self.colors[2], padx=10, pady=5, command=self.analyze_wrapper, cursor=self.button_cursor,
                                  activeforeground=white, activebackground=self.colors[2])

        border_button.place(rely=0.7, relx=0.5, anchor='center')
        analyzing_button.pack()
        self.analyzing_message.place(rely=0.8, relx=0.5, anchor='center', relwidth=0.8)

        # Bar Analyzing
        bar_analyzing_frame = self.frames[self.frame_names[3]]
        listbox_label = Label(bar_analyzing_frame, text='Оберіть кількість слів:', font=(self.main_font, 21), fg=self.colors[3],
                              bg=white)
        listbox_frame = Frame(bar_analyzing_frame)

        counts = [50, 40, 30, 20, 10]
        list_items = StringVar(value=counts)
        self.bar_analyzing_listbox = Listbox(listbox_frame, listvariable=list_items, height=5, relief=self.button_relief,
                                        font=(self.main_font, 20), fg=self.colors[3], border=0,
                                        activestyle='none', selectbackground=self.colors[3])
        self.bar_analyzing_message = Label(bar_analyzing_frame, text='', font=(self.main_font, 15), fg=red, bg=white)

        listbox_frame.place(rely=0.35, relx=0.5, anchor='center')
        listbox_label.place(rely=0.225, relx=0.5, anchor='center')
        self.bar_analyzing_listbox.pack(side=LEFT, fill=BOTH)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        self.bar_analyzing_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.bar_analyzing_listbox.yview)

        border_button = self.make_border(bar_analyzing_frame, self.colors[3])
        bar_analyzing_button = Button(border_button, text='Показати стовпчастий аналіз', font=(self.main_font, 15),
                                      relief=self.button_relief, bg=white, fg=self.colors[3], padx=10, pady=5,
                                      command=self.bar_analyze_wrapper, cursor=self.button_cursor,
                                      activeforeground=white, activebackground=self.colors[3])

        self.bar_analyzing_message.place(rely=0.6, relx=0.5, anchor='center')
        border_button.place(rely=0.5, relx=0.5, anchor='center')
        bar_analyzing_button.pack()

        self.root.mainloop()


if __name__ == '__main__':
    main.create()
    front = FrontEnd()
    front.make_stages()
    front.start()
