//import * as $ from '../../libs/jquery/jquery-3.3.1.min';
//import * as $ from 'jquery'; // esModuleInterop:false in tsconfig.json
import $ from 'jquery';
import {App} from './App';
import { UIOptionList, UITabs, UIFileUpload } from './UIWidgets'

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
