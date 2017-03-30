var KEY_ENTER = 13;
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;

var wsuggest = function(Elem, opts) {
	console.log('+wsuggest');
	console.log('element : '+Elem.prop("tagName"));
	var Inst = this;
	Inst.kd = {
		_ui: null,
		_count: 0,
		_jsonData: null,
		_selectedItem: null,
		_selectedIndex: 0,
	};

	Inst.kf = {
		minLength: 1,
		delay: 0,
		_create: function(e) {
			console.log('+_create');
			kd._ui = $('<ul class="ui-search-list ui-search-list-app" >');
			kd._ui.css({width: Elem.css('width')});
			Elem.after(kd._ui);
			kd._ui.on('mouseenter', 'li', kf._itemHover);
			Elem.on("keyup", kf._keyUp);
			Elem.on("keypress", kf._keyPress);
			Elem.on("focus", kf._onfocus);
			Elem.on("blur", kf._onunfocus);
		},
		_destroy: function(e) {
			kd._ui.remove();
			kd._ui = null;
		},
		_onfocus: function(e) {
			kd._ui.show();
		},
		_onunfocus: function(e) {
			kd._ui.hide();
		},
		_source: function(key, resp) {
			console.log('implement _source function');
		},
		_parse: function(jsonData) {
			console.log('+_parse');
			kd._ui.html('');
			if (jsonData.length > 0) {
				var count = 0;
				for (i in jsonData) {
					kd._ui.append(kf._itemCreate(jsonData[i]));
					count++;
				}
				kd._jsonData = jsonData;
				kd._count = count;
				kd._selectedIndex = 0;
				kd._selectedItem = kd._ui.children().eq(kd._selectedIndex).addClass('ui-search-item-a');
				kd._ui.show();
			} else {
				kd._count = 0;
				kd._selectedIndex = 0;
				kd._ui.html('<div class="ui-search-item">No search results</div>');
				kd._ui.show();
			}
		},
		_itemCreate: function(item) {
			console.log('implement _itemCreate function');
			return '';
		},
		_itemHover: function(e) {
			console.log('+_itemHover');
			var index = $(this).index();
			console.log('old selected : '+ kd._selectedIndex);
			console.log('new selected : '+ index);
			if (kd._selectedIndex != index) {
				kd._ui.children().eq(kd._selectedIndex).removeClass('ui-search-item-a');
				kd._selectedIndex = index;
				kd._ui.children().eq(kd._selectedIndex).addClass('ui-search-item-a');
				if (kd._jsonData) {
					kf._itemSelect(Elem, kd._jsonData[index]);
				}
			}
		},
		_itemSelect: function(input, item) {
			 console.log('implement _itemSelect function');
		},
		_itemSelectCurrent: function() {
			if (kd._count > 0 && kd._jsonData) {
				kf._itemSelect(Elem, kd._jsonData[kd._selectedIndex]);
			}
		},
		_onEnter: function(e) {
			console.log('+_onEnter');
			kf._itemSelectCurrent();
			kf._onunfocus();
		},
		_keyPress: function(e) {
			console.log('+_keyPress : '+ e.keyCode);
			if (e.keyCode === 10 || e.keyCode === 13) {
				e.preventDefault();
				e.data = Inst;
				kf._onEnter(e);
			}
		},
		_keyUp: function(e) {
			console.log('+_keyUp');
			var handled = false;
			switch(e.keyCode) {
			case KEY_UP:
				if (kd._selectedIndex > 0) {
					kd._ui.children().eq(kd._selectedIndex).removeClass('ui-search-item-a');
					kd._selectedIndex--;
					var child = kd._ui.children().eq(kd._selectedIndex).addClass('ui-search-item-a');
					var cont = kd._ui;
					cont.scrollTop(child.position().top + cont.scrollTop());
					//cont.scrollTop(child.offset().top - cont.offset().top + cont.scrollTop());
					if (kd._jsonData) {
						kf._itemSelect(Elem, kd._jsonData[kd._selectedIndex]);
					}
				}
				handled = true;
				break;
			case KEY_DOWN:
				if (kd._selectedIndex < kd._count - 1) {
					kd._ui.children().eq(kd._selectedIndex).removeClass('ui-search-item-a');
					kd._selectedIndex++;
					var child = kd._ui.children().eq(kd._selectedIndex).addClass('ui-search-item-a');
					var cont = kd._ui;
					//console.log("child top : "+ child.position().top);
					//console.log("scroll top : "+ cont.scrollTop());
					cont.scrollTop(child.position().top + cont.scrollTop());
					if (kd._jsonData) {
						kf._itemSelect(Elem, kd._jsonData[kd._selectedIndex]);
					}
				}
				handled = true;
				break;
			case KEY_ENTER:
				handled = true;
				break;
			case KEY_LEFT:
			case KEY_RIGHT:
			default:
				console.log('keycode : '+e.keyCode);
				handled = false;
			}

			if (handled) {
				e.preventDefault();
				return;
			}
			var key = Elem.val();
			(key.length >= kf.minLength && kf._source(key, kf._parse));
		},
	};

	var kf = Inst.kf;
	var kd = Inst.kd;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
};


