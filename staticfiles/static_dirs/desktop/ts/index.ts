//import * as $ from '../../libs/jquery/jquery-3.3.1.min';
//import * as $ from 'jquery'; // esModuleInterop:false in tsconfig.json
import $ from 'jquery';
import { App } from './App';
import { UIOptionList, UITabs, UIFileUpload } from './UIWidgets'
import { AjaxForm, AppFormHandler } from './AppForm';
import { UINoti } from './UINoti';
import { UIToast } from './UIToast';
import { HttpResponseHandler, HttpService } from './HttpService';
import { GoogleMap } from './GoogleMap';
import { ObjectUtil, AppUtil, FormUtil } from './AppUtils';
import { AppEventHandler, AppGeo, AppCookie, AppStorage } from './AppUtils';

/* Export for AppLib to use in html <script> tags */
export {
    AjaxForm,
    AppFormHandler,
    UINoti,
    UIToast,
    HttpResponseHandler,
    HttpService,
    GoogleMap,
    ObjectUtil,
    AppUtil,
    FormUtil,
    AppEventHandler,
    AppGeo,
    AppCookie,
    AppStorage,
};


function initPlugins()
{
    $.fn.extend({
        exists: function() {return this.length>0;},
        OptionList: function(overrides: any, config: any) { new UIOptionList(this, overrides, config); },
        Tabs: function(overrides: any, config: any) { new UITabs(this, overrides); },
        FileUpload: function(overrides: any, config: any) { new UIFileUpload(this, overrides, config); },
    });
}

$(function(){
    initPlugins();
    let app = App.Instance();
    app.show();
});