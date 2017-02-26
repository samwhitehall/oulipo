app.views.OptionsView = Backbone.View.extend({
    el: '#options',
    template: _.template($('#options-template').html()),
    render: function() {
        var context = this.model.toJSON();
        context.disabled = app.poemView.editMode;

        this.$el.html(this.template(context));
        this.updateLabel('noun');
        this.updateLabel('verb');
        return this;
    },
    events: {
        'input input[type="range"]': 'update'
    },
    updateLabel: function(pos) {
        var elem = $('output.' + pos);
        var value = this.model.get('advance_by__' + pos);
        var sign = value > 0 ? '+' : '';

        elem.html(sign + value);
    },
    update: function(e) {
        var options = app.poem.get('options');
        options.set(_.escape(e.target.id), _.escape(e.target.value));

        app.poem.save(app.poem.toJSON(), {
            wait: true
        });
        app.optionsView.updateLabel('noun');
        app.optionsView.updateLabel('verb');
    },
    reset: function() {
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

        this.$('#poem-title').html('<h2>' + app.poem.escape('title') + '</h2>');
    },
    toggleEdit: function(e) {
        app.poemView.editMode = !app.poemView.editMode;

        if (app.poemView.editMode) {
            var height = $('#token-list').height();
            if (!height)
                height = '100px';

            var textArea = document.createElement('textarea');
            var text = app.poem.escape('raw_text');
            textArea.id = 'raw-text';
            $(textArea).height(height);
            $(textArea).html(text);

            this.$('#token-list').html(textArea);
            this.$('#edit a').html('save');

            var headerWidth = $('#poem-title h2').width();
            var editButtonWidth = $('h3#edit').width();
            var newWidth = headerWidth - editButtonWidth - 12;

            var titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = app.poem.get('title');
            titleInput.style.width = newWidth + 'px';
            this.$('#poem-title').html(titleInput);

            // reset options
            app.poem.get('options').reset();
            app.optionsView.render();

            // don't bubble to document by clicking on title/text/save/edit
            $(titleInput).click(function(e) { return false; });
            $(textArea).click(function(e) { return false; });

            return false;
        }
        else {
            var oldText = app.poem.get('raw_text');
            var title = $('#poem-title input').val();
            var rawText = $('#raw-text').val();

            app.poem.set('title', title);

            if (rawText != oldText) {
                app.poem.set('raw_text', rawText);
                app.poem.unset('tokens');
            }

            app.poem.save({wait: true});
            app.optionsView.render();
            
            // don't also bubble up and call exitEditMode
            return false;
        }
    },
    exitEditMode: function(e) {
        if (app.poemView.editMode) {
            app.poemView.editMode = false;
            app.poemView.reset();
            app.optionsView.render();
        }
    }
});

