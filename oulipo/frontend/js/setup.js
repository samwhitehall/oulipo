app.poem = new app.models.Poem({
    'title': 'The Road Not Taken',
    'raw_text': 'Two roads diverged in a yellow wood,\n' + 
                'And sorry I could not travel both\n' + 
                'And be one traveler, long I stood\n' + 
                'And looked down one as far as I could\n' + 
                'To where it bent in the undergrowth;\n' + 
                '\n' + 
                'Then took the other, as just as fair,\n' + 
                'And having perhaps the better claim,\n' + 
                'Because it was grassy and wanted wear;\n' + 
                'Though as for that the passing there\n' + 
                'Had worn them really about the same,\n' + 
                '\n' + 
                'And both that morning equally lay\n' + 
                'In leaves no step had trodden black.\n' + 
                'Oh, I kept the first for another day!\n' + 
                'Yet knowing how way leads on to way,\n' + 
                'I doubted if I should ever come back.\n' + 
                '\n' + 
                'I shall be telling this with a sigh\n' + 
                'Somewhere ages and ages hence:\n' + 
                'Two roads diverged in a wood, and I—\n' + 
                'I took the one less traveled by,\n' + 
                'And that has made all the difference.'
});

app.poemView = new app.views.PoemView();
app.optionsView = new app.views.OptionsView({
    model: app.poem.get('options')
});

// set default advance_by (noun: -2, verb: 3)
app.poem.get('options').set('advance_by__noun', 1);
app.poem.get('options').set('advance_by__verb', -3);

// hide/show spinner depending on if loading
var timer = null;
var ongoingRequests = 0;
app.poem.on('request', function() { 
    if (ongoingRequests === 0)
        timer = window.setTimeout(function() { $('#spinner').show(); }, 200);
    ongoingRequests += 1;
});
app.poem.on('sync', function() { 
    ongoingRequests -= 1;
    if (ongoingRequests === 0) {
        $('#spinner').hide();
        window.clearTimeout(timer);
    }
});

app.poem.on('sync', app.poemView.reset, app.poemView);
app.optionsView.render();

// exit edit mode without saving
$(document).on('click', function() { app.poemView.exitEditMode(); }); 
$(document).on('keypress', function(e) { 
    if (e.keyCode == 27)  // escape key
        app.poemView.exitEditMode(); 
}); 

app.poem.save();
