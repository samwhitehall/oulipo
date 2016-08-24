module.exports = function(grunt) {
    // configure grunt
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // js linting
        jshint: {
            options: {
                reporter: require('jshint-stylish')
            },
            build: ['js/*.js']
        },

        // js minification & concatenation
        concat: {
            options: {
                banner: '/* <%= pkg.name %> v<%= pkg.version %> by <%= pkg.author %> */\n'
            },
            build: {
                src: [
                    'js/vendor/jquery.*.js', 
                    'js/vendor/underscore.*.js', 
                    'js/vendor/backbone.*.js', 
                    'js/vendor/backbone-deep-model.*.js', 
                    'js/app.js', 
                    'js/models.js', 
                    'js/views.js', 
                    'js/setup.js'
                ],
                dest: 'oulipo.js'
            }
        },

        // sass compilation
        sass: {
            dist: {
                files: {'style/main.css': 'style/main.scss'}
            }
        },
        
        // configure watch for auto-updating
        watch: {
            script: {
                files: 'js/**/*.js',
                tasks: ['jshint', 'concat']
            },
            css: {
                files: 'style/**/*.scss',
                tasks: ['sass']
            }
        }

    });

    // load grunt plugins
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // register tasks
    grunt.registerTask('default', ['jshint', 'concat']);
};
