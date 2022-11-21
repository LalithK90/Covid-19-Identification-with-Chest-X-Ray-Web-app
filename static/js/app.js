
$(document).ready(function () {
    result_hide();
});

function result_hide () {
    $("#result-show").hide();
} function result_show () {
    $("#result-show").show();
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

});

$("#predict-button").click(function () {
    let message = {
        image: base64Image
    };
    // console.log(message);

    if (message == null) {
        console.log("sdsad");
        window.alert("There is no selected image");
    } else {
        result_show();
        $.post("http://127.0.0.1:5000/predict", JSON.stringify(message),
            function (response) {
                $("#result").text(response.prediction.result);
                $("#probability").text(response.prediction.accuracy.toFixed(2));
                console.log(response);
            });
    }

});