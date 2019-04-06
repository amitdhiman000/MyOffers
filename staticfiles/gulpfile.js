const path = require("path");
const gulp = require("gulp");
const browserify = require("browserify");
const source = require('vinyl-source-stream');
const tsify = require("tsify");
const uglify = require('gulp-uglify');
const terser = require('gulp-terser');
const rename = require('gulp-rename');
const sourcemaps = require('gulp-sourcemaps');
const buffer = require('vinyl-buffer');
const del = require('del');



const baseDir = path.resolve(__dirname, "static_dirs/desktop");

const input_config = {
	tsConfigPath: path.resolve(baseDir, "ts/tsconfig.json"),
	srcFilesPath: [path.resolve(baseDir, "ts")],
	entryFilePath: path.resolve(baseDir, "ts/index.ts"),
}

const output_config_es5 = {
	outputName: "index.js",
    outputPath: path.resolve(baseDir, "tsfy/es5"),
};

const output_config_es6 = {
    outputName: "index.js",
    outputPath: path.resolve(baseDir, "tsfy/es6"),
};

gulp.task('clean', function (done) {
    del([path.resolve(input_config.srcFilesPath, "/*.d.ts")]);
    done();
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

gulp.task("build", gulp.parallel("clean", "build_es5", "build_es6"), function(done) { done(); });

gulp.task("default", gulp.series("build"));

gulp.watch(input_config.srcFilesPath, gulp.series("build"));
