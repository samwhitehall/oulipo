(function ($, Backbone, _, app) {

    var AppRouter = Backbone.Router.extend({
        routes: {
            '': 'home'
        },

        initialize: function (options) {
            this.contentElement = '#content';
            this.current = null;
            Backbone.history.start();
        },

        render: function (view) {
            if (this.current) {
                this.current.undelegateEvents();
                this.current.$el = $();
                this.current.remove();
            }

            this.current = view;
            this.current.render();
        },

        // views
        home: function () {
            var view = new app.views.HomeView({el: this.contentElement});
            this.render(view);
        }
    });
    
    app.router = AppRouter;

})(jQuery, Backbone, _, app);
