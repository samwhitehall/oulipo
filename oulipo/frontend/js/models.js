app.models.Options = Backbone.Model.extend({
    defaults: {
        advance_by__noun: 0,
        advance_by__verb: 0
    }
});

app.models.Token = Backbone.Model.extend({
    defaults: {
        content: '',
        category: 'other'
    }
});

app.models.Poem = Backbone.DeepModel.extend({
    url: 'http://localhost:8000/poem/',
    defaults: {
        title: '',
        raw_text: '',
        options: new app.models.Options(),
        tokens: []
    }
});
