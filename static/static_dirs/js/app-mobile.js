$(document).on('pagecreate', (e) => {
	console.log('+pagecreate');

	/********* Unregister all callbacks **********/
	$(document).off('keyup', '.search');
	$(document).off('click', '.submit');

	/********** Register the callbacks ***********/
	$(document).on('keyup', '.search', doSearch);
	$(document).on('click', '.submit', userFormPost);
});

$(document).on('pagecontainerbeforeshow', (e) => {
	console.log('+pagecontainerbeforeshow');
	(()=>{
		var id = $.mobile.activePage.attr('id');
		//console.log('page id : '+id);
		var decide = {
			'adminindexpage': ()=>{
			 	//console.log('register events for : '+id);
			},
			'indexpage': ()=>{
			 	//console.log('register events for index page');
			 	$('#'+id).off('click', '.user-reaction');
				$('#'+id).off('click', '.user-comment-link');
				$('#'+id).off('click', '.user-comment-submit');
			 	$('#'+id).on('click', '.user-reaction', userReactionPost);
				$('#'+id).on('click', '.user-comment-link', userCommentsShow);
				$('#'+id).on('click', '.user-comment-submit', userCommentPost);
			},
			'default': ()=>{
				//console.log('resiter default events'); 
			},
		}
		return (decide[id])?decide[id]():decide['default']();
	})();
	//$(this).enhanceWithin();
});

$(document).on('pagecontainershow', (e) => {
	console.log('+pagecontainershow');
});

function userFormPost(e)
{
	console.log("+userFormPost");
	e.preventDefault();
	var form = $(this).parents('form');
	var action = form.attr('action');
	console.log('action : '+ action);
	postRequest(action, form.serialize(), (status, result) => {
		if (status === true) {
			Toast.show(result.message);
		} else {
			Toast.show(result.error);
			console.log('error : '+result.error);
		}
	});
}

function showSearchList(pThis, status)
{
	console.log('+showSearchList : '+status);
	if (status === true) {
		pThis.parents(".search-box").find(".search-results").show();
	} else {
		pThis.parents(".search-box").find(".search-results").hide();
	}
}

function doSearch(e)
{
	console.log('+doSearch');
	var This = $(this);
	//var list = $('#search-results');
	var list = This.parents(".search-box").find(".search-results");
	var key = This.val();
	if ('' === key) {
		list.hide();
		return;
	}
	var data = {'keyword': key};
	postRequest('/ajax/search/', data, (status, result) => {
		if (status === true) {
			var jsonData = result.data;
			var it = null;
			list.empty();
			list.show();
			for (i in jsonData) {
				it = '<li data-filtertext="'+ jsonData[i] +'"><a href="#">'+ jsonData[i] +'</a></li>';
				//console.log('item : '+ item);
				list.append(it);
			}
			list.listview('refresh');
		} else {
			console.log('failed to search');
		}
	});
}

function userReactionPost(e)
{
	console.log("+userReactionPost");
	var This = $(this);
	var reaction = This.text();
	var article_id = This.parents('.user-reaction-div').attr('article-id');
	console.log('+userReactionPost');
	var data = {'user_reaction':reaction, 'article_id':article_id}
	postRequest('/post/post-reaction/', data, (status, result) => {
		if (status === true) {
			var count = 0;
			var other = null;
			switch(reaction) {
			case 'like':
				count = parseInt(This.attr('article-likes')) + 1;
				This.attr('article-likes', count);
				This.text('liked');
				This.next().text('['+count+']');
				other = This.parent().next();
				resetDislike(other);
				This.parent().attr('dais-active', 'true');
				break;
			case 'dislike':
				count = parseInt(This.attr('article-dislikes')) + 1;
				This.attr('article-dislikes', count);
				This.text('disliked');
				This.next().text('['+count+']');
				other = This.parent().prev();
				resetLike(other);
				This.parent().attr('dais-active', 'true');
				break;
			case 'liked':
				resetLike(This.parent());
				break;
			case 'disliked':
				resetDislike(This.parent());
				break;
			default:
				break;
			}
		}
	});
}

function resetLike(obj)
{
	console.log('+resetLike');
	if (obj.attr('dais-active') === 'true') {
		var likeObj = obj.children('.user-reaction');
		var count = parseInt(likeObj.attr('article-likes')) - 1;
		likeObj.attr('article-likes', count);
		likeObj.next().text((count>0)?'['+count+']':'');
		likeObj.text('like');
		obj.attr('dais-active', 'false');
		console.log('-resetLike');
	}
}

