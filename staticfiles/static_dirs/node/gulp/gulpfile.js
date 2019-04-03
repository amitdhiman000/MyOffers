var gulp = require("gulp");
var browserify = require("browserify");
var source = require('vinyl-source-stream');
var tsify = require("tsify");
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var buffer = require('vinyl-buffer');


gulp.task('clean', function () {
    return gulp
        .src([
            './tmp/',
        ], { read: false })
        .pipe(clean());
});


gulp.task("default", ["clean"], function () {
    return browserify({
        basedir: '.',
        debug: true,
        entries: ['src/AppFw.ts'],
        cache: {},
        packageCache: {}
    })
    .plugin(tsify)
    .bundle()
    .pipe(source('AppFw.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(uglify())
    .pipe(sourcemaps.write('./js'))
    .pipe(gulp.dest("./js"));
});
