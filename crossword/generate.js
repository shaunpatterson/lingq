function generate_puzzle() {

}

function random_puzzle_layout() {
    // Just one for now
    layout1 = 
        [
    "......_...._...",
    "......_...._...",
    "......_...._..."
    /*"___........_...",*/
    /*"..._.....___...",*/
    /*"....._.....____",*/
    /*"....._...._....",*/
    /*"......___......",*/
    /*"...._..........",*/
    /*"____....._.....",*/
    /*"....._....._...",*/
    /*"......_.....___",*/
    /*"........_......",*/
    /*"..._...._......",*/
    /*"..._...._......"*/
        ];

    return layout1;

}

function is_layout_complete(layout) {
    for (var i = 0; i < rows.length; i++) {
        row = rows[i];
        for (var j = 0; j < row.length; j++) {
            if (row[j] == ".") {
                return false;
            }
        }
    }

    console.log("Puzzle complete");
    return true;
}

function find_next_open(layout) {

    for (var i = 0; i < rows.length; i++) {
        row = rows[i];
        for (var j = 0; j < row.length; j++) {
            if (row[j] == ".") {
                return { y : i , x : j };
            }
        }
    }

    return { x : -1, y : -1 };
}

function find_length(layout, x, y) {
    row = layout[y];

    var len = 0;
    for (var i = x; i < row.length; i++) {
        if (row[i] == '_') {
            return len;
        }
        len++;
    }

    return len;
}

function fill_layout(layout, words) {
   
    var i = 0;

    while (!is_layout_complete(layout) && i < 5000) {
        result = false;

        while(result == false) {
            pos = find_next_open(layout);
            len = find_length(layout, pos['x'], pos['y']);
            console.log("Next length to fill: " + len);
           
            found_words = find_words_with_length(words, len);
            random_word = choose(found_words);
            console.log(random_word);
            old_layout = layout.slice(0);
            layout = fill_layout_with_word(layout, pos['x'], pos['y'], random_word);

            result = check_verticals(layout, pos['x'], pos['y'], random_word.length, words);
            if (result == true) {
                // Words still fit
            } else {
                // Words do not fit. Revert to old layout
                layout = old_layout;
            }

            console.log(pos);
        }
        /*console.log(len);*/


        i++;
    }

    return layout;
}

function check_verticals(layout, x, y, len, words) {
    // First find the "top" of the vertical word
    yStart = y;
    while (yStart > 0 && layout[yStart][x] != "_") {
        yStart--;
    }
    console.log("y start: " + yStart);
   
    // Now find the bottom
    yEnd = y;
    while (yEnd < layout.length && layout[yEnd][x] != "_") {
        yEnd++;
    }
    console.log("y end: " + yEnd);

    // Now build a regular expression
    regEx = "^";
    for (var i = yStart; i < yEnd; i++) {
        regEx += layout[i][x];
    }
    regEx += "$";
    regEx = new RegExp(regEx, 'i');
    console.log(regEx);
    
    // Find any matching words
    matchingWords = [];
    for (var word in words) {
        if (word.match(regEx)) {
            matchingWords.push(word);
        }
    }

    if (matchingWords.length == 0) {
        // No possible words now fit in the vertical.  Abort!
        return false;
    }

    return true;

}

function find_words_with_length(words, len) {
    found_words = [];
    for (var word in words) {
        if (word.length == len) {
            found_words.push(word);
        }
    }
    console.log("Found " + found_words.length + " words with length " + len);
    return found_words;
}

function choose(array) {
    console.log("Choosing among: " + array.length);
    var key = Math.floor(Math.random() * array.length);
    console.log("key: " + key + " : " + array[key]);
    return array[key];
}

function fill_layout_with_word(layout, x, y, word) {
    row = layout[y];

    new_row = row.slice(0, x).concat(word).concat(row.slice(x + word.length));
    console.log("old row:'" + row + "'");
    console.log("New row:'" + new_row + "'");
    layout[y] = new_row;
    return layout;
}

$(function() {
    lingqs = get_lingqs();
    
    words = {};
    for (var i = 0; i < lingqs.length; i++) {
        words[lingqs[i]['term']] = lingqs[i]['hint'];
    }
        
    rows = random_puzzle_layout();
    rows = fill_layout(rows, words);

    text = "";
    console.log(rows);
    console.log(JSON.stringify(rows));
    for (var i = 0; i < rows.length; i++) {
        text += rows[i] + "\n";
    }
    console.log(text);


    $('#row').html($('<pre>' + text + '</pre>'));

});
