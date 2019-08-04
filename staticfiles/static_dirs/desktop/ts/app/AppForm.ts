import { HttpService, HttpResponseHandler } from "./HttpService";
import {FormUtil, ObjectUtil} from './AppUtils';
import {UINoti} from '../widgets/UINoti';

export class AjaxForm {
    $_form: any = null;
    constructor($form: any) {
        this.$_form = $form;
	}
	
	static make($form: any): AjaxForm {
		return new this($form);
	}

    submit(e: any) {
        console.log("+$AjaxFrom::submit");
        let $form = this.$_form;
		e.$form = $form;
		let action = $form.attr('action');
		if (!action) action = window.location.href;
		console.log('action : ' + action);

		let handler = $form.data('data-handler');
		handler = (handler)? handler: window[$form.attr('data-delegate')];

		if (handler) {
			handler.before = (handler.before)? handler.before : this.before;
			handler.after = (handler.after)? handler.after: this.after;
		} else {
			handler = this;
		}

		if (handler.before(e) === false)
			return;

		function onResponse(status: boolean, json: any) {
			e.status = status;
			e.resp = json;
			handler.after(e);
        }
        
        let http = new HttpService();
		let fileFields = $form.find('[type=file]');
		if (fileFields.exists()) {
			console.log('file is present');
			let httpResHandler = new HttpResponseHandler({complete: onResponse});
			let reqData = new FormData($form[0]);
			http.file(action, reqData, httpResHandler);
		} else {
			let reqData = $form.serialize();
			http.post(action, reqData, onResponse);
		}
    }
    
	before(e: any) {
		console.log('+AjaxForm::before');
		return true;
    }
    
	after(e: any) {
        console.log('+AjaxForm::after');
		if (e.status) {
            UINoti.make({title:"Successful", text:e.resp.message}).show();
		} else {
			let errors = '';
			for (let key in e.resp.data) {
				console.log(key + ' : '+ e.resp.data[key]);
				errors += e.resp.data[key]+'<br />';
            }
            UINoti.make({title:e.resp.message, text:errors}).show();
		}
	}
};


export class AppFormHandler {
	constructor(config: any) {
		ObjectUtil.merge(this, config);
	}

	before(e: any) {
		console.log("+AppFormSaveHandler::before");
		return true;
	}

	after(e: any) {
		console.log("+AppFormSaveHandler::after");
		if (e.status) {
			let vals = e.resp.data;
			let $form = e.$form;
			for (let key in vals) {
				let val = vals[key];
				console.log(key+' : '+val);
				FormUtil.setValByName($form, key, val);
			}
            $form.find('input[type=button]').click();
            UINoti.make({title:'Done!!', text:e.resp.message}).show();
		} else {
			let errors = '';
			for (let err in e.resp.data) {
				errors += e.resp.data[err] + '<br />';
            }
            UINoti.make({title:e.resp.message, text:errors}).show();
		}
	}
};