{
    $("button").on("click", function (e) {
        e.preventDefault();
    })
    $(".overlay").hide();
}

{
    let interval1;
    const task_div = document.querySelector(".all_tasks")
    const task_status_mapping = ["To-do", "Ongoing", "Completed"];
    const time_formatting = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: "numeric",
        minute: "numeric",
        second: "numeric"
    }
    const weekday_mapping = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    function update_task_list(updated_task_list) {
        task_div.innerHTML = ""
        for (let task in updated_task_list) {
            const task_uuid = task;
            const task_info = updated_task_list[task];
            display_task(task_uuid, task_info);
        }
    }

    function query() {
        eel.recur_task()(out => {
        });
        eel.query_tasks()(out => update_task_list(out))
        eel.announce_expire()(out => {
            for (let _ of out) {
                const target = document.getElementById(_);
                target.classList.add("expired");
            }
        })
    }

    function check_recurring(recur_string) {
        if (recur_string.includes("d")) {
            return "Every day";
        } else {
            let recur_weekdays = []
            for (let i in weekday_mapping) {
                if (recur_string.includes(i.toString())) {
                    recur_weekdays.push(weekday_mapping[i])
                }
            }
            const length = recur_weekdays.length
            if (length === 0) {
            } else if (length === 1) {
                return `Every ${recur_weekdays[0]}`
            } else if (length === 2) {
                return `Every ${recur_weekdays[0]} and ${recur_weekdays[1]}`
            } else {
                return `Every ${recur_weekdays.slice(0, length - 1).join(", ")} and ${recur_weekdays[length - 1]}`
            }
            // console.log(recur_weekdays)
        }
    }

    function display_task(uuid, info) {
        const task_to_display = document.createElement("div");
        task_to_display.id = uuid;
        task_to_display.classList.add("task");
        const task_name = document.createElement("h3");

        const trash_task = document.createElement("img");
        trash_task.src = "/images/trash.png";
        trash_task.classList = "task_button";
        trash_task.addEventListener("click", function () {
            eel.remove_task(task_to_display.id);
            query();
        })
        task_to_display.appendChild(trash_task);


        task_name.innerHTML = info.name;
        task_to_display.appendChild(task_name);


        const task_status = document.createElement("p");
        task_status.classList.add("task_status");
        const task_cur_stage = info.stage;
        task_status.innerHTML = task_status_mapping[task_cur_stage];
        if (task_cur_stage === 0) {
            task_to_display.classList.add("todo");
        } else if (task_cur_stage === 1) {
            task_to_display.classList.add("ongoing");
        } else if (task_cur_stage === 2) {
            task_to_display.classList.add("completed");
        }

        task_to_display.appendChild(task_status);


        const task_info_deadline = document.createElement("p");
        task_info_deadline.classList.add("task_info_deadline");
        let task_deadline;
        if (info.deadline) {
            task_deadline = new Date(info.deadline * 1000).toLocaleString("en-US", time_formatting);
        } else {
            task_deadline = "None";
        }
        task_info_deadline.innerHTML = `Deadline: ${task_deadline}`;
        task_to_display.appendChild(task_info_deadline)

        if (info.recurring) {
            const task_recurring = check_recurring(info.recurring);
            const task_info_recurring = document.createElement("p");
            task_info_recurring.classList.add("task_info_recurring");
            task_info_recurring.innerHTML = task_recurring;
            task_to_display.appendChild(task_info_recurring);
        }
        $(task_to_display).on("click", function() {
            eel.update_stage(task_to_display.id)(out=>{});
            query();
        })

        task_div.appendChild(task_to_display);
    }


    interval1 = setInterval(function () {
        query()
    }, 30000);

    query()
}

{
    let close_buttons = $(".close");
    let add_buttons = $(".add_button");
    let forms = $("form");
    let add_form = $("#add_task_form");
    let overlay = $(".overlay");

    overlay.hide();
    close_buttons.on("click", function () {
        overlay.hide(200);
    })
    add_buttons.on("click", function () {
        overlay.show(200)
        forms.not(add_form).hide()
        add_form.show()
    })
}

{
    let add_form = $("#add_task_form");
    $("input[type='submit']").on("click", function (e) {
        e.preventDefault();
        let name = $("#n").val();
        if (!name) {
            name = "Untitled";
        }
        let deadline = $("#dl").val();
        if (!deadline) {
            deadline = null;
        } else {
            deadline = new Date(deadline).getTime()/1000;
        }
        console.log(deadline);
        let recur_day = $("#d")[0].checked;
        let recur;
        if (recur_day) {
            recur = "d";
        } else {
            let recur_list = [];
            for (let _ = 0; _ <= 6; _++) {
                if ($("#" + _)[0].checked) {
                    recur_list.push(_);
                }
            }
            recur = recur_list.join("");
        }
        if (!recur) {
            recur = null;
        }
        console.log(recur);
        eel.add_task(name, deadline, 0, recur)(out=>{});
        query();
        $(".overlay").hide(200);
    })
}

