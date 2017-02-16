'use strict';

var templates = [],
    originalQuestion = '',
    templateText = '',
    NUM_ROW = 10,
    BodyNode = document.getElementsByTagName('body')[0], 
    ArgTableNode,
    PreviewNode,
    ConfirmationNode,
    TableCache = {}; // cache already entered text

/* upload to the backend
    url - link to the webpage.
    question - the question turkers ask
    data - a list of dicts, each dict is key-value pairs that are arguments of the question.
 */
function upload(url, question, data) {
    removeTable();
    removePreview();
    question = JSON.stringify(question);
    data = JSON.stringify(data);
    var code = md5(question + data);
    var submission = {
        'url': url,
        'question': question,
        'data': data,
        'code': code
    };
    console.log(submission);
    $.post('/submit', submission, 
        function(response) {
            console.log('uploaded: ', response);
        });
    return code;
}

/*
 * Better alert message
 */
function swal_html(title, text, type) {
    swal({
        title: title,
        text: text,
        type: type,
        html: true
    });
}

/* add instant key change to question template
 */
document.TurkerInput.Question.oninput = parseTemplate;

function removeTable() {
    if (ArgTableNode) {
        BodyNode.removeChild(ArgTableNode);
        ArgTableNode = undefined;
    }
}

function removePreview() {
    if (PreviewNode) {
        BodyNode.removeChild(PreviewNode);
        PreviewNode = undefined;
    }
    if (ConfirmationNode) {
        BodyNode.removeChild(ConfirmationNode);
        ConfirmationNode = undefined;
    }
}

function parseTemplate() {
    removeTable();
    removePreview();
    checkWebsite();
    var is_valid = getTemplates(document.TurkerInput.Question);
    // console.log(templates);
    if (!is_valid) 
        return false;

    createTableForm();
    return true;
}

/*
 * We don't want yelp.com anymore
 */
function checkWebsite() {
    var website = document.TurkerInput.Website.value;
    if (!website) {
        swal({title: 'Website field cannot be blank!', type:'error'});
        return;
    }
    if (website.includes("yelp.com")) {
        swal_html('Be creative!',
                  'Please do not use <a>yelp.com</a> or its subdomains. Think of a more interesting website.',
                  'error');
        return;
    }
    return website;
}

function hasDuplicates(array) {
        return (new Set(array)).size !== array.length;
}

function getTemplates(question) {
    var reg = /\(([^)]+)\)/g;
    var qu = originalQuestion = question.value;
    var matches = qu.match(reg);
    if (!matches) {
        // alert('You must have at least one (...) template');
        // question.value = '';
        return false;
    }
    templates = [];
    matches.forEach(
        function (s) { templates.push(s.slice(1, -1)); }
    );
    if (hasDuplicates(templates)) {
        swal_html('Duplicate blank descriptions',
             'The template <b>must not have duplicate blank descriptions</b>.<br>For example, <i>"What is the best (place) around (place)?"</i> is not allowed. <br>You have to provide different descriptions: <i>"What is the best (dining place) around (tourist attraction)</i>?"',
             'error');
        return false;
    }
    templateText = qu.replace(reg, '<span class="highlighter">{}</span>');
    return true;
}

function createTableForm() {
    // table for question template instantiation
    ArgTableNode = createNode('form', BodyNode,
                          ['name', 'ArgTable', 
                          'onsubmit', 'submitForm(); return false;']);

    var table = createNode('table', ArgTableNode);
    //table.setAttribute('border', '1');
    var firstrow = createNode('tr', table);
    for (var i = 0; i < templates.length; i++) {
        var entry = createNode('td', firstrow);
        entry.innerHTML = '<b>' + templates[i] + '</b>';
        // addTextNode(entry, templates[i]);
    }

    for (var r = 0; r < NUM_ROW; r++) {
        var row = createNode('tr', table);
        for (var c = 0; c < templates.length; c++) {
            var entry = createNode('td', row);
            var inputnode = createNode('input', entry,
                                       ['type', 'text', 
                                       'name', 'input-'+r+'-'+c, 
                                       'style', 'width:250px']);
            inputnode.onclick = inputnode.oninput = previewTable;
            if (templates[c] in TableCache)
                inputnode.value = TableCache[templates[c]][r];
        }
    }
    var div = createNode('div', table);
    addNewLine(div);
    //var button = createNode('button', div, ['type', 'button', 'onclick', 'previewTable()']);
    //addTextNode(button, 'Preview completed questions');

    var instruction = createNode('tr', ArgTableNode, ['class', 'example']);
    instruction.innerHTML = 'A live preview will appear below as you fill out the table. The values you\'ve entered will be preserved, so feel free to change the question template if you need to.<br>Please <b>carefully verify</b> the completed questions before you click "submit". You will receive a confirmation code after submission.';
}

