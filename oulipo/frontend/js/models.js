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
    url: function() {
        root = 'http://localhost:8000/poem/';
        slug = this.get('slug');

        if (slug)
            return root + slug + '/';

        return root;
    },
    //idAttribute: 'slug',
    defaults: {
        title: '',
        raw_text: '',
        options: new app.models.Options(),
        tokens: []
    },
    getURL: function() {
        slug = this.get('slug');
        noun = this.get('options').get('advance_by__noun');
        verb = this.get('options').get('advance_by__verb');

        return '#poem/' + slug + '/n' + noun + '/v' + verb;
    }
});
