import datetime
import sys
import time

import eel
import hashlib
import os
import json
import traceback

os.chdir(os.path.realpath(os.path.dirname(__file__)))

data_directory = "data"
data_file = os.path.join(data_directory, "data.json")
data_backup = os.path.join(data_directory, "backup.json")


# recurring modes: "0123456dm"

def quick_strf(t):
    return time.strftime("%A %Y-%m-%d, %H:%M:%S", t)


def log_to_file(*args):
    with open("log.txt", "a") as _file:
        print(*args, file=_file, sep="\n")


@eel.expose
def save_data():
    with open(data_file, "w") as _file:
        json.dump(all_tasks, _file)


@eel.expose
def add_task(name: str = "Untitled", deadline=None, stage: int = 0, recurring=None):
    counter = 0
    while True:
        counter += 1
        task_uuid = hashlib.sha256(str(counter).encode()).hexdigest()
        if task_uuid not in all_tasks:
            break
    # print(task_uuid)
    all_tasks[task_uuid] = {}
    current_task = all_tasks[task_uuid]
    current_task["name"] = name
    current_task["deadline"] = deadline
    current_task["stage"] = stage
    current_task["recurring"] = recurring
    current_task["next_recur"] = None
    if recurring:
        # print('oof')
        update_recur(task_uuid)
    save_data()


@eel.expose
def edit_task(task_uuid, name: str = "Untitled", deadline=None, stage: int = 0, recurring=None):
    current_task = all_tasks[task_uuid]
    current_task["name"] = name
    current_task["deadline"] = deadline
    current_task["stage"] = stage
    current_task["recurring"] = recurring
    current_task["next_recur"] = None
    if recurring:
        update_recur(task_uuid)
    save_data()


@eel.expose
def announce_expire():
    current_time = time.time()
    expired_tasks = []
    for task_uuid, task_info in all_tasks.items():
        try:
            if task_info["deadline"] <= current_time and task_info["stage"] != 2:
                # expired_tasks.append((task_uuid, task_info["name"], quick_strf(time.localtime(task_info["deadline"]))))
                expired_tasks.append(task_uuid)
        except Exception as e:
            log_to_file(e, traceback.format_exc())
    # print(expired_tasks)
    save_data()
    return expired_tasks


@eel.expose
def recur_task():
    current_time = time.time()
    for task_uuid, task_info in all_tasks.items():
        try:
            if task_info["next_recur"] <= current_time:
                task_info["stage"] = 0
                update_recur(task_uuid)
        except Exception as e:
            log_to_file(e, traceback.format_exc())
    save_data()


def update_recur(task_uuid):
    task_info = all_tasks[task_uuid]
    cur_time = datetime.datetime.now()
    try:
        current_recurring = task_info["recurring"]
        if current_recurring:
            if any(map(lambda x: x in "0123456", current_recurring)):
                a = list(map(lambda x: next_weekday(cur_time, x).timestamp(),
                             [int(_) for _ in current_recurring if _ in "0123456"]))
                task_info["next_recur"] = min(a)
                # print(quick_strf(time.localtime(task_info["next_recur"])))
    except Exception as e:
        log_to_file(e, traceback.format_exc())
    save_data()


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


@eel.expose
def query_tasks():
    return all_tasks


@eel.expose
def remove_task(uuid):
    all_tasks.pop(uuid, 0)
    save_data()


@eel.expose
def update_stage(uuid):
    # print(all_tasks[uuid]["stage"])
    try:
        all_tasks[uuid]["stage"] = (all_tasks[uuid]["stage"] + 1) % 3
        save_data()
    except:
        pass


@eel.expose
def test():
    return 1


if __name__ == '__main__':
    try:
        try:
            with open(data_file) as file:
                all_tasks = json.load(file)
        except FileNotFoundError:
            all_tasks = {}
    except Exception as e:
        with open("log.txt", "w") as file:
            print(e, file=file)
            print(traceback.format_exc(), file=file)
        sys.exit()

    # add_task("Learn Python", deadline=time.time() - 10, stage=0, recurring="6")
    eel.init("web")
    eel.start("/index.html")
