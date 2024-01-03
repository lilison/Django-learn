var self_alert = function(msg, type) {
    if (typeof(type) == "undefined") {
        type = "success";
    }
    var divElement = $(`<div class="alert alert-${type}  fade show role="alert" style="text-align: center;">
                <span class="alert-inner--icon"><i class="fas fa-exclamation"></i></span>
                <span class="alert-inner--text"><strong>${msg}</strong> ${msg}</span>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
    </div>`);
    divElement.css({
        "position": "absolute",
        "width":"100%",
        "top": "50px",
        "left": "50%", // 改为水平居中
        "transform": "translate(-50%, -50%)", 
    });
    $('body').append(divElement);
    return divElement;
};
