lingqs = null;

function getLingQs(lang, apiKey) {
    url = 'http://www.lingq.com/api_v2/' + lang + '/lingqs/?apikey=' + apiKey;
    $.ajax({ url : url,
             type: 'get',
             dataType: 'jsonp',
             crossDomain: true,
             success: function(data) {
                 lingqs = data;
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
    $('#hint').css({'margin-top':$(document).height()/8+'px'});
   
    lang = _GET('lang');
    speed = _GET('speed');
    apiKey = _GET('apikey');

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

});
