var KEY_ESCAPE = 27;
var KEY_ENTER = 13;
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;

$(function() {
	console.log("+init");

	/*Initialize App*/
	initApp();
	/*Initialize History*/
	initHistory();
	/*Initialize search*/
	initSearch();
	/*Initialize switchTabs*/
	initSwitchTabs();

	console.log("-init");
});

function initApp()
{
	console.log("+initApp");
	$(document).on('submit', 'form.ajax-form', ajaxFormSubmit);

	$("#app_main_nav li:first-child").on('click' , function(e) {
		e.stopPropagation();
		$('#app_sub_nav_content').fadeToggle(100);
	});
	$("#app_main_nav").on('click', function(e) {
		$('#app_sub_nav_content').fadeOut(100);
	});

	$(".app_vlist_exp_item > a").on("click", function(e) {
		e.preventDefault();
		$(this).parent().toggleClass("expanded");
	});

	$AppOverlay.init();

	// Close the dropdown if the user clicks outside of it
	$(window).on("click", function(event) {
		console.log("window clicked");
		if (!event.target.matches('.ui-dropbtn')) {
			$(".ui-dropcontent").each(function(i, elm){
				elm.classList.remove("ui-show");
			});
		}
	});
}

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
		function makeRequest(state) {
			$AppRequest.get(state.url, 'pid='+state.dest[1],
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
			makeRequest(state);
		});

		window.addEventListener('popstate', function(e) {
			console.log('+popstate');
			console.log(JSON.stringify(state));
			if (e.state !== null) {
				makeRequest(e.state);
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
			$AppRequest.post('/search/offer/', {'key': key}, function(status, json){
				if (true == status) {
					resp(json.data);
				} else {
					console.log('data : '+JSON.stringify(json.data));
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

function dropToggle(e, pThis)
{
	console.log("+dropToggle");
	e = e || window.event;
	//dumpObject(e);
	//e.preventDefault();
	e.stopPropagation();
	pThis.parentElement.getElementsByClassName("ui-dropcontent")[0].classList.toggle("ui-show");
}


function navClicked()
{
	console.log("+navClicked");
	var appleft = document.getElementById("app_leftnav");
	var apppage = document.getElementById("app_page");
	if (appleft && apppage) {
		console.log("marginLeft: "+appleft.style.marginLeft)
		if (appleft.style.marginLeft !== "-20%") {
			appleft.style.marginLeft = "-20%";
			apppage.style.width = "95%";
			apppage.style.margin = "0 auto";
		} else {
			appleft.style.marginLeft = "0";
			apppage.style.marginLeft = "20%";
			apppage.style.width = "80%";
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

	$AppRequest.post(action, form.serialize(), (status, json) => {
		if (handle && handle.after) {
			e.status = status;
			e.resp = json;
			e.$src = form;
			handle.after(e);
		} else {
			$AppToast.show(JSON.stringify(json.message));
		}
	});
}

function afterResponse(e) {
	console.log("+afterResponse");
	if (e.status) {
		$AppNoti.info({title:"Successful", text:e.resp.message});
	} else {
		var errors = '';
		for (var key in e.resp.data) {
			console.log(key + ' : '+ e.resp.data[key]);
			errors += e.resp.data[key]+'<br />';
		}
		$AppNoti.error({title:e.resp.message, text:errors});
	}
}

var $AppRequest = {
	get: function(pUrl, pData, pCallback) {
		console.log('+get');
		this._request('GET', pUrl, pData, pCallback);
	},
	post: function (pUrl, pData, pCallback) {
		console.log("+post");
		this._request('POST', pUrl, pData, pCallback);
	},
	_request: function(pType='POST', pUrl, pData, pCallback) {
		$.ajax({url: pUrl,
			data: pData,
			type: pType,
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
							pCallback(true, jsonObj);
							break;
						case 401:
						default:
							pCallback(false, jsonObj);
							break;
					}
				} else if (mimeType.indexOf('html') > -1) {
					console.log('html response');
					pCallback(true, data);
				} else {
					console.log('unknown response');
					pCallback(false, {'message': 'Unknown response', 'data':'unexpected content type'});
				}
			},
			error: function (xhr,error) {
				console.log('status : '+xhr.status);
				$AppToast.show('Network error occured');
				pCallback(false, {'message': 'Network failed', 'data': {error} });
			}
		});
	}
}

/****************** Cookie API ***********************/
var $AppCookie = {
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

function get_csrf()
{
	var $mt = $('meta[name=csrf-token]');
	var data = {};
	data[$mt.attr("key")] = $mt.attr("content");
	return data;
}
/*****************************************************/
/******************** Widgets ************************/
/****************** UI API ************************/
var $AppOverlay = {
	init: function() {
		this.$overlay = $('#wt-overlay');
		this.$content_def = $('<div style="width:80% height:50%;" data-type="none"></div>');
		this.$content = this.$content_def;
		this.$overlay.find('.wt-closebtn').on('click', this, this._onclose);
	},
	show: function($content=this.$content_def) {
		return this.update($content);
	},
	hide: function() {
		this.$overlay.hide();
		return this;
	},
	update: function($content) {
		this.$content = $($content);
		this.$overlay.find('.wt-overlay-content').html(this.$content.show());
		this.$overlay.show();
		return this;
	},
	close: function(e) {
		console.log("CLOSE OVERLAY");
		this.$overlay.find('.wt-closebtn').click();
	},
	_onclose: function(e) {
		console.log("ON CLOSE OVERLAY");
		pThis = e.data;
		var $content = pThis.$content.hide();
		if ($content.attr('data-type') == 'persist') {
			setTimeout(function(){ $content.appendTo('body'); }, 100);
		} else {
			$content.remove();
		}
		pThis.hide();
	}
};


var $AppNoti = {
	_defaults: {
		link: window.location,
		title: 'Alert',
		text: 'Alert',
		timeout: 5000,
	},
	options: function(p) {
		var finalOpts = this._defaults;
		for (var key in p) {
			finalOpts[key] = p[key];
		}
		return finalOpts;
	},
	info: function(p) {
		var opts = this.options(p);
		console.log(JSON.stringify(opts));
		var $elm = $('#wt-noti').clone().removeAttr('id');
		$elm.fadeIn({duration: 500,
			start: function() {
				$(this).find('.wt-notititle').html(opts.title);
				$(this).find('.wt-notibody').html(opts.text);
				$(this).find('.wt-notilink').attr('href', opts.link);
			}
		}).delay(opts.timeout).fadeOut({duration:500,
			always: function() {
				$(this).remove();
			}
		});
		$('.wt-notibox').append($elm);
	},
	error: function(p) {
		this.info(p);
	},
	warn: function(p) {
		this.info(p);
	}
};

var $AppToast = {
	show: function(text='Error', timeout=1800) {
		$('.wt-toast').fadeIn({duration: 500, start: function() {$(this).text(text);}}).delay(timeout).fadeOut(500);
	},
	hide: function() {
		$('.wt-toast').hide();
	}
};

var wsuggest = function(Elem, opts) {
	console.log('+wsuggest element : '+Elem.prop("tagName"));
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
	console.log('+wfileupload element : '+Elem.prop('tagName'));
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
			fdata.append('image', file);
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
	console.log('+wswitchtab element : '+Elem.prop('tagName'));
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

/****************** Exteded Jquery *******************/
jQuery.fn.exists = function(){return this.length>0;}
jQuery.fn.switchtab = function(options) { new wswitchtab(this, options); }
jQuery.fn.fileupload = function(options) { new wfileupload(this, options); }
jQuery.fn.suggestions = function(options) { new wsuggest(this, options); }
