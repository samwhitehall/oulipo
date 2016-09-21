app.views.OptionsView = Backbone.View.extend({
    el: '#options',
    template: _.template($('#options-template').html()),
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    events: {
        'input input[type="range"]': 'update'
    },
    update: function(e) {
        this.setAdvanceBy(e.target.id);

        app.poem.save(app.poem.toJSON(), {
            wait: true
        });
    },
    setAdvanceBy: function(parameter) {
        var inputElem = this.$('#' + parameter);
        var outputElem = inputElem.prev('output');

        var amount = inputElem.val();

        var options = app.poem.get('options');
        options.set(parameter, amount);

        if (amount > 0) {
            amount = '+' + amount;
        }
        outputElem.text(amount);
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

