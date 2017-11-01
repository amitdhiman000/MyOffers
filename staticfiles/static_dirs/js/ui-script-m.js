var KEY_ESCAPE = 27
var KEY_ENTER = 13;
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;

$(function() {
	console.log("+init");

	$(document).on('submit', 'form.ajax-form', ajaxFormSubmit);
	/*Initialize History*/
	initHistory();
	/*Initialize search*/
	initSearch();
	/*Initialize switchTabs*/
	initSwitchTabs();
	/*Initialize App*/
	initApp();

	console.log("-init");
});

function dumpObject(obj)
{
	var output = '';
	for (var property in obj) {
		output += property + ': ' + obj[property]+'; ';
	}
	console.log(output);
}

function initHistory()
{
	console.log("+initHistory");
	if (window.history && window.history.pushState) {
		function afterGetResponse(status, data, state) {
			console.log('afterGetResponse');
			if (status) {
				$(state.dest[0]).html(data);
				history.pushState(state, state.title, state.url);
				document.title = state.title;
			} else {
				$(state.dest[0]).html("<h1>Failed to load page</h1>");
				//$(state.dest[0]).html("<h1>Failed to load page</h1>"+"<br />"+JSON.stringify(data));
			}
		}
		function makeGetRequest(state) {
			getRequest(state.url, 'pid='+state.dest[1],
				function(status, data) {
					afterGetResponse(status, data, state);
				});
		}
		$(document).on('click', 'a[data-dest]', function (e) {
			e.preventDefault();
			console.log("+a");
			var This = $(this),
			url = This.attr("href"),
			dest = This.attr("data-dest").split(':');
			title = This.text()+' | My Offers';
			state = {url:url, title:title, dest:dest,};
			makeGetRequest(state);
		});

		window.addEventListener('popstate', function(e) {
			console.log('+popstate');
			console.log(JSON.stringify(state));
			if (e.state !== null) {
				makeGetRequest(e.state);
			} else {
				console.log("no history to load");
				location.reload();
				//window.history.go(-1);
			}
		});
	}
}

function initSearch()
{
	console.log('+initSearch');
	$("#app_search_input").suggestions({
		minLength: 2,
		_source: function(key, resp) {
			postRequest('/search/offer/', {'key': key}, function(status, result){
				if (true == status) {
					resp(result.data);
				} else {
					console.log('data : '+JSON.stringify(result.data));
				}
			});
		},
		_itemCreate: function(item) {
			var uiItem = '<li>'
			+ '<div class="wt-search-item">'
			+ '<a style="display:block; padding: 0.5em;" href="'+item.url+'">'+item.name+'</a>'
			+ '</div>'
			+ '</li>';
			return uiItem;
		},
		_itemSelect: function(input, item) {
			input.val(item.name);
		},
		_onEnter: function(e) {
			console.log('+_onEnter');
			var Inst = e.data;
			Inst.kf._onunfocus();
			if (Inst.kd._count > 0) {
				var item = Inst.kd._jsonObj[Inst.kd._selectedIndex];
				location.href = item.url
			}
		}
	});
}

function initSwitchTabs()
{
	console.log("+initSwitchTabs");
	$(".wt-switchtab").each(function(i, elm) {
		$(elm).switchtab({});
	});
}

function initApp()
{
	console.log("+initApp");
	$("#app_close").on("click", function(e) {
		console.log("+ui-close clicked");
		navClicked();
	});

	$(".app_vlist_exp_item > a").on("click", function(e) {
        e.preventDefault();
        $(this).parent().toggleClass("expanded");
    });

	$("#app_leftnav li").not(".app_vlist_exp_item").on("click", function(e){
		console.log("+app_leftnav");
		navClicked();
	});
}

function navClicked() {
	console.log("+navClicked");
	var appleft = document.getElementById("app_leftnav");
	var appclose = document.getElementById("app_close");
	if (appleft && appclose) {
		console.log("width: "+appleft.style.width);
		if (appleft.style.width == "50%") {
			appleft.style.width = "0";
			appleft.style.display = "none";
			appclose.style.display = "none";
		} else {
			appleft.style.width = "50%";
			appleft.style.display = "block";
			appclose.style.display = "block";
		}
	}
}

function ajaxFormSubmit(e)
{
	console.log("+ajaxFormSubmit");
	e.preventDefault();
	var form = $(this);
	var handle = form.data('handlers');
	var action = form.attr('action');
	console.log('action : '+ action);

	if (handle && handle.before)
		if (handle.before(e) === false)
			return;

	postRequest(action, form.serialize(), (status, data) => {
		if (handle && handle.after) {
			e.status = status;
			e.data = data;
			handle.after(e);
		} else {
			if (status === true) {
				Toast.show(data.message);
			} else {
				Toast.show(JSON.stringify(data));
			}
		}
	});
}

