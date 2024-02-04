
$(document).ready(function () {
    result_hide();
    load_bg();
});

function covid_warning_bg () {
    $("#main-bg").removeClass("bg-success");
    $("#main-bg").addClass("bg-danger");
}

function normal_warning_bg () {
    $("#main-bg").removeClass("bg-danger");
    $("#main-bg").addClass("bg-success");
}
function load_bg () {
    $("#main-bg").removeClass();
}

function result_hide () {
    $("#result-show").hide();
    $("#predict-button").hide();
}
function result_show () {
    $("#result-show").show();
}

function predict_button_show () {
    $("#predict-button").show();
}

let base64Image;
$("#image-selector").change(function () {
    result_hide();
    let reader = new FileReader();
    reader.onload = function (e) {
        let dataURL = reader.result;
        $('#selected-image').attr("src", dataURL);
        base64Image = dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
        //console.log(base64Image);
    };
    reader.readAsDataURL($("#image-selector")[0].files[0]);
    $("#result").text("");
    $("#probability").text("");
    predict_button_show();
});

$("#predict-button").click(function () {

    let message = {
        image: base64Image
    };

    result_show();
    $.post("http://127.0.0.1:5000/predict", JSON.stringify(message),
        function (response) {
            let result = response.prediction.result;
            $("#result").text(result);
            $("#probability").text(response.prediction.accuracy);
            if (result === "Covid19 Negative") {
                normal_warning_bg();
            }
            if (result === "Covid19 Positive") {
                covid_warning_bg();
            }
            console.log(response);
        });


});