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

	console.log("-init");
});

function initApp()
{
	console.log("+initApp");

	$AppOverlay.init();

	$AppDialog.init();

	$(document).on("submit", "form.ajax-form", $AppForm.ajaxSubmit);

	$(document).on("click", ".app_vlist_exp_item > a", function(e) {
		e.preventDefault();
		$(this).parent().toggleClass("expanded");
	});

	$(document).on("click", function(e) {
		//e.stopPropagation();
		$(".ui-dropcontent").hide();
	});
	$(document).on("click", ".ui-dropbtn", function(e) {
		e.stopPropagation();
		$(e.target).parents(".ui-dropdown").find(".ui-dropcontent").toggle();
	});

	$(document).on("click", ".ui-hovermenu", function(e) {
		console.log("hovermenu clicked");
		e.preventDefault();
		e.stopPropagation();
	});
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
			title = This.text()+' | '+$AppData.name();
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
		source: function(key, resp) {
			$AppRequest.post('/search/offer/', {'key': key}, function(status, json){
				if (true == status) {
					resp(json.data);
				} else {
					console.log('data : '+JSON.stringify(json.data));
				}
			});
		},
		itemCreate: function(item) {
			var uiItem = '<li>'
			+ '<div class="wt-search-item">'
			+ '<a style="display:block; padding: 0.5em;" href="'+item.url+'">'+item.name+'</a>'
			+ '</div>'
			+ '</li>';
			return uiItem;
		},
		onItemSelect: function(input, item) {
			input.val(item.name);
		},
		onEnter: function(e) {
			console.log('+onEnter');
			var $Inst = e.data;
			$Inst.kf._onunfocus();
			if ($Inst.kd._count > 0) {
				var item = $Inst.kd._jsonObj[$Inst.kd._selectedIndex];
				location.href = item.url
			}
		}
	});
}

