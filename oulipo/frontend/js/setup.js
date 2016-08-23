app.poem = new app.models.Poem({
    'options': {
        'advance_by__verb': 0,    
        'advance_by__noun': 0    
    },
    'raw_text': 'hello cat i am a dog',
});

app.poemView = new app.views.PoemView();
app.optionsView = new app.views.OptionsView({
    model: app.poem.get('options')
});

app.poem.on('sync', app.poemView.reset, app.poemView);
app.poem.on('sync', app.optionsView.render, app.optionsView);

app.poem.save();
