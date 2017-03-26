$(document).ready(function() {
	/* search box*/
	$(document).on('submit', '.ajax-form', ajaxFormSubmit);

	$("#search-input").suggestions({
		minLength: 2,
		_source: function(key, resp) {
			postRequest('/ajax/search/', {'key': key}, function(status, result){
				if (true == status) {
					resp(result.data);
				} else {
					console.log('error : '+JSON.stringify(result.error));
				}
			});
		},
		_itemCreate: function(item) {
			var uiItem = '<li>'
			+ '<div class="search-item">'
			+ '<a style="display:block; padding: 0.5em;" href="/offer/'+item.id+'">'+item.name+'</a>'
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
				location.href = '/offer/'+item.id
			}
		}
	});
});

function ajaxFormSubmit(e)
{
	console.log("+ajaxFormSubmit");
	e.preventDefault();
	var form = $(this);
	var action = form.attr('action');
	console.log('action : '+ action);
	postRequest(action, form.serialize(), (status, result) => {
		if (status === true) {
			Toast.show(result.message);
		} else {
			Toast.show(JSON.stringify(result.error));
			console.log('error : '+JSON.stringify(result.error));
		}
	});
}

function postRequest(pAction, pData, pCallback)
{
	console.log("+postRequest");
	$.ajax({url: pAction,
		data: pData,
		type: 'POST',
		async: true,
		dataType: 'text',
		beforeSend: function(xhr) {
			console.log('+beforeSend');
			//$.mobile.loading('show');
		},
		complete: function(res) {
			// This function is called at last for cleanup
			console.log('+comeplete :'+ res.status);
			//$.mobile.loading('hide');
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
}
};

/****************** cookie API ***********************/
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