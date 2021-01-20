from tkinter import *
from tkinter import filedialog as fd
import Config
from ScrollableFrame import ScrollableFrame
from CheckBox import CheckBox
from JsonParser import JsonParser


class App:
    def __init__(self) -> object:
        self.__parser = JsonParser()
        self.root = Tk()
        self.frame = ScrollableFrame(self.root)
        self.__current_list = []
        self.__current_checkBoxes = []
        self.__last_entered_task = StringVar()
        self.main_menu = Menu(self.root)

    def __del__(self):
        self.__save_tasks()

    # TODO finish up func
    def __init_path(self):
        pass

    def __make_menu(self) -> None:
        self.root.config(menu=self.main_menu)
        file_menu = Menu(self.main_menu, tearoff=0)
        setting_menu = Menu(self.main_menu, tearoff=0)
        file_menu.add_command(label="Open tasks ...", command=self.__open_file)
        file_menu.add_command(label="New task", command=self.__new_task)
        file_menu.add_command(label="Save...", command=self.__save_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        # setting_menu.add_command(label="Colors", command=)
        # setting_menu.add_command(label="Font")
        # setting_menu.add_separator()
        # setting_menu.add_command(label="Default config")
        # setting_menu.add_command(label="File path")
        self.main_menu.add_cascade(label="File", menu=file_menu)
        # self.main_menu.add_cascade(label="Settings", menu=setting_menu)

    def __clear_canvas(self) -> None:
        for box in self.frame.scrollable_frame.winfo_children():
            box.destroy()
        self.frame.update()

    def __new_task(self) -> None:
        file_name = fd.asksaveasfilename(filetypes=[("Tasks files", "*.json")])
        print(file_name)
        self.__parser.change_file_path(file_name + ".json")
        self.__clear_canvas()
        self.__current_list.clear()

    def __save_tasks(self) -> None:
        for x, y in zip(self.__current_list, self.__current_checkBoxes):
            x["Status"] = y.get_state()
        self.__parser.back_up()

    def __open_file(self) -> None:
        file_name = fd.askopenfilename(filetypes=[("Tasks files", "*.json")])
        self.__parser.change_file_path(file_name)
        self.__clear_canvas()
        self.__current_checkBoxes.clear()
        self.__current_list.clear()
        self.__init_list_of_tasks()

    def __init_list_of_tasks(self) -> None:
        self.__parser.read_json()
        self.__current_list = self.__parser.get_lift_of_tasks()
        done = 0
        if len(self.__current_list) == 0:
            pass
        else:
            for task in self.__current_list:
                if task["Status"] == 1:
                    done = 1
                box = CheckBox(self.frame.scrollable_frame, text=f"{task['Task name']}",
                               bg=Config.BACKGROUND_FRAME, activeforeground="black", justify=LEFT,
                               activebackground=Config.BACKGROUND_FRAME, width=20, offvalue=done,
                               padx=Config.PADDING_X, pady=Config.PADDING_Y, fg=Config.FONT_COLOR,
                               wraplength=160, font=Config.FONT_SIZE)
                box.var.set(done)
                self.__current_checkBoxes.append(box)
                done = 0
                self.frame.update()

    def __add_task(self, event=None) -> None:
        box = CheckBox(self.frame.scrollable_frame, text=f"{self.__last_entered_task.get()}",
                       bg=Config.BACKGROUND_FRAME, activeforeground="black", justify=LEFT,
                       activebackground=Config.BACKGROUND_FRAME, width=20,
                       padx=Config.PADDING_X, pady=Config.PADDING_Y, fg=Config.FONT_COLOR,
                       wraplength=160, font=Config.FONT_SIZE)
        self.__current_checkBoxes.append(box)
        current_task = self.__last_entered_task.get()
        self.__last_entered_task.set("")
        self.__parser.add_task(current_task)
        self.frame.update()

    def select_all(self, event):
        def select_all2(widget):
            widget.selection_range(0, END)
            widget.icursor(END)  # курсор в конец

        self.root.after(10, select_all2, event.widget)

    def run(self) -> None:
        self.root.title(Config.TITTLE)
        self.root['bg'] = Config.BACKGROUND
        self.root.resizable(width=False, height=False)
        # menu bar
        self.__make_menu()
        add_task_entry = Entry(master=self.root, width=23, textvariable=self.__last_entered_task)
        add_task_button = Button(master=self.root, text="Add task", command=self.__add_task)
        add_task_entry.bind('<Return>', self.__add_task)
        # past inside frame
        self.__init_list_of_tasks()

        # top frame
        Frame(master=self.root, width=100, height=20, bg=Config.BACKGROUND) \
            .grid(row=0, column=0, columnspan=4)
        # left wrap
        Frame(master=self.root, width=Config.FRAME_WIDTH_LR, height=Config.FRAME_HEIGHT, bg=Config.BACKGROUND) \
            .grid(row=1, column=0, padx=Config.PADDING_X, pady=Config.PADDING_Y)
        # Main frame
        self.frame. \
            grid(row=1, column=1, columnspan=2, padx=Config.PADDING_X, pady=Config.PADDING_Y)
        # right wrap
        Frame(master=self.root, width=Config.FRAME_WIDTH_LR, height=Config.FRAME_HEIGHT, bg=Config.BACKGROUND) \
            .grid(row=1, column=4, padx=Config.PADDING_X, pady=Config.PADDING_Y)

        add_task_entry.grid(row=2, column=1, padx=Config.PADDING_X, pady=Config.PADDING_Y)
        add_task_button.grid(row=2, column=2, padx=Config.PADDING_X, pady=Config.PADDING_Y)

        self.root.mainloop()
