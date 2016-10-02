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
    events: {
        'click #edit': 'toggleEdit'
    },
    editMode: false,
    selectedToken: null,
    addToken: function(token) {
        var view = new app.views.TokenView({model: token});
        var $tokenListEl = $('#token-list');
        $tokenListEl.append(view.render().el);

        // Remove any spaces between the HTML tags
        var cleanedHTML = $tokenListEl.html().replace('> <', '><');
        $tokenListEl.html(cleanedHTML);
    },
    reset: function() {
        this.$('#edit a').html('edit');
        this.$('#token-list').html('');
        tokens = app.poem.get('tokens');
        tokens.forEach(this.addToken, this);

        this.$('#poem-title').html('<h2>' + app.poem.get('title') + '</h2>');
    },
    deselectCurrent: function(e) {
        if (this.selectedToken !== null)
            $('#tray').remove();
        
        this.selectedToken = null;
    },
    toggleEdit: function(e) {
        app.poemView.deselectCurrent();
        app.poemView.editMode = !app.poemView.editMode;

        if (app.poemView.editMode) {
            var height = $('#token-list').height();

            var textArea = document.createElement('textarea');
            textArea.id = 'raw-text';
            $(textArea).height(height);
            $(textArea).html(app.poem.get('raw_text'));

            this.$('#token-list').html(textArea);
            this.$('#edit a').html('save');

            var titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = app.poem.get('title');
            this.$('#poem-title').html(titleInput);
        }
        else {
            var title = $('#poem-title input').val();
            var rawText = $('#raw-text').val();

            app.poem.set('title', title);
            app.poem.set('raw_text', rawText);
            app.poem.unset('tokens');
            

            app.poem.save({wait: true});
        }
    },
    exitEditMode: function(e) {
        if (app.poemView.editMode)
            app.poemView.editMode = false;
            app.poemView.reset();
    }
});