function resetDislike(obj)
{
	console.log('+resetDislike');
	if (obj.attr('dais-active') === 'true') {
		var likeObj = obj.children('.user-reaction');
		var count = parseInt(likeObj.attr('article-dislikes')) - 1;
		likeObj.attr('article-dislikes', count);
		likeObj.next().text((count>0)?'['+count+']':'');
		likeObj.text('dislike');
		obj.attr('dais-active', 'false');
		console.log('-resetDislike');
	}
}

function userCommentsShow(e)
{
	e.preventDefault();
	console.log("+userCommentsShow");
	var cw = $(this).next('.user-comments-wid');
	if (cw.exists()) {
		console.log("hiding comment widget");
		console.log("length : "+ cw.length);
		console.log("name : "+ cw.prop('tagName'));
		(cw.is(":visible"))?cw.hide():cw.show();
	} else {
		console.log("creating comment widget");
		var article_id = $(this).parents('.user-reaction-div').attr('article-id');
		var xx = $('#user-comments-wid').clone().removeAttr('id');
		xx.find('#article_id').val(article_id);
		xx.insertAfter($(this)).show();
		loadComments(xx.find('.user-comments'), article_id, 0, 10);
	}
}

function loadComments(pThis, art_id, start, count)
{
	console.log('+loadComments');
	var data = {'article_id':art_id, 'comment_start':start, 'comment_count':count};
	postRequest('/post/load-post-comments/', data, (status, result) => {
		displayComments(pThis, result.data);
	});
}

function displayComments(pThis, cmts)
{
	console.log('+publishComments');
	pThis.show();
	if (!cmts) {
		console.log('list is empty');
		return;
	}
	for (i = 0; i < cmts.length; ++i) {
		appendComment(pThis, cmts[i]);
	}
	//pThis.show();
}

function appendComment(pThis, cmt)
{
	console.log('+appendComment');
	var html = '<div class ="user-comment" comment-id="'+cmt.id+'" >'
		+ '<div class="user-name" > <strong>' + cmt.author_name + '</strong></div>'
		+ '<div class="comment-text" >' + cmt.text + '</div>'
		+ '<div class="h-bar" ></div>'
		+ '</div>'
	pThis.append(html);
}

function userCommentPost(e)
{
	e.preventDefault();
	console.log('+userCommentPost');
	var This = $(this);
	var form = This.parents('form');
	var action = form.attr('action');
	var cmtBox = form.find('.comment-text');
	var text = cmtBox.val();
	if (text == '') {
		console.log('Comment cannot be empty');
		Toast.show('Comment cannot be empty');
		return;
	}
	console.log("comment : "+text);
	var data = form.serialize();
	postRequest(action, data, (status, result) => {
		if(status === true) {
			var cmtCont = This.parents('.user-comments-wid').children('.user-comments');
			appendComment(cmtCont, result.data);
			cmtBox.val('');
			Toast.show('Posted');
		}
	});
}


function followTopic(pThis)
{
	console.log("+followTopic");
	var form = $('#topic-select-form');
	var action = form.attr('action');
	var id = parseInt(pThis.attr('data-tid'));
	var followed = parseInt(pThis.attr("data-tf"));
	var data = form.serializeArray();
	data.push({name: 'topic_id', value: id}, {name: 'topic_followed', value: followed});
	console.log("data : "+JSON.stringify(data));

	var lPromise = jQuery.data(pThis, 'promise');
	console.log("promise : "+lPromise);
	if (lPromise != undefined) {
		lPromise.reject();
		Jquery.removeData(This, 'promise');
	}
	
	lPromise = new Promise(function(resolve, reject){
		postRequest(action, data, (status, result)=>{
			(status === true) ? resolve(result) : reject(result);
		});
	});
	jQuery.data(pThis, 'promise', lPromise);

	lPromise.then(function(arg){
		console.log('resolved : '+arg);
		console.log("followed : "+followed);
		if (followed == 0) {
			pThis.removeClass('topic-item-uf');
			pThis.addClass('topic-item-f');
			pThis.attr('data-tf', 1);
		} else {
			pThis.removeClass('topic-item-f');
			pThis.addClass('topic-item-uf');
			pThis.attr('data-tf', 0);
		}
	}).catch(function(arg){
		console.log('rejected : '+arg);
	});
}

function postRequest(pAction, pData, pCallback)
{
	console.log("+postRequest");
	$.ajax({url: pAction,
		data: pData,
		type: 'POST',
		async: 'true',
		dataType: 'text',
		beforeSend: function(xhr) {
			console.log('+beforeSend');
			$.mobile.loading('show');
		},
		complete: function(res) {
			// This function is called at last for cleanup
			console.log('+comeplete :'+ res.status);
			$.mobile.loading('hide');
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
					pCallback(true, jsonData);
					break;
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