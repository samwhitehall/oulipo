app.views.OptionsView = Backbone.View.extend({
    el: '#options',
    template: _.template($('#options-template').html()),
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));

        /* add tooltip label to advance_by sliders */
        this.$('input[type="range"]').on('input', function() {
            var el = $(this);
            var outputElem = el.prev('output');
            
            var value = el.val();
            if (value > 0) {
                value = '+' + value;
            }

            outputElem.text(value);
        });

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

