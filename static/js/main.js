
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
  
  
    /*==================================================================
    [ Validate ]*/
    /*var input = $('.validate-input .input100');

     /*$('.validate-form').on('submit',function(){
         var check = true;

         for(var i=0; i<input.length; i++) {
             if(validate(input[i]) == false){
                 showValidate(input[i]);
                 check=false;
             }
         }

         return check;
     });*/


     /*$('.validate-form .input100').each(function(){
         $(this).focus(function(){
            hideValidate(this);
         });
     });

     function validate (input) {
         if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
             if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                 return false;
             }
         }
         else {
             if($(input).val().trim() == ''){
                 return false;
             }
         }
     }

     function showValidate(input) {
         var thisAlert = $(input).parent();
     $(thisAlert).addClass('alert-validate');
 }

     function hideValidate(input) {
         var thisAlert = $(input).parent();

         $(thisAlert).removeClass('alert-validate');
     }
    
    /*==================================================================
    [ Show pass ]*/
    /*var showPass = 0;
    $('.btn-show-pass').on('click', function(){
        if(showPass == 0) {
            $(this).next('input').attr('type','text');
            $(this).addClass('active');
            showPass = 1;
        }
        else {
            $(this).next('input').attr('type','password');
            $(this).removeClass('active');
            showPass = 0;
        }
        
    });*/

})(jQuery);

$(document).ready(function() {
    $("#testButton").click(function() {
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

   $("#inputImage").change(function () {
        $("#testResultContainer").attr("hidden", "true");
        $("#validationContainer").attr("hidden", "true");
        $("#validateLossContainer").attr("hidden", "true");
    })
});