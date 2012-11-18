$(function() {

    cw = new Crossword(10, 10, 10, [['blah', 'clue'], ['bla', 'clu']]);

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
    this.available_words = available_words;

    console.log("Starting");
    this.randomize_word_list();
    this.clear_grid();

}

Crossword.prototype.randomize_word_list = function() {
    console.log("Randomizing list");
    console.log(this.available_words);
    temp_list = [];
    for (var i = 0; i < this.available_words.length; i++) {
        var word = this.available_words[i];
        console.log(word);
        if (word instanceof Word) {
            temp_list.push(new Word(word.word, word.clue));
        } else {
            temp_list.push(new Word(word[0], word[1]));
        }
    }
    temp_list.shuffle();
    temp_list.sort(function (a,b) { return a.length < b.length });

    console.log(temp_list);
    this.available_words = temp_list;

}

Crossword.prototype.clear_grid = function() {
    this.grid = [];
    for (var i = 0; i < this.rows; i++) {
        ea_row = [];
        for (var j = 0; j < this.cols; j++) {
            ea_row.push('');
        }
        this.grid.push(ea_row);
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

