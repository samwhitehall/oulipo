var AppRouter = Backbone.Router.extend({
    routes: {
        '': 'home',
        'poem/:id/n:noun/v:verb/': 'view'
    },
    home: function() {
        app.poem = new app.models.Poem({
            'title': 'A Poem',
            'options': {
                'advance_by__verb': 0,    
                'advance_by__noun': 0    
            },
            'raw_text': 'Just type your initial poem, in here, click save'
        });
        app.poem.save();
    },
    view: function(id, noun, verb) {
        app.poem = new app.models.Poem({
            'slug': id,
            'options': {
                'advance_by__verb': noun,    
                'advance_by__noun': verb    
            },
        });
        app.poem.fetch();
    }
});

$(document).ready(function() {
    var router = new AppRouter();

    app.poemView = new app.views.PoemView();
    Backbone.history.start();

    app.optionsView = new app.views.OptionsView({
        model: app.poem.get('options')
    });

    app.poem.on('sync', app.poemView.reset, app.poemView);
    app.optionsView.render();

    // exit edit mode without saving
    $(document).on('click', function() { app.poemView.exitEditMode(); }); 
    $(document).on('keypress', function(e) { 
        if (e.keyCode == 27)  // escape key
            app.poemView.exitEditMode(); 
    }); 
});
