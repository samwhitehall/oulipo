app.views.OptionsView = Backbone.View.extend({
    el: '#options',
    template: _.template($('#options-template').html()),
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    events: {
        'click .update': 'update'
    },
    update: function(e) {
        options = app.poem.get('options');

        noun = this.$('#advance_by__noun').val();
        verb = this.$('#advance_by__verb').val();

        options.set('advance_by__noun', noun);
        options.set('advance_by__verb', verb);

        app.poem.save(app.poem.toJSON(), {
            wait: true
        });
    }
});

app.views.TokenView = Backbone.View.extend({
    tagName: 'span', 
    className: 'token',
    template: _.template($('#token-template').html()),
    render: function() {
        this.$el.html(this.template(this.model));
        this.$el.addClass(this.model.category);
        return this;
    }
});

app.views.PoemView = Backbone.View.extend({
    el: '#poem',
    addToken: function(token) {
        var view = new app.views.TokenView({model: token});
        $('#token-list').append(view.render().el);
    },
    reset: function() {
        this.$('#token-list').html('');
        tokens = app.poem.get('tokens');
        tokens.forEach(this.addToken, this);
    }
});

