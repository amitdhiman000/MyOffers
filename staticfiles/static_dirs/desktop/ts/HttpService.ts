import {$} from '../../libs/jquery/jquery-3.3.1.min';
import {UIToast} from './UIToast'


export class HttpResponseHandler  {
    progress_up = function(p: number): any { console.log('default_progress_up'); };
	progress_dn = function(p: number): any { console.log('default_progress_dn');  };
    complete = function(s: any, d: any): any { console.log('default_complete');  };
    constructor(handlers: any) {

    }
};

export class HttpService {
    _handle: any = null;
    constructor()
    {}
    
	abort(): any {
		this._handle.abort();
    }
    
	get(url: string, data: any, callback: any): any {
		console.log('+get');
		let options = {type:'GET', 'url': url, 'data': data};
		let handler: HttpResponseHandler = new HttpResponseHandler({complete: callback});
		console.log(handler);
		return this._request(handler, options);
    }
    
	post(url: string, data: any, callback: any): any {
		console.log("+post");
		let options = {type:'POST', 'url': url, 'data': data};
		let handler: HttpResponseHandler = new HttpResponseHandler({complete: callback});
		console.log(handler);
		return this._request(handler, options);
    }
    
	file(url: string, data: any, handler: any): any {
		console.log("+file");
		let options = {type:'POST', 'url': url, 'data': data, processData: false, contentType: false};
		return this._request(handler, options);
    }
    
	public request(handler: any, options: any): any {
		console.log("+request");
		return this._request(handler, options);
    }
    
	private _request(handler: any = HttpResponseHandler, options: any = {}): any {
		let methods = {
			dataType: 'text',
			xhr: () => {
				var xhr = $.ajaxSettings.xhr();
				xhr.upload.onprogress = function(evt: any) {
					if (evt.lengthComputable) {
						var percent = 100 * parseInt(evt.loaded / evt.total);
						handler.progress0(percent);
					}
				};
				xhr.onprogress = function(evt: any) {
					if (evt.lengthComputable) {
						var percent = 100 * parseInt(evt.loaded / evt.total);
						handler.progress1(percent);
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
}