function navClicked()
{
	console.log("+navClicked");
	var appleft = document.getElementById("app_leftnav");
	var apppage = document.getElementById("app_page");
	if (appleft && apppage) {
		console.log("marginLeft: "+appleft.style.marginLeft);
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

var $AppForm = {
	ajaxSubmit: function(e) {
		console.log("+ajaxSubmit");
		e.preventDefault();
		var $form = $(this);
		e.$form = $form;
		var action = $form.attr('action');
		console.log('action : '+ action);

		var handler = $form.data('data-handler');
		handler = (handler)? handler: window[$form.attr('data-delegate')];

		if (handler) {
			handler.before = (handler.before)? handler.before : this.before;
			handler.after = (handler.after)? handler.after: this.after;
		} else {
			handler = this;
		}

		if (handler.before(e) === false)
			return;

		$AppRequest.post(action, $form.serialize(), (status, json) => {
			e.status = status;
			e.resp = json;
			handler.after(e);
		});
	},
	before: function(e) {
		console.log('+$AppForm::before');
		return true;
	},
	after: function(e) {
		console.log("+$AppForm::after");
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
};

var $AppFormUtils = {
	setValByName: function($form, name, val) {
		console.log('+setValByName');
		var viewVal = val;
		var $editNode = $form.find('.ui-input[name='+name+']');
		var $viewNode = $form.find('[data-rel='+name+']');
		if ($editNode.exists()) {
			viewVal = this.setVal($editNode, val);
			$editNode.attr('data-value', val);
		}
		($viewNode.exists() && $viewNode.html(viewVal));
	},
	setVal: function($node, val) {
		var retVal = val;
		switch($node.prop("tagName").toLowerCase()) {
			case 'input':
				var type = $node.prop('type').toLowerCase();
				switch(type) {
					case 'text':
						$node.val(val);
						break;
					case 'radio':
					case 'checkbox':
						if (val) {
							$node.prop('checked', true);
						} else {
							$node.removeProp('checked');
						}
						retVal = $node.val();
						break;
				}
				break;
			case 'select':
				retVal = $node.find('[value='+val+']').prop('selected', true).text();
				break;
			case 'textarea':
				$editNode.html(val);
				break;
		}
		console.log('retVal : '+ retVal);
		return retVal;
	},
	resetVal: function($form) {
		var This = this;
		$form.find('input[type=text], select, textarea').each(function(index, node) {
			This.setVal($(node), $(node).attr('data-value'));
		});
	}
}

var $AppFormSaveHandler = {
	before: function(e) {
		console.log("+beforeSaveReq");
		return true;
	},
	after: function(e) {
		console.log("+afterSaveRes");
		if (e.status) {
			var vals = e.resp.data;
			var $form = e.$form;
			for (var key in vals) {
				var val = vals[key];
				console.log(key+' : '+val);
				$AppFormUtils.setValByName($form, key, val);
			}
			$form.find('input[type=button]').click();
			$AppNoti.info({title:'Done!!', text:e.resp.message});
		} else {
			var errors = '';
			for (var err in e.resp.data) {
				errors += e.resp.data[err] + '<br />';
			}
			$AppNoti.info({title:e.resp.message, text:errors});
		}
	},
};

/*******************************************************/
/******************** App Library **********************/
/*******************************************************/
var $AppUtil = {
	merge: function(a1, a2) {
		var res = a1;
		//for (var k in a1) { res[k] = a1[k]; }
		for (var k in a2) { res[k] = a2[k]; }
		return res;
	},
	dump: function(obj) {
		var out = '';
		for (var k in obj) { out += k + ': ' + obj[k]+'; '; }
		console.log(out);
	},
	scrollTo: function($elm) {
		var elmTop = $elm.offset().top;
		var headerH = $("#app_header").height();
		$('html, body').animate({
			scrollTop: elmTop - headerH
		}, 500);
	}
};

var $AppEvent = {
	new: function() {
		console.log("+Event new");
		copy = {'_set': new Array()};
		for (var key in this) {
			if (this.hasOwnProperty(key))
				copy[key] = this[key];
		}
		return copy;
	},
	add: function(p) {
		console.log("+Event add");
		if (this._set.indexOf(p) == -1)
			this._set.push(p);
	},
	del: function(p) {
		console.log("+Event del");
		var pos = this._set.indexOf(p);
		if (pos > 1)
			this._set.splice(pos, 1);

	},
	call: function(e) {
		console.log("+Event call");
		var ret = true;
		for (i in this._set) {
			ret = ret && this._set[i](e);
		}
		return ret;
	}
};

var $AppRequest = {
	_options: {
		url: '', data: '', type: 'POST',
		dataType: 'text', processData: true,
		contentType: 'application/x-www-form-urlencoded; charset=UTF-8', /* 'multipart/form-data', or 'text/plain' */
		progress: function(p){},
		complete: function(s,o){},
	},
	options: function() {
		return $.extend({}, this._options);
	},
	abort: function(request) {
		request.abort();
	},
	get: function(pUrl, pData, pCallBack) {
		console.log('+get');
		var opts = this.options();
		opts.url = pUrl;
		opts.type = 'GET';
		opts.data = pData;
		opts.complete = pCallBack;
		return this._request(opts);
	},
	post: function(pUrl, pData, pCallBack) {
		console.log("+post");
		var opts = this.options();
		opts.url = pUrl;
		opts.data = pData;
		opts.complete = pCallBack;
		return this._request(opts);
	},
	file: function(opts) {
		return this._request(opts);
	},
	_request: function(opts) {
		return $.ajax(
			{url: opts.url,
			data: opts.data,
			type: opts.type,
			dataType: opts.dataType,
			processData: opts.processData,
			contentType: opts.contentType,
			async: true,
			cache: false,
			xhr: function() {
				var xhr = jQuery.ajaxSettings.xhr();
				xhr.upload.addEventListener("progress", function(evt){
					if (evt.lengthComputable) {
						var percent = 100 * parseInt(evt.loaded / evt.total);
						opts.progress(percent);
					}
				}, false);
				return xhr;
			},
			complete: function(res) {
				console.log('+comeplete : '+ res.status);
			},
			success: function (data, status, xhr) {
				console.log('+success');
				mimeType = xhr.getResponseHeader("content-type");
				if (mimeType.indexOf('json') > -1) {
					console.log('content-type: json');
					console.log('data : ' + data);
					jsonObj = JSON.parse(data);
					switch(jsonObj.status) {
						case 302:
							console.log('redirect');
							location.href = jsonObj.url;
							break;
						case 200:
						case 204:
							opts.complete(true, jsonObj);
							break;
						case 401:
						default:
							opts.complete(false, jsonObj);
							break;
					}
				} else if (mimeType.indexOf('html') > -1) {
					console.log('content-type: html');
					opts.complete(true, data);
				} else {
					console.log('content-type: unknown');
					opts.complete(false, {'message': 'Unknown response', 'data':'unexpected content type'});
				}
			},
			error: function (xhr,error) {
				console.log('+error : '+xhr.status);
				$AppToast.show('Network error occured');
				opts.complete(false, {'message': 'Network failed', 'data': {error} });
			}
		});
	}
};


var $AppData = {
	Cookie: {
		get: function(cname) {
			var cv = null;
			if (document.cookie != 'undefined' && document.cookie !== '') {
				var cks = document.cookie.split(';');
				for (var i = 0; i < cks.length; i++) {
					var c = cks[i].trim();
					/* Does this cookie string begin with the name we want? */
					if (c.substring(0, cname.length + 1) === (name + '=')) {
						cv = decodeURIComponent(c.substring(cname.length + 1));
						break;
					}
				}
			}
			return cv;
		},
		set: function(cname, cvalue, exdays) {
			var d = new Date();
			d.setTime(d.getTime() + (exdays*24*60*60*1000));
			var expires = "expires="+d.toUTCString();
			document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
		},
		has: function(cname) {
			return (this.get(cname) != null);
		}
	},
	Storage: {
		get: function(key) {
			if (typeof(Storage) !== "undefined")
				return localStorage.getItem(key);
			return "";
		},
		set: function(key, val) {
			if (typeof(Storage) !== "undefined")
				localStorage.setItem(key, val);
		},
	},
	csrf: function() {
		var $mt = $('meta[name=csrf-token]');
		var data = {};
		data[$mt.attr("key")] = $mt.attr("content");
		return data;
	},
	name: function() {
		if (!this._name) {
			var $mt = $('meta[name=app-name]');
			this._name = $mt.attr("content") || "/m\\";
		}
		return this._name;
	}
};

var $AppOverlay = {
	init: function() {
		this.$overlay = $('#wt-overlay');
		this.$closebtn = this.$overlay.find('.wt-closebtn');
		this.$body = this.$overlay.find('.wt-overlay-body');
		this.$html_def = $('<div style="width:80%; height:inherit; margin: 0 auto; background:#fff;" data-type="none"></div>');
		this.$html = this.$html_def;
		this.$closebtn.on('click', this, this._onclose);
		this.$overlay.on('click', this, this._onclick);
		this.$overlay.on('keyup', this, this._onkeyup);
		this._shown = false;
		this._options_def = { closeBtn:true, closeOnEscape:true, closeOnClickOutside:true };
		this._options = $AppUtil.merge(this._options_def, {});
	},
	_apply_options: function(options) {
		this._options = $AppUtil.merge(this._options_def, options);
		if (this._options['closeBtn'] === false)
			this.$closebtn.hide();
		else
			this.$closebtn.show();
	},
	shown: function() {
		return this._shown;
	},
	show: function($html=this.$html_def, options={}) {
		this._apply_options(options);
		/* ordering matter for correct heights */
		this.$overlay.show();
		this.update($html);
		this.$overlay.focus();
		this._shown = true;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
	},
	hide: function() {
		this.$overlay.hide();
		this._shown = false;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
	},
	update: function($html) {
		this.$html = $($html);
		this.$body.html(this.$html.show());
		var $scroll = this.$html.find(".wt-overlay-scroll");
		if ($scroll.exists()) {
			var h1 = this.$body.height();
			var h2 = this.$html.height();
			var h3 = $scroll.height();
			if (h1 < h2) {
				var h4 = h3 - (h2 - h1);
				console.log("h4 : "+h4);
				$scroll.height(h4);
			}
		}
		return this;
	},
	clear: function() {
		this.update(this.$html_def);
		return this;
	},
	close: function(e) {
		console.log("CLOSE OVERLAY");
		this.$closebtn.click();
	},
	_close: function(e) {
		var $html = this.$html.hide();
		if ($html.attr('data-type') == 'persist') {
			setTimeout(function(){ $html.appendTo('body'); }, 100);
		} else {
			$html.remove();
		}
		this.hide();
	},
	_onclose: function(e) {
		console.log("ONCLOSE OVERLAY");
		e.data._close();
	},
	_onclick: function(e) {
		console.log("ONCLICK OVERLAY");
		var This = e.data;
		if (This._options["closeOnClickOutside"] === true && $(e.target).parent().is(This.$overlay)) {
			This._close();
		}
	},
	_onkeyup: function(e) {
		console.log("ONKEYUP OVERLAY");
		var This = e.data;
		if (This._options["closeOnEscape"] === true && e.keyCode == KEY_ESCAPE) {
			This._close();
		}
	}
};


/* App Modal */
var $AppModal = {
	show: function($html) {
		$AppOverlay.show($html, {closeOnClickOutside:true});
	},
	update: function($html) {
		$AppOverlay.update($html);
	},
	close: function() {
		$AppOverlay.close();
	},
};

/* App Dialog */
var $AppDialog = {
	init: function() {
		this.$dialog = $('#wt-dialog');
		this.$closebtn = this.$dialog.find('.wt-closebtn');
		this.$body = this.$dialog.find('.wt-dialog-body');
		this.$html_def = $('<div style="width:100%; height:inherit; margin: 0 auto; background:#fff;" data-type="none"><h1>Hello World!!</h1></div>');
		this.$html = this.$html_def;
		this.$closebtn.on('click', this, this._onclose);
		this.$dialog.on('click', this, this._onclick);
		this.$dialog.on('keyup', this, this._onkeyup);
		this._shown = false;
		this._options_def = { closeBtn:true, closeOnEscape:true, closeOnClickOutside:true };
		this._options = $AppUtil.merge(this._options_def, {});
	},
	_apply_options: function(options) {
		this._options = $AppUtil.merge(this._options_def, options);
		if (this._options['closeBtn'] === false)
			this.$closebtn.hide();
		else
			this.$closebtn.show();
	},
	shown: function() {
		return this._shown;
	},
	show: function($html=this.$html_def, options={}) {
		this._apply_options(options);
		/* ordering matter for correct heights */
		this.$dialog.show();
		this.update($html);
		this.$dialog.focus();
		this._shown = true;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
	},
	hide: function() {
		this.$dialog.hide();
		this._shown = false;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
	},
	update: function($html) {
		this.$html = $($html);
		this.$body.html(this.$html.show());
		var $scroll = this.$html.find(".wt-dialog-scroll");
		if ($scroll.exists()) {
			var h1 = this.$body.height();
			var h2 = this.$html.height();
			var h3 = $scroll.height();
			if (h1 < h2) {
				var h4 = h3 - (h2 - h1);
				console.log("h4 : "+h4);
				$scroll.height(h4);
			}
		}
		return this;
	},
	clear: function() {
		this.update(this.$html_def);
		return this;
	},
	close: function(e) {
		console.log("CLOSE OVERLAY");
		this.$closebtn.click();
	},
	_close: function(e) {
		var $html = this.$html.hide();
		if ($html.attr('data-type') == 'persist') {
			setTimeout(function(){ $html.appendTo('body'); }, 100);
		} else {
			$html.remove();
		}
		this.hide();
	},
	_onclose: function(e) {
		console.log("ONCLOSE DIALOG");
		e.data._close();
	},
	_onclick: function(e) {
		console.log("ONCLICK DIALOG");
		var This = e.data;
		if (This._options["closeOnClickOutside"] === true && $(e.target).parent().is(This.$dialog)) {
			This._close();
		}
	},
	_onkeyup: function(e) {
		console.log("ONKEYUP DIALOG");
		var This = e.data;
		if (This._options["closeOnEscape"] === true && e.keyCode == KEY_ESCAPE) {
			This._close();
		}
	}
};


/* App Popup */
var $AppPopup = {

};


var $AppNoti = {
	_defaults: {
		link: window.location,
		title: 'Alert',
		text: 'Alert',
		timeout: 5000,
	},
	info: function(p) {
		var opts = $AppUtil.merge(this._defaults, p);
		console.log(JSON.stringify(opts));
		var $elm = $('#wt-noti').clone().removeAttr('id');
		$elm.fadeIn({duration: 500,
			start: function() {
				$(this).find('.wt-notititle').html(opts.title);
				$(this).find('.wt-notibody').html(opts.text);
				$(this).find('.wt-notilink').attr('href', opts.link);
			}
		}).delay(opts.timeout).fadeOut({
			duration:500,
			always: function() { $(this).remove();}
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
		$('.wt-toast').fadeIn({
			duration: 500,
			start: function() { $(this).text(text); },
		}).delay(timeout).fadeOut(500);
	},
	hide: function() {
		$('.wt-toast').hide();
	}
};

/*******************************************************/
/******************** UI Widgets **********************/
/*******************************************************/

var wsuggest = function($Inst, opts) {
	console.log('+wsuggest : '+$Inst.prop("tagName"));
	$Inst.kd = {
		_name: 'suggest',
		_count: 0,
		_selectedIndex: 0,
		_jsonItemsList: null,
		$_body: null,
		$_selectedItem: null,
	};

	$Inst.kf = {
		minLength: 1,
		delay: 0,
		scrollTimer: null,
		_create: function(e) {
			console.log('+_create['+kd._name+']');
			kd.$_body = $('<ul class="wt-search-list wt-search-list-app" >');
			kd.$_body.css({width: $Inst.css('width')});
			kd.$_body.on('mouseenter', 'li', kf._onitemhover);
			kd.$_body.on('click', 'li', kf._onitemclick);
			kd.$_body.on('scroll', kf._onlistscroll);
			$Inst.on("keyup", kf._onkeyup);
			$Inst.on("keypress", kf._onkeypress);
			$Inst.on("focus", kf._onfocus);
			$Inst.on("blur", kf._onunfocus);
			$Inst.after(kd.$_body);
		},
		_destroy: function(e) {
			kd.$_body.remove();
			kd.$_body = null;
		},
		_onfocus: function(e) {
			console.log('+_onfocus');
			kd.$_body.show();
		},
		_onunfocus: function(e) {
			kd.$_body.hide();
		},
		source: function(key, resp) {
			console.log('implement source function');
		},
		_parse: function(jsonItemsList) {
			console.log('+_parse');
			kd.$_body.html('');
			kd._jsonItemsList = jsonItemsList;
			kd._count = jsonItemsList.length;
			kd._selectedIndex = 0;
			if (kd._count > 0) {
				for (i in jsonItemsList) {
					kd.$_body.append(kf.itemCreate(jsonItemsList[i]));
				}
				kd.$_selectedItem = kd.$_body.children().eq(kd._selectedIndex);
				kd.$_selectedItem.addClass('wt-search-item-a');
			} else {
				kd.$_body.html('<div class="wt-search-item">No search results</div>');
			}
			kd.$_body.show();
		},
		itemCreate: function(item) {
			console.log('implement itemCreate function');
			return '';
		},
		_setItemSelected(newIndex) {
			var oldIndex = kd._selectedIndex;
			console.log('oldIndex : '+oldIndex + ' newIndex : '+newIndex);
			if (newIndex >= 0 && newIndex < kd._count) {
				if (oldIndex != newIndex) {
					var $children = kd.$_body.children();
					$children.eq(oldIndex).removeClass('wt-search-item-a');
					kd.$_selectedItem = $children.eq(newIndex).addClass('wt-search-item-a');
					kd._selectedIndex = newIndex;
					kf._notifyItemSelected();
				}
				var itemTop = kd.$_selectedItem.position().top;
				var itemHeight = kd.$_selectedItem.outerHeight();
				var bodyScroll = kd.$_body.scrollTop();
				var bodyHeight = kd.$_body.outerHeight();

				console.log('itemTop : '+ itemTop +' itemHeight : '+ itemHeight);
				console.log('bodyScroll : '+ bodyScroll +' bodyHeight : '+ bodyHeight);
				if (itemTop < 0) {
					console.log('scrollup');
					kd.$_body.scrollTop(bodyScroll + itemTop);
				} else if (itemTop + itemHeight > bodyHeight) {
					console.log('scrolldown');
					kd.$_body.scrollTop(bodyScroll + itemHeight - (bodyHeight - itemTop));
				}
				kd.$_body.show();
			}
		},
		_onlistscroll: function(e) {
			kf.scrollTimer = setTimeout(function() {
				kf.scrollTimer = null;
			}, 300);
		},
		_onitemhover: function(e) {
			console.log('+_onitemhover');
			if (!kf.scrollTimer) {
				kf._setItemSelected($(this).index());
			}
		},
		_onitemclick: function(e) {
			console.log('+_onitemclick');
			kf._setItemSelected($(this).index());
		},
		onItemSelect: function(input, item) {
			 console.log('implement onItemSelect function');
		},
		_notifyItemSelected: function() {
			if (kd._count > 0 && kd._jsonItemsList) {
				kf.onItemSelect($Inst, kd._jsonItemsList[kd._selectedIndex]);
			}
		},
		_onenter: function(e) {
			console.log('+onEnter');
			kf._notifyItemSelected();
			kf._onunfocus();
		},
		_onkeypress: function(e) {
			console.log('+_onkeypress : '+ e.keyCode);
			if (e.keyCode === 10 || e.keyCode === 13) {
				e.preventDefault();
				e.data = $Inst;
				kf._onenter(e);
			}
		},
		_onkeyup: function(e) {
			console.log('+_onkeyup');
			var handled = true;
			switch(e.keyCode) {
			case KEY_UP:
				kf._setItemSelected(kd._selectedIndex - 1);
				break;
			case KEY_DOWN:
				kf._setItemSelected(kd._selectedIndex + 1);
				break;
			case KEY_ENTER:
				break;
			case KEY_LEFT:
			case KEY_RIGHT:
				kf._onfocus();
				break;
			default:
				console.log('keycode : '+e.keyCode);
				handled = false;
			}

			if (handled) {
				e.preventDefault();
				return;
			}
			var key = $Inst.val();
			(key.length >= kf.minLength && kf.source(key, kf._parse));
		},
	};

	var kf = $Inst.kf;
	var kd = $Inst.kd;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
};


function wfileupload($Inst, opts)
{
	console.log('+wfileupload : '+$Inst.prop('tagName'));
	// klass data
	$Inst.kd = {
		_name: 'fileupload',
		_ui: null,
		_uploads: [],
		_hidden: null,
	};
	// klass functors
	$Inst.kf =  {
		maxFiles: 1,
		mimeType: 'image',
		maxSize: 1024, // 1KB
		_create: function(e) {
			console.log('+_create['+kd._name+']');
			kd._ui = $('<div class="wt-progress-div" ></div>');
			kd._ui.css({width: $Inst.css('width')});
			kd._hidden = $('<input type="hidden" name="files" value="" >');
			$Inst.before(kd._hidden);
			$Inst.after(kd._ui);
			$Inst.on('change', kf._upload);
		},
		_destroy: function(e) {
			console.log('+_destroy['+kd._name+']');
			kd._ui.remove();
			kd._hidden.remove();
		},
		_upload: function(e) {
			console.log('+_upload');
			e.stopPropagation();
			e.preventDefault();
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

			var opts = $AppRequest.options();
			opts.url = '/upload/fileupload/';
			opts.processData = false;
			opts.contentType = false,
			opts.data = fdata;
			opts.progress = function(percent) {
				kf._progress(percent);
			};
			opts.complete = function(status, jsonObj) {
				if (status) {
					console.log("upload finished");
					var id = jsonObj.data.upload_id;
					kd._uploads.push(id);
					kd._hidden.val(kd._uploads.toString());
					uiBtn.data('request', null);
					uiBtn.data('upload_id', id);
					uiBtn.text('Remove');
					console.log('ids : '+kd._uploads.toString());
				} else {
					console.log('file upload failed reason : '+ JSON.stringify(jsonObj));
					uiItem.remove();
				}
			};
			var request = $AppRequest.file(opts);
			uiBtn.data('request', request);
		},
		_cancel: function(e) {
			console.log('+_cancel');
			e.preventDefault();
			var lThis = $(this);
			console.log(lThis.text());
			if (lThis.text() == 'Cancel') {
				var request = lThis.data('request');
				$AppRequest.abort(request);
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
			var pgbar = kd._ui.find('.wt-progress-bar');
			pgbar.css({width: progress+'%'});
			pgbar.html(progress+'%');
		}
	};

	var kd = $Inst.kd;
	var kf = $Inst.kf;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
}

function wswitchtab($Inst, opts)
{
	console.log('+wswitchtab : '+$Inst.prop('tagName'));
	// klass data
	$Inst.kd = {
		_name: 'switchtab',
		_total: 2,
		_active: null,
	};
	// klass functors
	$Inst.kf =  {
		_activeIndex: 0,
		_create: function(e) {
			console.log('+_create['+kd._name+']');
			//$Inst.find('.wt-switchtab-nav > a:nth-child(2)').
			var $elems = $Inst.find(".wt-switchtab-nav > li > a[rel]");
			kd._total = $elems.length;
			console.log("length : "+ kd._total);
			kd._active = $elems.eq(kf._activeIndex);
			var rel = kd._active.prop("rel");
			$Inst.find(rel).show();
			$elems.on("click", function(e){
				console.log("+tabClicked");
				e.preventDefault();
				var rel = kd._active.prop("rel");
				kd._active.removeClass("wt-switchtab-a");
				$Inst.find(rel).hide();
				kd._active = $(this);
				rel = kd._active.prop("rel");
				kd._active.prop("class", "wt-switchtab-a");
				$Inst.find(rel).show();
			});
		},
		_destroy: function(e) {
			console.log('+_destroy['+kd._name+']');
			kd._ui.remove();
		},
	};

	var kd = $Inst.kd;
	var kf = $Inst.kf;

	/* merge the options */
	for (var key in opts) {
		kf[key] = opts[key];
	}
	kf._create();
}

var $WgtTabs = {
	_$Inst: null,
	_name: 'stab',
	_total: 2,
	_active: null,
	_activeIndex: 0,

	new: function() {
		//return $AppWidgets.copy(this);
		return $.extend({}, {}, this);
	},
	attach: function($Inst, options) {
		console.log('+_create['+this._name+']');
		this._$Inst = $Inst;
		var $elems = $Inst.find(".wt-switchtab-nav > li > a[rel]");
		this._total = $elems.length;
		console.log("length : "+ this._total);
		this._active = $elems.eq(this._activeIndex);
		var rel = this._active.prop("rel");
		$Inst.find(rel).show();
		$elems.on("click", this, function(e){
			console.log("+tabClicked");
			e.preventDefault();
			var This = e.data;
			var rel = This._active.prop("rel");
			This._active.removeClass("wt-switchtab-a");
			$Inst.find(rel).hide();
			This._active = $(this);
			rel = This._active.prop("rel");
			This._active.prop("class", "wt-switchtab-a");
			$Inst.find(rel).show();
		});
		$Inst.on('unload', this._onremove);
	},
	detach: function() {
		console.log('+detach['+this._name+']');
		var $elems = this._$Inst.find(".wt-switchtab-nav > li > a[rel]");
		$elems.off("click");
	},
	_onremove: function(e) {
		console.log("+_onremove");
	},
};

var $WgtSuggesions = {
	_name: 'suggest',
	_$ui: null,
	_count: 0,
	_jsonObj: null,
	_selectedItem: null,
	_selectedIndex: 0,

	new: function() {
		return $.extend({}, {}, this);
	},
	attach: function($Inst, options) {
		console.log('+attach['+this._name+']');
		this._$ui = $('<ul class="wt-search-list wt-search-list-app" >');
		this._$ui.css({width: $Inst.css('width')});
		$Inst.after(this._$ui);
		this._$ui.on('mouseenter', 'li', this, this.onitemhover);
		$Inst.on("keyup", this, this.onkeyup);
		$Inst.on("keypress", this, this.onkeypress);
		$Inst.on("focus", this, this.onfocus);
		$Inst.on("blur", this, this.onunfocus);
		$Inst.on("unload", this, this.onunfocus);
	},
	detach: function() {
		this._$ui.remove();
		this._$ui = null;
	},
	_onremove: function(e) {
		var This = e.data;
		This.detach();
	},
	onfocus: function(e) {
		var This = e.data;
		This._$ui.show();
	},
	onunfocus: function(e) {
		var This = e.data;
		This._$ui.hide();
	},
	source: function(key, resp) {
		console.log('implement source function');
	},
	_parse: function(jsonObj) {
		console.log('+_parse');
		this._$ui.html('');
		if (jsonObj.length > 0) {
			var count = 0;
			for (i in jsonObj) {
				this._$ui.append(this.itemCreate(jsonObj[i]));
				count++;
			}
			this._jsonObj = jsonObj;
			this._count = count;
			this._selectedIndex = 0;
			this._selectedItem = this._$ui.children().eq(this._selectedIndex).addClass('wt-search-item-a');
			this._$ui.show();
		} else {
			this._count = 0;
			this._selectedIndex = 0;
			this._$ui.html('<div class="wt-search-item">No search results</div>');
			this._$ui.show();
		}
	},
	itemcreate: function(item) {
		console.log('implement itemcreate function');
		return '';
	},
	onitemhover: function(e) {
		console.log('+onitemhover');
		var index = $(this).index();
		console.log('old : '+ this._selectedIndex+ ' new: '+ index);
		if (this._selectedIndex != index) {
			this._$ui.children().eq(this._selectedIndex).removeClass('wt-search-item-a');
			this._selectedIndex = index;
			this._$ui.children().eq(this._selectedIndex).addClass('wt-search-item-a');
			if (this._jsonObj) {
				this.itemselect($Inst, this._jsonObj[index]);
			}
		}
	},
	onitemclick: function(e) {
		console.log('+onitemclick');
		var index = $(this).index();
		console.log('old : '+ this._selectedIndex+ ' new : '+ index);
		if (this._jsonData) {
			this._$ui.children().eq(this._selectedIndex).removeClass('wt-search-item-a');
			this._$ui.children().eq(index).addClass('wt-search-item-a');
			this.itemselect($Inst, this._jsonData[index]);
			this._selectedIndex = index;
		}
	},
	onitemselect: function(input, item) {
		 console.log('implement onitemselect function');
	},
	onitemselectcurrent: function() {
		if (this._count > 0 && this._jsonObj) {
			this.onitemselect($Inst, this._jsonObj[this._selectedIndex]);
		}
	},
	onenter: function(e) {
		console.log('+onenter');
		this.onitemselectcurrent();
		this.onunfocus();
	},
	onkeypress: function(e) {
		console.log('+_keyPress : '+ e.keyCode);
		if (e.keyCode === 10 || e.keyCode === 13) {
			e.preventDefault();
			e.data = $Inst;
			this.onenter(e);
		}
	},
	onkeyup: function(e) {
		console.log('+onkeyup');
		var handled = false;
		switch(e.keyCode) {
		case KEY_UP:
			if (this._selectedIndex > 0) {
				this._$ui.children().eq(this._selectedIndex).removeClass('wt-search-item-a');
				this._selectedIndex--;
				var child = this._$ui.children().eq(this._selectedIndex).addClass('wt-search-item-a');
				var cont = this._$ui;
				cont.scrollTop(child.position().top + cont.scrollTop());
				//cont.scrollTop(child.offset().top - cont.offset().top + cont.scrollTop());
				if (this._jsonObj) {
					this.itemselect($Inst, this._jsonObj[this._selectedIndex]);
				}
			}
			handled = true;
			break;
		case KEY_DOWN:
			if (this._selectedIndex < this._count - 1) {
				this._$ui.children().eq(this._selectedIndex).removeClass('wt-search-item-a');
				this._selectedIndex++;
				var child = this._$ui.children().eq(this._selectedIndex).addClass('wt-search-item-a');
				var cont = this._$ui;
				//console.log("child top : "+ child.position().top);
				//console.log("scroll top : "+ cont.scrollTop());
				cont.scrollTop(child.position().top + cont.scrollTop());
				if (this._jsonObj) {
					this.itemselect($Inst, this._jsonObj[this._selectedIndex]);
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
		var key = $Inst.val();
		(key.length >= this.minLength && this.source(key, this._parse));
	},
};

var $AppWidgets = {
	copy: function(obj) {
		return $.extend( {}, {}, obj);
	},
	stabs: $WgtTabs,
};

/****************** Exteded Jquery *******************/
jQuery.fn.exists = function(){return this.length>0;}
jQuery.fn.switchtab = function(options) { new wswitchtab(this, options); }
jQuery.fn.fileupload = function(options) { new wfileupload(this, options); }
jQuery.fn.suggestions = function(options) { new wsuggest(this, options); }
