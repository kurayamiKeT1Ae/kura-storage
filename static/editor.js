const brackets = {
    "{": "}",
    "}": "{",

    "]": "[",
    "[": "]",

    ")": "(",
    "(": ")",

    "'": "'",
    '"': '"',
    "`": "`"
};

const code_editor = document.getElementById('code-editor');

function moveCursor(position){
    code_editor.selectionStart = position;
    code_editor.selectionEnd = position;
}

function get_last_line(text, cursor_pos){
    const last_n = text.lastIndexOf("\n", cursor_pos - 1);

    if (last_n === -1){
        return text.slice(0, cursor_pos);
    } 
    return text.slice(last_n + 1, cursor_pos);
}

function handle_chars_after(char, cbefore=null){
    if (!(char in brackets)){
        return 0;
    }
    if (cbefore !== null && brackets[char] !== cbefore){
        return 0;
    }
    return char === "]" || char === "}" || char === ")" ? 1 : 0;
}

function handle_chars_before(char, cafter=null){
    if (!(char in brackets)){
        return 0;
    }
    if (cafter !== null && brackets[char] !== cafter){
        return 0;
    }
    return char === "[" || char === "{" || char === "(" ? 1 : 0;
}

function add_between(start_pos, end_pos, inserted_text, text){
    // if starting pos and ending pos eq -> there is no selected text to delete
    const before_cursor = text.slice(0, start_pos);
    const after_cursor = text.slice(end_pos);

    if (inserted_text !== "\t" && start_pos !== end_pos){
        const before = text.slice(0, start_pos);
        const highlight = text.slice(start_pos, end_pos);
        const after = text.slice(end_pos);

        return {
            text: `${before}${inserted_text[0]}${highlight}${inserted_text[1]}${after}`,
            steps: highlight.length + 1
        }
    }
    
    return {
        text: `${before_cursor}${inserted_text}${after_cursor}`,
        steps: 1
    }
}


code_editor.addEventListener("keydown", (event) => {

    // console.log(event.code);
    const start_pos = code_editor.selectionStart; // get start selection
    const end_pos = code_editor.selectionEnd; // get end selection 
    const text = code_editor.value; // get the text-area value

    // handle () {} [] "" '' `` auto close brackets
    if (event.code === "Digit9" && event.shiftKey){ // 9 + shift => (
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "()", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }

    else if (event.code === "BracketLeft" && event.shiftKey){ // [ + shift => {
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "{}", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }

    else if (event.code === "BracketLeft"){ // [
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "[]", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }

    else if (event.code === "Quote" && event.shiftKey){ // ' + shift => "
        event.preventDefault();
        const result = add_between(start_pos, end_pos, '""', text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }
    

    else if (event.code === "Quote"){ // '
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "''", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }

    else if (event.code === "Backquote"){ // `
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "``", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
    }


    // handle enter \n
    if (event.code === "Enter") {
        event.preventDefault();

        const last_line = get_last_line(text, start_pos);
        const last_char = text[start_pos - 1];
        const cchar = text[start_pos];

        let tab_times = 0;

        for (const char of last_line) {
            if (char !== "\t") {
                break;
            }

            tab_times++;
        }

        const base_tabs = tab_times;
        const inside_tabs = base_tabs + handle_chars_before(last_char, cchar);
        const before_cursor = text.slice(0, start_pos);
        const after_cursor = text.slice(end_pos);
        const inserted_text = "\n" + "\t".repeat(inside_tabs);
        const new_cursor_pos = start_pos + inside_tabs+1;

        let after_insert = "";
        if (handle_chars_after(cchar, last_char)) {
            after_insert = "\n" + "\t".repeat(base_tabs);
        }

        code_editor.value = `${before_cursor}${inserted_text}${after_insert}${after_cursor}`;

        moveCursor(start_pos + inserted_text.length);

    }

    // handle tab \t
    if (event.code === "Tab"){
        event.preventDefault();
        const result = add_between(start_pos, end_pos, "\t", text)
        const result_text = result.text;
        const steps = result.steps;
        code_editor.value = result_text;
        moveCursor(start_pos + steps);
        
        
    }

});