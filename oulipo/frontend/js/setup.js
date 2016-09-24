app.poem = new app.models.Poem({
    'options': {
        'advance_by__verb': 0,    
        'advance_by__noun': 0    
    },
    'raw_text': 'she came from Greece, she had a thirst for knowledge,\n' +
                'she studied sculpture at St Martin\'s College,\n' +
                'that\'s where I caught her eye'
});

app.poemView = new app.views.PoemView();
app.optionsView = new app.views.OptionsView({
    model: app.poem.get('options')
});

app.poem.on('sync', app.poemView.reset, app.poemView);
app.optionsView.render();

// add de-select handlers to body
$(document).on('click', function() { app.poemView.deselectCurrent(); }); 
$(document).on('keypress', function(e) { 
    if (e.keyCode == 27)  // escape key
        app.poemView.deselectCurrent(); 
}); 

// exit edit mode without saving
$(document).on('keypress', function(e) { 
    if (e.keyCode == 27)  // escape key
        app.poemView.exitEditMode(); 
}); 

app.poem.save();