function previewTable() {
    removePreview();

    if (templates.length < 2) {
        swal_html('Not enough blanks', 
             'You must have <b>at least two blanks</b> in the question template!', 
             'error');
        return;
    }

    for (var c = 0; c < templates.length; c++)
        TableCache[templates[c]] = [];
    var matrix = [];
    for (var r = 0; r < NUM_ROW; r++) {
        var row = [];
        for (var c = 0; c < templates.length; c++) {
            var val = document.ArgTable['input-'+r+'-'+c].value;
            if (val)
                row.push(val);
            else
                row.push('___');
            TableCache[templates[c]].push(val);
        }
        matrix.push(row);
    }
    // console.log(matrix);
    // display
    /*
    PreviewNode = createNode('ul', BodyNode);
    for (var r = 0; r < NUM_ROW; r++) {
        var entry = createNode('li', PreviewNode);
        entry.innerHTML = strformat(templateText, ...matrix[r]);
        // addTextNode(entry, strformat(templateText, ...matrix[r]));
    }
    */
    PreviewNode = createNode('table', BodyNode, ['class', 'roundrect']);
    var PreviewNode_ = createNode('table', PreviewNode, ['class', 'collapsed']);
    for (var r = -1; r < NUM_ROW; r++) {
        var entry = createNode('tr', PreviewNode_);
        if (r == -1) {
            entry = createNode('td', entry);
            entry.innerHTML = '<h2><b>Preview completed question</b></h2>';
        } else {
            entry = createNode('td', entry, ['class', 'tdborder']);
            entry.innerHTML = strformat(templateText, ...matrix[r]);
        }
    }

    addNewLine(PreviewNode_);
    var submitButton = createNode('a', PreviewNode_, ['class', 'fancybutton']);
    submitButton.innerHTML = '<span>Submit</span>';
    // addTextNode(button2, 'Submit');
    submitButton.onclick = submitForm;

    return matrix;
}

function submitForm() {
    var matrix = previewTable();
    var D = []; // list of dicts of blank args
    for (var r = 0; r < matrix.length; r++) {
        var entry = {};
        for (var c = 0; c < templates.length; c++) {
            if (matrix[r][c] === '___') {
                swal_html('Missing value', 
                     'Please fill out all the blanks.<br>Missing value at <b>row ' + (r+1) + ' and column ' + (c+1) + '</b>',
                     'error');
                return;
            }
            entry[templates[c]] = matrix[r][c];
        }
        D.push(entry);
    }

    // check duplicate in rows
    var check_dup_row = [];
    matrix.forEach(
        function (row) { check_dup_row.push(JSON.stringify(row)); }
    );
    if (hasDuplicates(check_dup_row)) {
        swal_html('Duplicate rows',
             'There are duplicates in the table!<br>Please make sure each row is unique.',
             'error');
        return;
    }

    var website = checkWebsite();
    if (!website) return;

    var code = upload(website, originalQuestion, D);
    ConfirmationNode = createNode('p', BodyNode);
    ConfirmationNode.innerHTML = 'Your submission code is <br><br><span class="highlighter">' + code + '</span><br><br>Please copy and paste it back to the Amazon Mechanical Turk page. <br>Thanks for your participation! We really appreciate your time.';
    swal('Thanks!', 
         'You have successfully completed the task. Please copy and paste the submission code back to the Amazon Mechanical Turk page.',
         'success');
}

function createNode(name, ancestor, attrs) {
    var node = document.createElement(name);
    if (attrs)
        for (var i = 0; i < attrs.length; i += 2) {
            node.setAttribute(attrs[i], attrs[i+1]);
        }
    if (ancestor)
        ancestor.appendChild(node);
    return node;
}

function addNewLine(ancestor) {
    var mybr = document.createElement('br');
    ancestor.appendChild(mybr);
    return ancestor;
}

function addTextNode(ancestor, text) {
    ancestor.appendChild(document.createTextNode(text));
    return ancestor;
}

function strformat(s) {
    var i = 1, args = arguments;
    return s.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};
