{
    let canvas = $("canvas");
    let canvas_handle = canvas[0];
    let ctx = canvas_handle.getContext("2d");
    let mousedown_ = 0;
    let mouseX = 0;
    let mouseY = 0;
    let old_mouseX = 0;
    let old_mouseY = 0;
    let fill_style = "#000000";
    let fill_mode = "stroke";
    let fill_radius = 10;
    let stroke_style = "#000000";
    let recursive_timeout;
    canvas_handle.height = 0.8 * window.innerHeight;
    canvas_handle.width = 0.8 * window.innerWidth;
    canvas.on("mousedown", function (e) {
        if (e.button === 0) {
            mousedown_ = 1;
        } else {
            mousedown_ = 0;
        }
    })
    $(window).on("mouseup", function (e) {
        mousedown_ = 0;
    })
    // canvas.on("mouseover", function (e) {
    //     mousedown_ = 0;
    // })
    // canvas.on("mouseover")
    $(window).on("mousemove", function (e) {
        old_mouseX = mouseX;
        old_mouseY = mouseY;
        mouseX = e.pageX - (canvas_handle.getBoundingClientRect().left + window.pageXOffset);
        mouseY = e.pageY - (canvas_handle.getBoundingClientRect().top + window.pageYOffset);
        // mouseX = e.pageX;
        // mouseY = e.pageY;
        draw()
    })

    function draw() {
        if (mousedown_) {
            fill_style = $("#fill_color").val();
            stroke_style = $("#stroke_color").val()
            fill_radius = $("#radius").val();
            console.log(fill_style)
            ctx.fillStyle = fill_style;
            ctx.strokeStyle = fill_style;
            // console.log(mouseX, mouseY)
            switch (fill_mode) {
                case "circle": {
                    ctx.globalCompositeOperation = 'source-over'
                    ctx.moveTo(mouseX, mouseY)
                    ctx.arc(mouseX, mouseY, fill_radius, 0, Math.PI * 2, false);
                    // console.log("oof");
                    ctx.fill();
                    break;
                }
                case "square": {
                    ctx.globalCompositeOperation = 'source-over'
                    ctx.fillRect(mouseX - fill_radius / 2, mouseY - fill_radius / 2, fill_radius, fill_radius);
                    break;
                }
                case "stroke": {
                    ctx.lineCap = "round";
                    ctx.globalCompositeOperation = 'source-over'
                    ctx.beginPath();
                    ctx.moveTo(old_mouseX, old_mouseY);
                    ctx.lineTo(mouseX, mouseY);
                    ctx.lineWidth = fill_radius;
                    ctx.stroke();
                    break;
                }
                case "eraser": {
                    ctx.lineCap = "round";
                    ctx.globalCompositeOperation = "destination-out";
                    ctx.beginPath();
                    ctx.moveTo(old_mouseX, old_mouseY);
                    ctx.lineTo(mouseX, mouseY);
                    ctx.lineWidth = fill_radius;
                    ctx.stroke();
                    break;
                }
            }
        }
        recursive_timeout = setTimeout(draw, 1);
    }

    recursive_timeout = setTimeout(draw, 1);

    $("nav p").on("click", function () {
        switch (this.id) {
            case "stroke":
                fill_mode = "stroke";
                break;
            case "eraser":
                fill_mode = "eraser";
                break;
        }
    })
}

{
    let handle = $(".handle");
    console.log(handle)
    let navbar = $("nav");
    let mousedown_ = 0;
    let mouseX = 0;
    let mouseY = 0;
    let old_mouseX;
    let old_mouseY;
    let recursive_timeout;
    // handle.css("background", "yellow")
    handle.on("mousedown", function (e) {

        // console.log("oof");
        if (e.button === 0) {
            mousedown_ = 1;
        } else {
            mousedown_ = 0;
        }
    });
    $(window).on("mouseup", function (e) {
        mousedown_ = 0;
    });
    $(window).on("mousemove", function (e) {
        old_mouseX = mouseX;
        old_mouseY = mouseY;
        mouseX = e.pageX;
        mouseY = e.pageY;
        const dX = mouseX - old_mouseX
        const dY = mouseY - old_mouseY
        // console.log(mouseX, mouseY)
        if (mousedown_) {
            console.log(mouseX, mouseY)
            navbar.css({position: "fixed", top: `+=${dY}px`, left: `+=${dX}px`});
        }
    });

}