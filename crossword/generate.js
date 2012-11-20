/**
  * Javascript translation based on the work of
  *
  * Bryan Helmig
  * bryanhelmig.com
  */

$(function() {

    cw = new Crossword(10, 10, 10, [['blah', 'clue'], ['bla', 'clu']]);
    cw.compute_crossword(1 * 1000, 2);

});

/** Word object */
function Word(word, clue) {

    this.word = word.replace(/\s/g).toLowerCase();
    this.clue = clue;
    this.length = word.length;
    this.row = undefined;
    this.col = undefined;
    this.vertical = undefined;
    this.number = undefined;

    function down_across() {
        if (this.vertical) {
            return "down";
        } else {
            return "across";
        }
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
    temp_list.sort(function (a,b) { return a.length < b.length });

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
                if ($.inArray(word, copy.available_words) == false) {
                    copy.fit_and_word(word);
                }
            }
            x++;
            
        }
            
        if (copy.current_word_list.length > this.current_word_list) {
            this.current_word_list = copy.current_word_list;
            this.grid = copy.grid;
        }

        count++;
    }

    console.log("Computed");

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
                    if (row - glc > 0) {
                        if ((rowc - glc) + word.length <= this.rows) {
                            coordlist.push([colc, rowc - glc, 1, colc + (rowc - glc)]);
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

    new_coordlist.shuffle();

    // Put best scores first
    new_coordlist.sort(function (a,b) { return a[4] > b[4] });
    return new_coordlist;
}

Crossword.prototype.fit_and_word = function(word) {
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
            var vertical = cooldlist[count][2];

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
        var letter = word[i];

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

Crossword.prototype.set_word = function(col, row, value, force) {
    if (force) {
        word.col = col;
        word.row = row;
        word.vertical = vertical;

        this.current_word_list.push(word);

        for (var i = 0; i < word.word.length; i++) {
            var letter = word.word[i];

            this.set_cell(col, row, letter);
            if (vertical) {
                row++;
            } else {
                col++;
            }
        }

    } else {
        // Do nothing??
    }
}

Crossword.prototype.set_cell = function(col, row, value) {
    this.grid[row-1][col-1] = value;
}

Crossword.prototype.get_cell = function(col, row) {
    return this.grid[row-1][col-1];
}

Crossword.prototype.check_if_cell_clear = function(col, row) {

    if (col <= 0 || row <= 0) {
        return false;
    }

    var cell = this.get_cell(col, row);
    if (cell == this.empty) {
        return true;
    }

    return false;
}

Crossword.prototype.order_number_words = function() {
    this.current_word_list.sort(function (a,b) { return (a.col + a.row) < (b.col + b.row); });
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


Array.prototype.shuffle = function () {
    for (var i = this.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = this[i];
        this[i] = this[j];
        this[j] = tmp;
    }

    return this;
}


