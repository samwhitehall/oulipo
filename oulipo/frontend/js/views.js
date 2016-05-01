(function ($, Backbone, _, app) {
    var TemplateView = Backbone.View.extend({
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },

        render: function () {
            html = this.template();
            this.$el.html(html);
        }
    });

    var HomeView = TemplateView.extend({
        tagName: 'div',
        templateName: '#new-poem'
    })

    app.views.HomeView = HomeView;
})(jQuery, Backbone, _, app);
