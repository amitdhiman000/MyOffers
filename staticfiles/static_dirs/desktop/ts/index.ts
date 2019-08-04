//import * as $ from '../../libs/jquery/jquery-3.3.1.min';
//import * as $ from 'jquery'; // esModuleInterop:false in tsconfig.json
import $ from 'jquery';
import { App } from './app/App';
import { UINoti } from './widgets/UINoti';
import { UIToast } from './widgets/UIToast';
import { UIOverlay } from './widgets/UIOverlay';
import { UIModal } from './widgets/UIModal';
import { UIDialog } from './widgets/UIDialog';
import { UIOptionList } from './widgets/UIOptionList';
import { UIFileUpload } from './widgets/UIFileUpload';
import { UITabs } from './widgets/UITabs';

import { AddressPicker } from './widgets/AddressPicker';
import { AjaxForm, AppFormHandler } from './app/AppForm';
import { HttpResponseHandler, HttpService } from './app/HttpService';
import { GoogleMap } from './app/GoogleMap';
import { ObjectUtil, AppUtil, DomUtil, FormUtil } from './app/AppUtils';
import { AppEvent, AppGeo, AppCookie, AppStorage } from './app/AppUtils';

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
    AddressPicker,
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