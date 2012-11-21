/**
  * Javascript translation based on the work of
  *
  * Bryan Helmig
  * bryanhelmig.com
  *
  * Used and modified with permission
  */

/** Word object */
function Word(word, clue) {

    this.word = word.replace(/\s/g).toUpperCase();
    this.clue = clue;
    this.length = word.length;
    this.row = undefined;
    this.col = undefined;
    this.vertical = undefined;
    this.number = undefined;
}

Word.prototype.down_across = function() {
    if (this.vertical) {
        return "down";
    } else {
        return "across";
    }
}

/** Crossword puzzle object */
function Crossword(cols, rows, maxloops, available_words) {
    this.cols = cols;
    this.rows = rows;
    this.maxloops = maxloops;
    this.empty = "_";
    this.available_words = available_words;

    this.randomize_word_list();
    this.current_word_list = [];
    this.clear_grid();

}

Crossword.prototype.randomize_word_list = function() {
    temp_list = [];
    for (var i = 0; i < this.available_words.length; i++) {
        var word = this.available_words[i];
        if (word instanceof Word) {
            temp_list.push(new Word(word.word, word.clue));
        } else {
            temp_list.push(new Word(word[0], word[1]));
        }
    }
    temp_list.shuffle();
    temp_list.sort(function (a,b) { return (a.length - b.length) });

    this.available_words = temp_list;

}

Crossword.prototype.clear_grid = function() {
    this.grid = [];
    for (var i = 0; i < this.rows; i++) {
        ea_row = [];
        for (var j = 0; j < this.cols; j++) {
            ea_row.push(this.empty);
        }
        this.grid.push(ea_row);
    }
}

Crossword.prototype.compute_crossword = function(time_permitted, spins)
{
    time_permitted = parseFloat(time_permitted);

    var count = 0;
    var copy = new Crossword(this.cols, this.rows, this.maxloops, this.available_words);

    var date = new Date();
    var start_full = date.getTime();
    while ((new Date().getTime() - start_full) < time_permitted || count == 0)
    {
        copy.current_word_list = [];
        copy.clear_grid();
        copy.randomize_word_list();

        var x = 0;
        while (x < spins) 
        {
            for (var i = 0; i < copy.available_words.length; i++) 
            {
                var word = copy.available_words[i];
                if ($.inArray(word, copy.current_word_list) < 0) {
                    copy.fit_and_add(word);
                }
            }
            x++;
            
        }

        if (copy.current_word_list.length > this.current_word_list.length) {
            this.current_word_list = copy.current_word_list;
            this.grid = copy.grid;
        }

        count++;
    }

    console.log("Computed");

    /** 
      * Okay, so there's a weird bug in the generation code.  TODO: Explain
     */
    downs = {};
    acrosses = {};
    pruned_word_list = [];
    
    this.current_word_list.sort(function (a,b) { return ((a.col + a.row) - (b.col + b.row)); });
   
    // Very inefficient way of doing this.  TODO: Change 
    for (var i = 0; i < this.current_word_list.length; i++) {
        var word = this.current_word_list[i];

        for (var j = i + 1; j < this.current_word_list.length; j++) {
            var word_to_test = this.current_word_list[j];

            if ($.inArray(word_to_test, pruned_word_list) >= 0) {
                // Skip this word
                continue;
            }

            if (word.col == word_to_test.col && word.row == word_to_test.row && word.vertical == word_to_test.vertical && word.length < word_to_test.length) {
                word = word_to_test;
                i = j + 1;
            }
        }
        pruned_word_list.push(word);
    }

    this.current_word_list = pruned_word_list;

    return;
}

Crossword.prototype.suggest_coord = function(word) {
    var count = 0;
    var coordlist = [];
    var glc = -1;

    for (var i = 0; i < word.word.length; i++) {
        var given_letter = word.word[i];

        glc++;
        var rowc = 0;
        for (var rowIndex = 0; rowIndex < this.grid.length; rowIndex++) {
            var row = this.grid[rowIndex];
            rowc++;
            var colc = 0;

            for (var colIndex = 0; colIndex < row.length; colIndex++) {
                var cell = row[colIndex];
                colc++;

                if (given_letter == cell) {
                    
                    if (rowc - glc > 0) {
                        if (((rowc - glc) + word.word.length) <= this.rows) {
                            coordlist.push([colc, rowc - glc, 1, colc + (rowc - glc)])
                        }
                    }

                    if (colc - glc > 0) {
                        if ((colc - glc) + word.length <= this.cols) {
                            coordlist.push([colc - glc, rowc, 0, rowc + (colc - glc)]);
                        }
                    }
                }
            }
        }
    }

    var new_coordlist = this.sort_coordlist(coordlist, word);
    return new_coordlist;
}

Crossword.prototype.sort_coordlist = function(coordlist, word) {
    var new_coordlist = [];

    for (var i = 0; i < coordlist.length; i++) {
        var coord = coordlist[i];

        var col = coord[0];
        var row = coord[1];
        var vertical = coord[2];

        var fit_score = this.check_fit_score(col, row, vertical, word);
        coord.push(fit_score);

        if (fit_score) {
            new_coordlist.push(coord);
        }
    }

    // Put best scores first
    new_coordlist.sort(function (a,b) { return (a[4] - b[4]) });
    return new_coordlist;
}

