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
            prod: {
                src: [
                    'js/vendor/jquery.*.js', 
                    'js/vendor/underscore.*.js', 
                    'js/vendor/backbone.*.js', 
                    'js/vendor/backbone-deep-model.*.js', 
                    'js/app.js', 
                    'js/config.prod.js', 
                    'js/models.js', 
                    'js/views.js', 
                    'js/setup.js'
                ],
                dest: 'oulipo.prod.js'
            },
            dev: {
                src: [
                    'js/vendor/jquery.*.js', 
                    'js/vendor/underscore.*.js', 
                    'js/vendor/backbone.*.js', 
                    'js/vendor/backbone-deep-model.*.js', 
                    'js/app.js', 
                    'js/config.dev.js', 
                    'js/models.js', 
                    'js/views.js', 
                    'js/setup.js'
                ],
                dest: 'oulipo.js'
            }
        },

        uglify: {
            my_target: {
                files: {'oulipo.js': ['oulipo.prod.js']}
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
                tasks: ['jshint', 'concat:dev']
            },
            css: {
                files: 'style/**/*.scss',
                tasks: ['sass']
            }
        },

        // remove generated files
        clean: ['oulipo.js', 'style/main.css']
    });

    // load grunt plugins
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');

    // register tasks
    grunt.registerTask('default', ['concat:prod', 'uglify', 'sass']);
};
