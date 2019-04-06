import $ from 'jquery';
import {UIToast} from './UIToast';
import {ObjectUtil} from './AppUtils';


export class HttpResponseHandler  {
    progress_up = function(p: number): any { console.log('default_progress_up'); };
	progress_dn = function(p: number): any { console.log('default_progress_dn');  };
    complete = function(s: any, d: any): any { console.log('default_complete');  };
    constructor(handlers: any) {
		ObjectUtil.Instance().merge(this, handlers);
    }
};
 
export class HttpService {
    _handle: any = null;
    constructor()
    {}
    
	abort(): any {
		if (this._handle) {
			this._handle.abort();
		}
    }
    
	get(url: string, data: any, callback: any): any {
		console.log('+get');
		let options = {type:'GET', 'url': url, 'data': data};
		let handler = new HttpResponseHandler({complete: callback});
		console.log(handler);
		return this._request(options, handler);
    }
    
	post(url: string, data: any, callback: any): any {
		console.log("+post");
		let options = {type:'POST', 'url': url, 'data': data};
		let handler = new HttpResponseHandler({complete: callback});
		console.log(handler);
		return this._request(options, handler);
    }
    
	file(url: string, data: any, handler?: any): any {
		console.log("+file");
		let options = {type:'POST', 'url': url, 'data': data, processData: false, contentType: false};
		return this._request(options, handler);
    }
    
	public request(options: any, handler?: any): any {
		console.log("+request");
		return this._request(options, handler);
    }
    
	private _request(options: any, handler: any = HttpResponseHandler): any {
		let methods = {
			dataType: 'text',
			xhr: () => {
				let xhr = $.ajaxSettings.xhr();
				xhr.upload.onprogress = function(evt: any) {
					if (evt.lengthComputable) {
						let percent:number = 100 * (evt.loaded / evt.total);
						handler.progress_up(percent);
					}
				};
				xhr.onprogress = function(evt: any) {
					if (evt.lengthComputable) {
						let percent: number = 100 * (evt.loaded / evt.total);
						handler.progress_dn(percent);
					}
				};
				return xhr;
			},
			complete: function(res: any) {
				console.log('+comeplete : '+ res.status);
			},
			success: (data: any, status: number, xhr: any) => {
				console.log('+success');
				let mimeType: string = xhr.getResponseHeader("content-type");
				console.log('content-type: '+ mimeType);
				if (mimeType.indexOf('json') > -1) {
					console.log('data : ' + data);
					let jsonObj: any = JSON.parse(data);
					switch(jsonObj.status) {
						case 302:
							console.log('redirect');
							location.href = jsonObj.url;
							break;
						case 200:
						case 204:
							handler.complete(true, jsonObj);
							break;
						case 401:
						default:
							handler.complete(false, jsonObj);
							break;
					}
				} else if (mimeType.indexOf('html') > -1) {
					handler.complete(true, data);
				} else {
					console.log('content-type: unknown');
					handler.complete(false, {'message': 'Unknown response', 'data':'unexpected content type'});
				}
			},
			error: (xhr: any, error: any) => {
				console.log('+error : '+xhr.status);
				UIToast.Instance().show('Network error occured');
				handler.complete(false, {'message': 'Network failed', 'data': {error} });
			}
		};
		$.extend(options, methods);
		this._handle = $.ajax(options);
	}
};