

function getLingQs(lang, apiKey, success) {
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
                                 lingqs.push([this['term'], this['hint']]);
                             }
                         });
                     }
                 });

                 success(lingqs);
             },
             error: function() {
                alert("Failed to get LingQs");
             }
    });

}
