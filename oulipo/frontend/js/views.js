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
    },
    events: {
        'click': 'select'
    },
    select: function(e) {
        var currentlySelected = (app.poemView.selectedToken === this.model);
        app.poemView.deselectCurrent();

        if (currentlySelected)
            return;

        app.poemView.selectedToken = this.model;
        e.stopPropagation();  // don't bubble to background (and deselect)

        var tray = new app.views.SelectedTokenTrayView({model: this.model});
        this.$el.append(tray.render().el);
    }
});

app.views.SelectedTokenTrayView = Backbone.View.extend({
    tagName: 'span',
    id: 'tray',
    template: _.template($('#selected-token-tray-template').html()),
    render: function() {
        this.$el.html(this.template(this.model));

        // disable button for current type
        var elemName = '.' + this.model.category;
        this.$el.find(elemName).attr('disabled', true);

        // handler for updating component
        this.$el.find('button').on('click', this.setCategory);

        return this;
    },
    setCategory: function(e) {
        category = e.srcElement.className;

        app.poemView.selectedToken.category = category;
        app.poem.save();
    }
});

app.views.PoemView = Backbone.View.extend({
    el: '#poem-view',
    selectedToken: null,
    addToken: function(token) {
        var view = new app.views.TokenView({model: token});
        var $tokenListEl = $('#token-list');
        $tokenListEl.append(view.render().el);

        // Remove any spaces between the HTML tags
        var cleanedHTML = $tokenListEl.html()
            .replace('\s*', '')
            .replace('\>\<', '> <')
            ;
        $tokenListEl.html(cleanedHTML);
    },
    reset: function() {
        this.$('#token-list').html('');
        tokens = app.poem.get('tokens');
        tokens.forEach(this.addToken, this);
    },
    deselectCurrent: function(e) {
        if (this.selectedToken !== null)
            $('#tray').remove();
        
        this.selectedToken = null;
    }
});

