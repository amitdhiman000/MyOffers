import $ from 'jquery';
import { AppUtil, ObjectUtil } from '../app/AppUtils';
import {HttpService, HttpResponseHandler} from '../app/HttpService';

export class UIFileUpload {

    _name: string = 'UIFileUpload';
	_uploads: any = [];
    
    $_hidden: any = null;
    $_ui: any =  null;
    $_self: any = null;
    
    _overrides: any = {};
    _config: any = {maxFiles: 1, mimeType: 'image', maxSize: 1024,};

    constructor($Inst: any, overrides: any, config: any) {
        console.log('+UIFileUpload : '+$Inst.prop('tagName'));
        ObjectUtil.merge(this._overrides, overrides);
        ObjectUtil.merge(this._config, config);
        this.$_self = $Inst;
        this._create();
    }

    _create() {
        let This = this;
        console.log('+_create['+This._name+']');
        This.$_ui = $('<div class="wt-progress-div" ></div>');
        This.$_ui.css({width: This.$_self.css('width')});
        This.$_hidden = $('<input type="hidden" name="files" value="" >');
        This.$_self.before(This.$_hidden);
        This.$_self.after(This.$_ui);
        This.$_self.on('change', This._upload.bind(This));
        This.$_self.on('DOMNodeRemoved', This._destroy.bind(This));
    }
        
    _destroy(e: any) {
        console.log('+_destroy['+this._name+']');
        this.$_ui.remove();
        this.$_hidden.remove();
    }

    _upload(e: any) {
        console.log('+_upload');
        e.stopPropagation();
        e.preventDefault();
        let This = this;
        let FileField = e.target;
        let Files = $(FileField)[0].files;
        let count = This.$_ui.find('.wt-progress-outer').length;
        console.log('count : '+count);
        let rem = This._config.maxFiles - count;
        if (rem == 0) {
            FileField.value = '';
            console.log('Already attached to max limit');
            return;
        }

        if (rem > Files.length) {
            rem = Files.length;
        }
        for (let i = 0; i < rem; ++i) {
            console.log('name : '+ Files[i].name + ' data : '+Files[i]);
            This._uploadFile(Files[i]);
        }
    }
    
    _uploadFile(file: any) {
        console.log('+_uploadFile');
        let This = this;
        let formData = new FormData();
        let fileName: string = file.name;
        let csrf: any = AppUtil.csrfToken();
        for (let key in csrf) {
            formData.append(key, csrf[key]);
        }
        formData.append('image', file);
        //(fileName.length > 20 && (fileName = fileName.substring(0, 20)));

        let $item = $(`<div class="wt-progress-outer" >'
                        <div class="wt-progress-inner">'
                        <div class="wt-progress-filename">${fileName}</div>'
                        <div class="wt-progress-bar">&nbsp;0%</div></div>'
                        <div class="wt-progress-control">'
                        <button class="ui-btn">Cancel</button>'
                        </div></div>`);
        let $cancelBtn = $item.find('.ui-btn');
        $cancelBtn.on('click', This._cancel.bind(This));
        This.$_ui.append($item);

        const callbacks = {
            progress_up :(percent: number) => {
                This._progress(percent);
            },
            complete: (status: boolean, jsonObj: any) => {
                if (status) {
                    console.log("upload finished");
                    let upload_ids = jsonObj.data.upload_ids;
                    This._uploads.push(upload_ids);
                    This.$_hidden.val(This._uploads.toString());
                    $cancelBtn.data('request', null);
                    $cancelBtn.data('upload_ids', upload_ids);
                    $cancelBtn.text('Remove');
                    console.log('ids : '+This._uploads.toString());
                } else {
                    console.log('file upload failed reason : '+ JSON.stringify(jsonObj));
                    $cancelBtn.remove();
                }
            }
        };
        let handler = new HttpResponseHandler(callbacks);
        let http = new HttpService();
        http.file('/upload/file/', formData, handler);
        $cancelBtn.data('request', http);
    }
    
    _cancel(e: any) {
        console.log('+_cancel');
        e.preventDefault();
        let This = this;
        let $item = $(e.target);
        console.log($item.text());
        if ($item.text() == 'Cancel') {
            let http: HttpService = $item.data('request');
            http.abort();
            console.log('aborted');
        } else {
            let id = $item.data('upload_id');
            let index = This._uploads.indexOf(id);
            This._uploads.splice(index, 1);
            This.$_hidden.val(This._uploads);
            console.log('ids : '+This._uploads.toString());
        }
        $item.parents('.wt-progress-outer').remove();
    }
    
    _progress(progress: number) {
        console.log('progress : '+progress+'%');
        let $pgbar = this.$_ui.find('.wt-progress-bar');
        $pgbar.css({width: progress+'%'});
        $pgbar.html(progress+'%');
    }
}