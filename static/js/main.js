
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
})(jQuery);

$(document).ready(function() {
    $("#testButton").click(function() {
        console.log("click")
        var formData = new FormData();
        var images = $("#inputImage")[0].files;
        
        if(images.length > 0) {
            formData.append('image', images[0]);
            
            $.ajax({
                url: '/test',
                type: 'post',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                success: function(response) {
                    $("#testResult").html(response.result);
                    $("#testResultContainer").removeAttr("hidden");
                    $("#validationContainer").removeAttr("hidden");
                }
                
            })
        }
    });

    $("#validateButton").click(function() {
        var formData = new FormData();
        var images = $("#inputImage")[0].files;
        var classes = {"infected": 0, "uninfected": 1};
        if(images.length > 0) {
            formData.append('image', images[0]);
            formData.append('result', classes[$('#testResult').text()]);

            $.ajax({
                url: '/validate',
                type: 'post',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                success: function(response) {
                    $("#validateLoss").html(response.loss);
                    $("#validateLossContainer").removeAttr("hidden");
                }
            })
        }
    });

    $("#syncButton").click(function() {
        $("#loading").removeAttr("hidden");
        $.ajax({
            url: '/sync',
            type: 'get',
            data: {
                'name': window.location.search.substring(1).split("=")[1],
            },
            success: function(response) {
                $("#loading").attr("hidden", "true");
                $("#synchronised").removeAttr("hidden");
            }
        });
    })

   $("#inputImage").change(function () {
        $("#testResultContainer").attr("hidden", "true");
        $("#validationContainer").attr("hidden", "true");
        $("#validateLossContainer").attr("hidden", "true");
        $("#loading").attr("hidden", "true");
        $("#synchronised").attr("hidden", "true");
    })
});
