import json
import Config

class Task:
    def __init__(self) -> object:
        self.task_name: str = None
        self.is_done: bool = False

class JsonParser:

    def __init__(self) -> object:
        self.__all_tasks: list = []
        self.__filename: str = Config.FILE_PATH

    def change_file_path(self, new_path: str) -> None:
        self.__filename = new_path

    def add_task(self, task_name: str) -> None:
        d = {"Task name": task_name, "Status": 0}
        self.__all_tasks.append(d)

    def read_json(self) -> None:
        with open(self.__filename, 'r') as read_file:
            self.__all_tasks = json.load(read_file)

    def back_up(self) -> None:
        with open(self.__filename, 'w') as write_file:
            json.dump(self.__all_tasks, write_file)

    def list_empty(self) -> bool:
        if len(self.__all_tasks) == 0:
            return True
        return False

    def get_lift_of_tasks(self) -> list:
        return self.__all_tasks

    def set_lift_of_tasks(self, list_of_tasks: list) -> None:
        self.__all_tasks = list_of_tasks

    def print_tasks(self):
        print(self.__all_tasks)

    def get_file_path(self) -> str:
        return self.__filename

    def access_by_index(self, index: int) -> dict:
        return self.__all_tasks[index]

    def find(self, task_name: str):
        pass

    def find_if(self, func):
        pass