function wfileupload(Elem, opts)
{
	console.log('+wfileupload');
	console.log('Tag : '+Elem.prop('tagName'));
	var Inst = this;
	// klass data
	Inst.kd = {
		_ui: null,
		_uploads: [],
		_hidden: null,
	};
	// klass functors
	Inst.kf =  {
		maxFiles: 1,
		mimeType: 'image',
		maxSize: 1024, // 1KB
		_create: function(e) {
			console.log('+_create');
			kd._ui = $('<div class="progress-div" ></div>');
			kd._ui.css({width: Elem.css('width')});
			kd._hidden = $('<input type="hidden" name="files" value="" >');
			Elem.before(kd._hidden);
			Elem.after(kd._ui);
			Elem.on('change', kf._upload);
		},
		_destroy: function(e) {
			console.log('+_destroy');
			kd._ui.remove();
			kd._hidden.remove();
		},
		_upload: function(e) {
			console.log('+_upload');
			e.stopPropagation(); // Stop stuff happening
			e.preventDefault(); // Totally stop stuff happening
			var lThis = this;
			var lfiles = $(lThis)[0].files;
			var count = kd._ui.find('.progress-outer').length;
			console.log('count : '+count);
			var rem = kf.maxFiles - count;
			if (rem == 0) {
				lThis.value = '';
				console.log('Already attached to max limit');
				return;
			}

			if (rem > lfiles.length) {
				rem = lfiles.length;
			}
			for (var i = 0; i < rem; ++i) {
				console.log('name : '+ lfiles[i].name + ' data : '+lfiles[i]);
				kf._uploadFile(lThis, lfiles[i]);
			}
		},
		_uploadFile: function(lThis, file) {
			console.log('+_uploadFile');
			var fdata = new FormData();
			fdata.append(file.name, file);
			var fileName = file.name;
			//(fileName.length > 20 && (fileName = fileName.substring(0, 20)));

			var uiItem = $('<div class="progress-outer" >'
				+'<div class="progress-inner">'
				+'<div class="progress-filename">'+fileName+'</div>'
				+'<div class="progress-bar">&nbsp;0%</div></div>'
				+'<div class="progress-control">'
				+'<button class="ui-btn">Cancel</button>'
				+'</div></div>');
			var uiBtn = uiItem.find('.ui-btn');
			uiBtn.on('click', kf._cancel);
			kd._ui.append(uiItem);
			var request = $.ajax({
				url: '/upload/fileupload/',
				type: 'post',
				data: fdata,
				cache: false,
				dataType: 'json',
				processData: false,
				contentType: false,
				xhr: function() {
					var xhr = jQuery.ajaxSettings.xhr();
					//Upload progress
					xhr.upload.addEventListener("progress", function(evt){
						if (evt.lengthComputable) {
							var percent = 100*(evt.loaded / evt.total);
							percent = parseInt(percent);
							kf._progress(percent);
						}
					}, false);
					return xhr;
				},
				success: function(jsonData, status, xhr) {
					if(!jsonData.error) {
						console.log("upload finished");
						var id = jsonData.data.upload_id;
						kd._uploads.push(id);
						kd._hidden.val(kd._uploads.toString());
						uiBtn.data('request', null);
						uiBtn.data('upload_id', id);
						uiBtn.text('Remove');
						console.log('ids : '+kd._uploads.toString());
					} else {
						// Handle errors here
						console.log('ERRORS: ' + JSON.stringify(data.error));
						uiItem.remove();
					}
				},
				error: function(xhr, status, errorThrown) {
					console.log('ERRORS: ' + status);
					uiItem.remove();
				},
				complete: function(res) {
					// This function is called at last for cleanup
					console.log('+comeplete :'+ res.status);
					lThis.value = '';
				},
			});
			uiBtn.data('request', request);
		},
		_cancel: function(e) {
			console.log('+_cancel');
			e.preventDefault();
			var lThis = $(this);
			console.log(lThis.text());
			if (lThis.text() == 'Cancel') {
				var request = lThis.data('request');
				request.abort();
				console.log('aborted');
			} else {
				var id = lThis.data('upload_id');
				var index = kd._uploads.indexOf(id);
				kd._uploads.splice(index, 1);
				kd._hidden.val(kd._uploads);
				console.log('ids : '+kd._uploads.toString());
			}
			lThis.parents('.progress-outer').remove();
		},
		_progress: function(progress) {
			console.log('progress : '+progress+'%');
			var progressbar = kd._ui.find('.progress-bar');
			progressbar.css({width: progress+'%'});
			progressbar.html(progress+'%');
		}
	};

	var kd = Inst.kd;
	var kf = Inst.kf;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
}

jQuery.fn.fileupload = function(options) { new wfileupload(this, options); }
jQuery.fn.suggestions = function(options) { new wsuggest(this, options); }
