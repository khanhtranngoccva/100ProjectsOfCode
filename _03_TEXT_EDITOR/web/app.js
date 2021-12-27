{
    let last_saved_text = "";
    let cur_fn = "";
    const new_button = $("#new_tx");
    const open_button = $("#open_tx");
    const save_button = $("#save_tx");
    const save_button2 = $("#save_as_tx");
    const file_name = $("h2");
    const text_area = $("textarea");
    const unsaved = $("#unsaved_overlay");
    const yes_button = $("#yes");
    const no_button = $("#no");
    const tab_title = $("title");

    const gather_info = out => {
        if (out != null) {
            last_saved_text = out[0];
            $(text_area).val(last_saved_text);
            cur_fn = out[1];
            tab_title.html(cur_fn);
            file_name.html(out[2]);
        } else {
        }
    }

    function open() {
        eel.open_file()(gather_info)
    }

    function new_() {
        file_name.html("Untitled");
        text_area.val("");
        cur_fn = "";
        last_saved_text = "";
        tab_title.html("Untitled");
    }

    function save_as() {
        eel.save_file(text_area.val())(gather_info);
    }

    function save() {
        if (!cur_fn) {
            save_as()
        } else {
            eel.auto_save(text_area.val(), cur_fn)(out => {
            });
        }
    }

    save_button.on("click", save);
    save_button2.on("click", save_as);

    open_button.on("click", () => {
            if (text_area[0].value !== last_saved_text) {
                unsaved.show(100);
                yes_button.on("click", function () {
                    unsaved.hide(100);
                    open()
                })
                no_button.on("click", function () {
                    unsaved.hide(100);
                })
            } else {
                open();
            }
        }
    )

    new_button.on("click", () => {
        if (text_area[0].value !== last_saved_text) {
            unsaved.show(100);
            yes_button.on("click", function () {
                unsaved.hide(100);
                new_()
            })
            no_button.on("click", function () {
                unsaved.hide(100);
            })
        } else {
            new_();
        }

    })


    unsaved.hide();
}

{
    function highlight() {
        let value = find_input.val();
        console.log(value)
        text_area.highlightTextarea('destroy');
        text_area.highlightTextarea({words: [value]});
    }

    let find_input = $("#find");
    let replace_button = $("#replace");
    let replace_button2 = $("#replace2");
    let replace_input = $("#replace_as");
    let text_area = $("textarea");
    find_input.on("keydown", function () {
        setTimeout(highlight, 50)
    })
    replace_button.on("click", function () {
        text_area.val(text_area.val().replace(find_input.val(), replace_input.val()));
        highlight();

    });
    replace_button2.on("click", function () {
        text_area.val(text_area.val().replaceAll(find_input.val(), replace_input.val()));
        highlight();

    });
    $(window).on("resize", highlight);
}