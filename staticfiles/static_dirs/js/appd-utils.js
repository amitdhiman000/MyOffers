$(function() {
	$(document).on('submit', 'form.ajax-form', ajaxFormSubmit);
	/*Initialize History*/
	initHistory();
	/*Initialize search*/
	initSearch();
});

function initHistory()
{
	if (window.history && window.history.pushState) {
		$(document).on('click', 'a[data-dest]', function (e) {
			e.preventDefault();
			var This = $(this),
			url = This.attr("href"),
			dest = This.attr("data-dest"),
			title = This.text()+' :: My Offers';
			history.pushState({url:url, title:title, dest:dest,}, title, url);
			document.title = title;
			getRequest(url, dest);
		});

		$(window).on('popstate', function (e) {
			var state = e.originalEvent.state;
			if (state !== null) {
				document.title = state.title;
				getRequest(state.url, state.dest);
			} else {
				console.log("nothing to show");
				//document.title = 'World Regions';
				//$("#content").empty();
			}
		});
	}
}

function initSearch()
{
	console.log('+initSearch');
	$("#search-input").suggestions({
		minLength: 2,
		_source: function(key, resp) {
			postRequest('/search/offer/', {'key': key}, function(status, result){
				if (true == status) {
					resp(result.data);
				} else {
					console.log('error : '+JSON.stringify(result.error));
				}
			});
		},
		_itemCreate: function(item) {
			var uiItem = '<li>'
			+ '<div class="ui-search-item">'
			+ '<a style="display:block; padding: 0.5em;" href="'+item.url+'">'+item.name+'</a>'
			+ '</div>'
			+ '</li>';
			return uiItem;
		},
		_itemSelect: function(input, item) {
			input.val(item.name);
		},
		_onEnter: function(e) {
			console.log('+_onEnter1');
			var Inst = e.data;
			Inst.kf._onunfocus();
			if (Inst.kd._count > 0) {
				var item = Inst.kd._jsonData[Inst.kd._selectedIndex];
				location.href = item.url
			}
		}
	});
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

	postRequest(action, form.serialize(), (status, result) => {
		if (handle && handle.after) {
			e.status = status;
			e.result = result;
			handle.after(e);
		} else {
			if (status === true) {
				Toast.show(result.message);
			} else {
				Toast.show(JSON.stringify(result.error));
			}
		}
	});
}

function afterResponse(e,status,result) {
	console.log("+afterResponse");
	if (e.status == false) {
		var errors = '';
		for (var key in e.result.error) {
			console.log(key);
			console.log(e.result.error[key]);
			errors += e.result.error[key]+'<br />';
		}
		$('.ui-errors').html(errors);
	} else {
		$('.ui-errors').html('');
	}
}

function postRequest(pAction, pData, pCallback)
{
	console.log("+postRequest");
	$.ajax({url: pAction,
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
				jsonData = jQuery.parseJSON(data);
				switch(jsonData.status) {
				case 302:
					console.log('redirect');
					location.href = jsonData.url;
					break;
				case 200:
				case 204:
					pCallback(true, jsonData);
					break;
				default:
					pCallback(false, jsonData);
					break;
				}
			} else if (mimeType.indexOf('html') > -1) {
				pCallback(true, data);
			} else {
				pCallback(false, {'error':'unexpected content type'});
			}
		},
		error: function (xhr,error) {
			console.log('status : '+xhr.status);
			Toast.show('Network error occured');
			pCallback(false, {'error':error});
		}
	});
}

function getRequest((url, dest)
{
	$.get(url).done(function(data) {
		$(dest).html(data);
	}).fail(function() {
    	$(dest).html("<h1>Failed to load page</h1>");
  	});
}

/****************** Exteded Jquery *******************/
jQuery.fn.exists = function(){return this.length>0;}
/****************** Toast API ************************/
var Toast =  {
show: function(text='Error', timeout=1200) {
	//$('.toast').text(text).fadeIn(500).delay(timeout).fadeOut(500);
	$('.toast').fadeIn({duration: 500, start: function() {$(this).text(text);}}).delay(timeout).fadeOut(500);
},
hide: function() {
	$('.toast').hide();
}};
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
