var gulp = require('gulp');
var jsFiles = ['*.js', 'src/**/*.js'];
var jshint = require('gulp-jshint');
var jscs = require('gulp-jscs');
var nodemon = require('gulp-nodemon');

gulp.task('style', function() {
    return gulp.src(jsFiles)
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish', {
            verbose: true 
        }))
        .pipe(jscs());
});

gulp.task('inject', function() {
    var wiredep = require('wiredep').stream;
    var inject = require('gulp-inject');
    var options = {
        bowerJson: require('./bower.json'),
        directory: './public/lib',
        ignorePath: '../../public'
    };
    var injectSrc = gulp.src(['./public/js/*.js', './src/css/*.css'], {read: false});
    var injectOptions = {
        ignorePath: ['/public','/src/css/']
    };
    return gulp.src('./src/views/*.html')
                .pipe(wiredep(options))
                .pipe(inject(injectSrc, injectOptions))
                .pipe(gulp.dest('./src/views'));
});

gulp.task('serve', ['style', 'inject'], function() {
    var options = {
        script: 'trend.js',
        delayTime: 1,
        env: {
            'PORT': 3000
        },
        watch: jsFiles
    };
    return nodemon(options)
        .on('restart', function(ev) {
            console.log('Restarting...');
    });
});