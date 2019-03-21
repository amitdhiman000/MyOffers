
const TOOL_SELECT = 0;
const TOOL_CROP = 1;
const TOOL_TRANSFORM = 2;

class App {
    constructor() {
        this.tool = TOOL_SELECT;
        this.stage = new Stage("stage");
        this.docs = [];
        this.currDoc = null;
        this.callbacks = {};
        this.undoStack = [];
        this.redoStack = [];
    }

    newDoc() {
        this.hideDoc();
        this.currDoc = new Doc(this.stage, 500, 500);
        this.docs.push(this.currDoc);
        this.currDoc.show();
        return this.currDoc;
    }

    switchDoc(index) {
        this.hideDoc();
        this.currDoc = this.docs[index];
        this.currDoc.show();
    }

    hideDoc() {
        if (this.currDoc && this.currDoc.hide());
    }

    saveFile() { }

    importFile() { }

    exportFile() { }

    undo() { }

    redo() { }
};

class Stage {
    constructor(id) {
        this.$view = $('#' + id);
        this.$view.css({ 'width': 700, 'height': 700, 'overflow': 'scroll' })
    }

    setBGColor(hex) {
        this.$view.css({ 'background-color': hex });
    }
};

class Canvas {
    constructor(stage, w, h) {
        this.stage = stage;
        this.$view = $('<div class="canvas" ><form method="post" enctype="multipart/form-data" class="I_form ajax-form" >' + $AppData.csrfField() + '<input type="file" name="I_file" class="I_file" style="display:none;" /> <input type="hidden" name="I_x" class="I_x" /> <input type="hidden" name="I_y" class="I_y" /> <input type="hidden" name="I_width" class="I_width" /><input type="hidden" name="I_height" class="I_height" /></form></div>');
        this.setSize(w, h);
        this.images = [];
        this.$fileInput = this.$view.find(".I_file");
        this._init();
        this.canvasData = null;
        this.cropBoxData = null;
    }

    setBGColor(hex) {
        this.$view.css({ 'background-color': hex });
    }

    setSize(w, h) {
        this.width = w;
        this.height = h;
        this.$view.css({ 'width': w, 'height': h });
    }

    detach() {
        this.$view.detach();
        this.$view.hide();
    }
    attach() {
        this.stage.$view.html(this.$view);
        this.$view.show();
    }

    selectFile() {
        this.$fileInput.click();
    }

    saveFile() {
        console.log("+saveFile");
        var $image = this.$view.find('.I_image');
        var cropData = $image.cropper("getData");
        this.$view.find(".I_x").val(cropData["x"]);
        this.$view.find(".I_y").val(cropData["y"]);
        this.$view.find(".I_height").val(cropData["height"]);
        this.$view.find(".I_width").val(cropData["width"]);
        this.$view.find(".I_form").submit();
    }

    cropFile() {
        console.log("+cropFile");
        var This = this;
        var $image = this.$view.find('.I_image');
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function () {
                $image.cropper("setCanvasData", This.canvasData);
                $image.cropper("setCropBoxData", This.cropBoxData);
            }
        });
    }

    _readFile(event, files) {
        console.log('+_readFile');
        var This = this;
        var reader = new FileReader();
        reader.onload = function (e) {
            console.log("loading image");
            var $image = $('<img src="" class="I_image" style="position: absolute;" />');
            $image.attr("src", e.target.result);
            This.$view.append($image);
            This.images.push(e.target.result);
        }
        reader.readAsDataURL(files[0]);
    }

    _init() {
        var readFileCB = this._readFile.bind(this);
        this.$view.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
        }).on('drop', function (e) {
            var droppedFiles = e.originalEvent.dataTransfer.files
            readFileCB(e, droppedFiles);
        });

        this.$fileInput.on('change', function (e) {
            readFileCB(e, this.files);
        });
    }
};

class Doc {
    constructor(stage, w, h) {
        this.selection = { x: -1, y: -1 };
        this.canvas = new Canvas(stage, w, h);
    }

    hide() {
        this.canvas.detach();
    }

    show() {
        this.canvas.attach();
    }
};