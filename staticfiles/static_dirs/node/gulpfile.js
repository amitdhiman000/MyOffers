var gulp = require("gulp");
var browserify = require("browserify");
var source = require('vinyl-source-stream');
var tsify = require("tsify");
var uglify = require('gulp-uglify');
var terser = require('gulp-terser');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var buffer = require('vinyl-buffer');
var del = require('del');


let input_config = {
	tsConfigPath: '../desktop/ts/tsconfig.json',
	srcFilesPath: ['../desktop/ts/'],
	entryFilePath: '../desktop/ts/AppMain.ts'
}

var output_config_es5 = {
	outputName: 'index.js',
    outputPath: '../desktop/tsfy/es5'
};

var output_config_es6 = {
    outputName: 'index.js',
    outputPath: '../desktop/tsfy/es6'
};

gulp.task('clean', function () {
    //return del([paths.tempDst]);
});


gulp.task("build_es5", function (done) {
    browserify({
        debug: true,
        entries: input_config.entryFilePath,
        cache: {},
        packageCache: {}
    })
    .plugin(tsify, { target: 'es5' })
    .bundle()
    .pipe(source(output_config_es5.outputName))
    .pipe(buffer())
    .pipe(gulp.dest(output_config_es5.outputPath))
    .pipe(rename({ extname: '.min.js' }))
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(terser())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(output_config_es5.outputPath));
    done();
});

gulp.task("build_es6", function (done) {
    browserify({
        debug: true,
        entries: input_config.entryFilePath,
        cache: {},
        packageCache: {}
    })
    .plugin(tsify, { target: 'es6' })
    .bundle()
    .pipe(source(output_config_es6.outputName))
    .pipe(buffer())
    .pipe(gulp.dest(output_config_es6.outputPath))
    .pipe(rename({ extname: '.min.js' }))
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(terser())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(output_config_es6.outputPath));
    done();
});

gulp.task("build", gulp.parallel("build_es5", "build_es6"), function(done) { done(); });

gulp.task("default", gulp.series("build"));

gulp.watch(input_config.srcFilesPath, gulp.series("build"));