Crossword.prototype.fit_and_add = function(word) {
    var fit = false;
    var count = 0;
    var coordlist = this.suggest_coord(word);

    while (!fit && count < this.maxloops) {
        if (this.current_word_list.length == 0) {
            // This is the first word.  THe seed
            var vertical = Math.floor(Math.random() * 2);
            var col = 1;
            var row = 1;

            if (this.check_fit_score(col, row, vertical, word)) {
                fit = true;
                this.set_word(col, row, vertical, word, true);
            }
        } else {
            if (count >= coordlist.length) return;
            var col = coordlist[count][0];
            var row = coordlist[count][1];
            var vertical = coordlist[count][2];

            if (coordlist[count][4]) {
                fit = true;
                this.set_word(col, row, vertical, word, true);
            }

        }

        count++;
    }

    return;
}

Crossword.prototype.check_fit_score = function(col, row, vertical, word) {
    
    if (col < 1 || row < 1) {
        return 0;
    }

    var count = 1;
    var score = 1;

    for (var i = 0; i < word.length; i++) {
        var letter = word.word[i];

        if (col >= this.cols || row >= this.rows) {
            return 0;
        }
            
        var active_cell = this.get_cell(col, row);

        if (active_cell == this.empty || active_cell == letter) {
            // pass
        } else {
            return 0;
        }

        if (active_cell == letter) {
            score++;
        }

        if (vertical) {
            // Check surroundings
            if (active_cell != letter) {
                // Don't check surroundings if cross point
                if (!this.check_if_cell_clear(col + 1, row)) {
                    return 0;
                }

                if (!this.check_if_cell_clear(col - 1, row)) {
                    return 0;
                }
            }

            if (count == 1) {
                if (!this.check_if_cell_clear(col, row - 1)) {
                    return 0;
                }
            }

            if (count == word.length) {
                if (!this.check_if_cell_clear(col, row + 1)) {
                    return 0;
                }
            }

            row++;
        } else {

            if (active_cell != letter) {
                // Don't check surroundings if cross point
                if (!this.check_if_cell_clear(col, row - 1)) {
                    return 0;
                }

                if (!this.check_if_cell_clear(col, row + 1)) {
                    return 0;
                }
            }

            if (count == 1) {
                if (!this.check_if_cell_clear(col - 1, row)) {
                    return 0;
                }
            }

            if (count == word.length) {
                if (!this.check_if_cell_clear(col + 1, row)) {
                    return 0;
                }
            }

            col++;
        }

        count++;
    }

    return score;
}

Crossword.prototype.set_word = function(col, row, vertical, word, force) {
    if (force) {
        word.col = col;
        word.row = row;
        word.vertical = vertical;


        for (var i = 0; i < word.word.length; i++) {
            var letter = word.word[i];

            this.set_cell(col, row, letter);
            if (vertical) {
                row++;
            } else {
                col++;
            }
        }
        
        this.current_word_list.push(word);

    } else {
        // Do nothing??
    }
}

Crossword.prototype.set_cell = function(col, row, value) {
    this.grid[row-1][col-1] = value;
}

Crossword.prototype.get_cell = function(col, row) {

    var wrappedRow = row - 1;
    if (wrappedRow < 0) {
        wrappedRow = this.grid.length - 1;
    }

    var wrappedCol = col - 1;
    if (wrappedCol < 0) {
        wrappedCol = this.grid[wrappedRow].length - 1;
    }

    if (this.grid == undefined) {
        alert('undefined grid');
    }
    
    if (wrappedRow >= this.grid.length) {
        alert('greater than grid length: row' + row + " wr" + wrappedRow + " grid: " + this.grid.length);
    }

    if (wrappedCol >= this.grid[0].length) {
        alert("greater than col length");
    }


    return this.grid[wrappedRow][wrappedCol];
}

Crossword.prototype.check_if_cell_clear = function(col, row) {

    if (col < 0 || row < 0) {
        return false;
    }

    var cell = this.get_cell(col, row);
    if (cell == this.empty) {
        return true;
    }

    return false;
}

Crossword.prototype.order_number_words = function() {
    this.current_word_list.sort(function (a,b) { return ((a.col + a.row) - (b.col + b.row)); });
    var count = 1;
    var icount = 1;

    for (var i = 0; i < this.current_word_list.length; i++) {
        var word = this.current_word_list[i];

        word.number = count;
        if (icount < this.current_word_list.length) {
            if (word.col == this.current_word_list[icount].col && 
                word.row == this.current_word_list[icount].row) 
            {
                // pass
            } else {
                count++;
            }
        }

        icount++;
    }
}

Crossword.prototype.display = function() {
    var output = [];
    this.order_number_words();

    for (var i = 0; i < this.current_word_list.length; i++) {
        var word = this.current_word_list[i];
        output.push({ x : word.col - 1, y : word.row - 1, num : word.number });
        this.set_cell(word.col, word.row, word.number);
    }
        
    return output;
}

Crossword.prototype.solution = function() {
    rows = [];
    for (var r = 0; r < this.rows; r++) {
        var row = this.grid[r];
        var rowOutput = "";
        for (var c = 0; c < row.length; c++) {
            rowOutput += row[c];
        }
        rows.push(rowOutput)
    }

    return { "row" : rows };
}

Crossword.prototype.legend = function() {
    var across = [];
    var down = [];

    for (var i = 0; i < this.current_word_list.length; i++) {
        var word = this.current_word_list[i];

        if (word.down_across() == "across") {
            across.push({ "no" : word.number, "text" : word.clue});
        } else {
            down.push({ "no" : word.number, "text" : word.clue});
        }
    }

    return { "down" : down, "across" : across };
}


Array.prototype.shuffle = function () {
    for (var i = this.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = this[i];
        this[i] = this[j];
        this[j] = tmp;
    }

    return this;
}


