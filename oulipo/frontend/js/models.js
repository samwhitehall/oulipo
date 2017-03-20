app.models.Options = Backbone.Model.extend({
    defaults: {
        advance_by__noun: 0,
        advance_by__verb: 0
    },
    resetSilently: function() {
        this.set('advance_by__noun', 0, {silent: true});
        this.set('advance_by__verb', 0, {silent: true});
    },
});

app.models.Token = Backbone.Model.extend({
    defaults: {
        original_word: '',
        category: 'other',
        offset: ''
    }
});

app.models.Poem = Backbone.DeepModel.extend({
    url: app.config.api_host + '/poem/',
    defaults: {
        title: '',
        raw_text: '',
        tokens: []
    }
});