function afterResponse(e) {
	console.log("+afterResponse");
	if (e.status == false) {
		var errors = '';
		for (var key in e.data) {
			console.log(key + ' : '+ e.data[key]);
			errors += e.data[key]+'<br />';
		}
		$('.ui-errors').html(errors);
	} else {
		$('.ui-errors').html('');
	}
}

function postRequest(pUrl, pData, pCallback)
{
	console.log("+postRequest");
	$.ajax({url: pUrl,
		data: pData,
		type: 'POST',
		async: true,
		dataType: 'text',
		complete: function(res) {
			console.log('+comeplete :'+ res.status);
		},
		success: function (data, status, xhr) {
			mimeType = xhr.getResponseHeader("content-type");
			if (mimeType.indexOf('json') > -1) {
				console.log('response : ' + data);
				jsonObj = jQuery.parseJSON(data);
				switch(jsonObj.status) {
					case 302:
						console.log('redirect');
						location.href = jsonObj.url;
						break;
					case 200:
					case 204:
						pCallback(true, jsonObj.data);
						break;
					case 401:
					default:
						pCallback(false, jsonObj.data);
						break;
				}
			} else if (mimeType.indexOf('html') > -1) {
				console.log('html response');
				pCallback(true, data);
			} else {
				console.log('unknown response');
				pCallback(false, {'error':'unexpected content type'});
			}
		},
		error: function (xhr,error) {
			console.log('status : '+xhr.status);
			Toast.show('Network error occured');
			pCallback(false, {'data': error});
		}
	});
}

function getRequest(pUrl, pData, pCallback)
{
	$.ajax({url: pUrl,
		data: pData,
		type: 'GET',
		async: true,
		dataType: 'text',
		success: function (data, status, xhr) {
			mimeType = xhr.getResponseHeader("content-type");
			if (mimeType.indexOf('json') > -1) {
				console.log('response : ' + data);
				jsonObj = jQuery.parseJSON(data);
				switch(jsonObj.status) {
				case 302:
					console.log('redirect');
					location.href = jsonObj.url;
					break;
				}
			}
		},
	}).done(function(data) {
		console.log('html response');
		pCallback(true, data);
	}).fail(function(error) {
		console.log('unknown response');
		pCallback(false, error);
	});
}

/****************** Cookie API ***********************/
var Cookie = {
	get: function(name) {
		var cv = null;
		if (document.cookie != 'undefined' && document.cookie !== '') {
			var c = document.cookie.split(';');
			for (var i = 0; i < c.length; i++) {
				var c = jQuery.trim(c[i]);
				// Does this cookie string begin with the name we want?
				if (c.substring(0, name.length + 1) === (name + '=')) {
					cv = decodeURIComponent(c.substring(name.length + 1));
					break;
				}
			}
		}
		return cv;
	},
	set: function (cname, cvalue, exdays) {
		var d = new Date();
		d.setTime(d.getTime() + (exdays*24*60*60*1000));
		var expires = "expires="+d.toUTCString();
		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
	}
};

/*****************************************************/
/******************** Widgets ************************/
/****************** Toast API ************************/
var Popup = {
	show: function() {

	},
	hide: function() {

	}
};

var Toast =  {
	show: function(text='Error', timeout=1200) {
		//$('.ui-toast').text(text).fadeIn(500).delay(timeout).fadeOut(500);
		$('.ui-toast').fadeIn({duration: 500, start: function() {$(this).text(text);}}).delay(timeout).fadeOut(500);
	},
	hide: function() {
		$('.ui-toast').hide();
	}
};

