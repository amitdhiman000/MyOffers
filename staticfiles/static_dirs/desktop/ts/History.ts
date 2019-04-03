import {$} from '../../libs/jquery/jquery-3.3.1.min';
import { HttpService } from './HttpService';
import {App} from './App';

export class History {
	constructor()
	{
		console.log("+History");
		this.init();
	}

	init()
	{
		console.log("+AppHistory::init");
		if (window.history && window.history.pushState) {
			let afterGetResponse = (status: any, data: any, state: any) => {
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
			let makeRequest = (state: any) => {
				let httpService: HttpService = new HttpService();
				httpService.get(state.url, 'pid='+state.dest[1],
					function(status: any, data: any) {
						afterGetResponse(status, data, state);
					});
			}
			$(document).on('click', 'a[data-dest]', function (e) {
				e.preventDefault();
				console.log("+a");
				let This = $(this);
				let url:string = This.attr("href");
				let dest:string = This.attr("data-dest").split(':');
				let title:string = This.text()+' | '+App.Instance().name();
				let state:any = {url:url, title:title, dest:dest,};
				makeRequest(state);
			});

			window.addEventListener('popstate', function(e) {
				console.log('+popstate');
				console.log(JSON.stringify(e.state));
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
}