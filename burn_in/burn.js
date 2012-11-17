lingqs = null;

function getLingQs(lang, apiKey) {
    url = 'http://www.lingq.com/api_v2/' + lang + '/repetition-lingqs/?apikey=' + apiKey;
    $.ajax({ url : url,
             type: 'get',
             dataType: 'jsonp',
             crossDomain: true,
             success: function(data) {
                 // Format: Date : [linqgs]
                 // Flatten them out
                 lingqs = [];
                 $.each(data, function() {
                     // 'this' is the date
                     if (this != null) {
                         $.each(this, function() {
                             // 'this' is a lingq
                             if (this != null) {
                                 lingqs.push(this);
                             }
                         });
                     }
                 });
             },
             error: function() {
                alert("Failed to get LingQs");
             }
    });

}

$(function() {

    // Full screen content
    $('#content').css({'height':$(document).height()+'px'});

    // 1/3rd screen height word and hint
    $('#word').css({'height':$(document).height()/3+'px'});
    $('#hint').css({'height':$(document).height()/4+'px'});

    $('#word').css({'margin-top':$(document).height()/8+'px'});
    /*$('#hint').css({'margin-top':$(document).height()/16+'px'});*/
    // Closer?
    $('#hint').css({'margin-top':'-'+$(document).height()/32+'px'});

    $('#go').click(function() {
        start();
    });

    $('#show').click(function () {
        $('#control ul').show();
        $(this).hide();
    }).hide();
});


function start() {
   
    lang = $('#lang').val();
    speed = $('#speed').val(); 
    apiKey = $('#apikey').val();

<<<<<<< HEAD
=======
    alert(apiKey + " " + speed + " " + lang);

>>>>>>> master
    // Load the LingQs
    getLingQs(lang, apiKey);
	

    // Display changer 
    jQuery.fn.timer = function() {
        if (lingqs == null) {
            $('#word span').text("Loading...");
            $('#hint span').text("Loading...");
        } else {
            // Here we go!
            var key = Math.floor(Math.random() * lingqs.length);
            
            lingq = lingqs[key];

            $('#word span').text(lingq['term']);
            $('#hint span').text(lingq['hint']);
        }
    
        $('.jtextfill').textfill({ maxFontPixels: 300, innerTag: 'span' });
    }


    window.setInterval(function() { 
        $(document).timer();
    }, speed);

    $('#control ul').hide();
    $('#show').show();

}