var wsuggest = function(Elem, opts) {
	console.log('+wsuggest');
	console.log('element : '+Elem.prop("tagName"));
	var Inst = $(Elem);
	Inst.kd = {
		_name: 'suggest',
		_ui: null,
		_count: 0,
		_jsonObj: null,
		_selectedItem: null,
		_selectedIndex: 0,
	};

	Inst.kf = {
		minLength: 1,
		delay: 0,
		_create: function(e) {
			console.log('+_create['+kd._name+']');
			kd._ui = $('<ul class="wt-search-list wt-search-list-app" >');
			kd._ui.css({width: Elem.css('width')});
			Elem.after(kd._ui);
			//kd._ui.on('touchstart click', 'li', kf._itemClick);
			//kd._ui.on('mouseenter', 'li', kf._itemHover);
			kd._ui.on('touchend', 'li', kf._itemClick);
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
		_parse: function(jsonObj) {
			console.log('+_parse');
			kd._ui.html('');
			if (jsonObj.length > 0) {
				var count = 0;
				for (i in jsonObj) {
					kd._ui.append(kf._itemCreate(jsonObj[i]));
					count++;
				}
				kd._jsonObj = jsonObj;
				kd._count = count;
				kd._selectedIndex = 0;
				kd._selectedItem = kd._ui.children().eq(kd._selectedIndex).addClass('wt-search-item-a');
				kd._ui.show();
			} else {
				kd._count = 0;
				kd._selectedIndex = 0;
				kd._ui.html('<div class="wt-search-item">No search results</div>');
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
				kd._ui.children().eq(kd._selectedIndex).removeClass('wt-search-item-a');
				kd._selectedIndex = index;
				kd._ui.children().eq(kd._selectedIndex).addClass('wt-search-item-a');
				if (kd._jsonObj) {
					kf._itemSelect(Elem, kd._jsonObj[index]);
				}
			}
		},
		_itemClick: function(e) {
			console.log('+_itemClick');
			var index = $(this).index();
			console.log('old selected : '+ kd._selectedIndex);
			console.log('new selected : '+ index);
			if (kd._jsonData) {
				kd._ui.children().eq(kd._selectedIndex).removeClass('wt-search-item-a');
				kd._ui.children().eq(index).addClass('wt-search-item-a');
				kf._itemSelect(Elem, kd._jsonData[index]);
				kd._selectedIndex = index;
			}
		},
		_itemSelect: function(input, item) {
			 console.log('implement _itemSelect function');
		},
		_itemSelectCurrent: function() {
			if (kd._count > 0 && kd._jsonObj) {
				kf._itemSelect(Elem, kd._jsonObj[kd._selectedIndex]);
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
					kd._ui.children().eq(kd._selectedIndex).removeClass('wt-search-item-a');
					kd._selectedIndex--;
					var child = kd._ui.children().eq(kd._selectedIndex).addClass('wt-search-item-a');
					var cont = kd._ui;
					cont.scrollTop(child.position().top + cont.scrollTop());
					//cont.scrollTop(child.offset().top - cont.offset().top + cont.scrollTop());
					if (kd._jsonObj) {
						kf._itemSelect(Elem, kd._jsonObj[kd._selectedIndex]);
					}
				}
				handled = true;
				break;
			case KEY_DOWN:
				if (kd._selectedIndex < kd._count - 1) {
					kd._ui.children().eq(kd._selectedIndex).removeClass('wt-search-item-a');
					kd._selectedIndex++;
					var child = kd._ui.children().eq(kd._selectedIndex).addClass('wt-search-item-a');
					var cont = kd._ui;
					//console.log("child top : "+ child.position().top);
					//console.log("scroll top : "+ cont.scrollTop());
					cont.scrollTop(child.position().top + cont.scrollTop());
					if (kd._jsonObj) {
						kf._itemSelect(Elem, kd._jsonObj[kd._selectedIndex]);
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
	console.log('element : '+Elem.prop('tagName'));
	var Inst = $(Elem);
	// klass data
	Inst.kd = {
		_name: 'fileupload',
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
			console.log('+_create['+kd._name+']');
			kd._ui = $('<div class="wt-progress-div" ></div>');
			kd._ui.css({width: Elem.css('width')});
			kd._hidden = $('<input type="hidden" name="files" value="" >');
			Elem.before(kd._hidden);
			Elem.after(kd._ui);
			Elem.on('change', kf._upload);
		},
		_destroy: function(e) {
			console.log('+_destroy['+kd._name+']');
			kd._ui.remove();
			kd._hidden.remove();
		},
		_upload: function(e) {
			console.log('+_upload');
			e.stopPropagation(); // Stop stuff happening
			e.preventDefault(); // Totally stop stuff happening
			var lThis = this;
			var lfiles = $(lThis)[0].files;
			var count = kd._ui.find('.wt-progress-outer').length;
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

			var uiItem = $('<div class="wt-progress-outer" >'
				+'<div class="wt-progress-inner">'
				+'<div class="wt-progress-filename">'+fileName+'</div>'
				+'<div class="wt-progress-bar">&nbsp;0%</div></div>'
				+'<div class="wt-progress-control">'
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
				success: function(jsonObj, status, xhr) {
					switch (jsonObj.status) {
						case 302:
						{
							console.log('redirect');
							location.href = jsonObj.url;
							break;
						}
						case 200:
						case 204:
						{
							console.log("upload finished");
							var id = jsonObj.data.upload_id;
							kd._uploads.push(id);
							kd._hidden.val(kd._uploads.toString());
							uiBtn.data('request', null);
							uiBtn.data('upload_id', id);
							uiBtn.text('Remove');
							console.log('ids : '+kd._uploads.toString());
							break;
						}
						case 401:
						default:
							console.log('ERRORS: ' + JSON.stringify(jsonObj.data));
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
			lThis.parents('.wt-progress-outer').remove();
		},
		_progress: function(progress) {
			console.log('progress : '+progress+'%');
			var progressbar = kd._ui.find('.wt-progress-bar');
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

function wswitchtab(Elem, opts)
{
	console.log('+wswitchtab');
	console.log('element : '+Elem.prop('tagName'));
	var Inst = $(Elem);
	// klass data
	Inst.kd = {
		_name: 'switchtab',
		_total: 2,
		_active: null,
	};
	// klass functors
	Inst.kf =  {
		_activeIndex: 0,
		_create: function(e) {
			console.log('+_create['+kd._name+']');
			//Inst.find('.wt-switchtab-nav > a:nth-child(2)').
			var elems = Inst.find(".wt-switchtab-nav > li > a[rel]");
			kd._total = elems.length;
			console.log("length : "+ kd._total);
			kd._active = elems.eq(kf._activeIndex);
			var rel = kd._active.prop("rel");
			Inst.find(rel).show();
			elems.on("click", function(e){
				console.log("+tabClicked");
				e.preventDefault();
				var rel = kd._active.prop("rel");
				kd._active.removeClass("wt-switchtab-a");
				Inst.find(rel).hide();
				kd._active = $(this);
				rel = kd._active.prop("rel");
				kd._active.prop("class", "wt-switchtab-a");
				Inst.find(rel).show();
			});
		},
		_destroy: function(e) {
			console.log('+_destroy['+kd._name+']');
			kd._ui.remove();
		},
	};

	var kd = Inst.kd;
	var kf = Inst.kf;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
}

function onSwipe(el,func) {
      swipe_det = new Object();
      swipe_det.sX = 0;
      swipe_det.sY = 0;
      swipe_det.eX = 0;
      swipe_det.eY = 0;
      var min_x = 20;  //min x swipe for horizontal swipe
      var max_x = 40;  //max x difference for vertical swipe
      var min_y = 40;  //min y swipe for vertical swipe
      var max_y = 50;  //max y difference for horizontal swipe
      var direc = "";
      ele = document.getElementById(el);
      ele.addEventListener('touchstart',function(e){
        var t = e.touches[0];
        swipe_det.sX = t.screenX;
        swipe_det.sY = t.screenY;
      },false);
      ele.addEventListener('touchmove',function(e){
        e.preventDefault();
        var t = e.touches[0];
        swipe_det.eX = t.screenX;
        swipe_det.eY = t.screenY;
      },false);
      ele.addEventListener('touchend',function(e){
        //horizontal detection
        if ((((swipe_det.eX - min_x > swipe_det.sX) || (swipe_det.eX + min_x < swipe_det.sX)) && ((swipe_det.eY < swipe_det.sY + max_y) && (swipe_det.sY > swipe_det.eY - max_y)))) {
          if(swipe_det.eX > swipe_det.sX) direc = "r";
          else direc = "l";
        }
        //vertical detection
        if ((((swipe_det.eY - min_y > swipe_det.sY) || (swipe_det.eY + min_y < swipe_det.sY)) && ((swipe_det.eX < swipe_det.sX + max_x) && (swipe_det.sX > swipe_det.eX - max_x)))) {
          if(swipe_det.eY > swipe_det.sY) direc = "d";
          else direc = "u";
        }

        if (direc != "") {
          if(typeof func == 'function') func(el,direc);
        }
        direc = "";
      },false);
}

function wcenter () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).height()) / 2) +
                                                $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).width()) / 2) +
                                                $(window).scrollLeft()) + "px");
    return this;
}

/****************** Exteded Jquery *******************/
jQuery.fn.exists = function(){return this.length>0;}
jQuery.fn.switchtab = function(options) { new wswitchtab(this, options); }
jQuery.fn.fileupload = function(options) { new wfileupload(this, options); }
jQuery.fn.suggestions = function(options) { new wsuggest(this, options); }
jQuery.fn.center = wcenter;
