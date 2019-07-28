//import * as $ from '../../libs/jquery/jquery-3.3.1.min';
//import * as $ from 'jquery'; // esModuleInterop:false in tsconfig.json
import $ from 'jquery';
import { App } from './App/App';
import { UIOptionList, UITabs, UIFileUpload } from './App/UIWidgets';
import { UIOverlay, UIModal, UIDialog } from './App/UIWidgets';
import { AjaxForm, AppFormHandler } from './App/AppForm';
import { UINoti } from './App/UINoti';
import { UIToast } from './App/UIToast';
import { HttpResponseHandler, HttpService } from './App/HttpService';
import { GoogleMap } from './App/GoogleMap';
import { ObjectUtil, AppUtil, DomUtil, FormUtil } from './App/AppUtils';
import { AppEvent, AppGeo, AppCookie, AppStorage } from './App/AppUtils';

/* Export for AppLib to use in html <script> tags */
export {
    AjaxForm,
    AppFormHandler,
    UINoti,
    UIToast,
    UIOverlay,
    UIModal,
    UIDialog,
    HttpResponseHandler,
    HttpService,
    GoogleMap,
    ObjectUtil,
    AppUtil,
    DomUtil,
    FormUtil,
    AppEvent,
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