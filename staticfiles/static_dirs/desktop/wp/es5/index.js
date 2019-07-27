var AppLib =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "../static_dirs/desktop/ts/index.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "../static_dirs/desktop/ts/App/App.ts":
/*!********************************************!*\
  !*** ../static_dirs/desktop/ts/App/App.ts ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function($) {
Object.defineProperty(exports, "__esModule", { value: true });
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var AppHistory_1 = __webpack_require__(/*! ./AppHistory */ "../static_dirs/desktop/ts/App/AppHistory.ts");
var AppComponents_1 = __webpack_require__(/*! ./AppComponents */ "../static_dirs/desktop/ts/App/AppComponents.ts");
var AppForm_1 = __webpack_require__(/*! ./AppForm */ "../static_dirs/desktop/ts/App/AppForm.ts");
var App = /** @class */ (function () {
    function App() {
        this._history = null;
        this._header = null;
        this._name = "App";
        this._history = new AppHistory_1.AppHistory();
        this._header = new AppComponents_1.AppHeader();
        this.init();
    }
    App.Instance = function () {
        return this._instance || (this._instance = new this());
    };
    App.prototype.init = function () {
        console.log("+App::init");
        $(document).on("submit", "form.ajax-form", function (e) {
            e.preventDefault();
            AppForm_1.AjaxForm.make($(this)).submit(e);
        });
        $(document).on("click", ".app_vlist_exp_item > a", function (e) {
            e.preventDefault();
            $(this).parent().toggleClass("expanded");
        });
        $(document).on("click", function (e) {
            //e.stopPropagation();
            $(".ui-dropcontent").hide();
        });
        $(document).on("click", ".ui-dropbtn", function (e) {
            e.stopPropagation();
            $(e.target).parents(".ui-dropdown").find(".ui-dropcontent").toggle();
        });
        $(document).on("click", ".ui-hovermenu", function (e) {
            console.log("hovermenu clicked");
            e.preventDefault();
            e.stopPropagation();
        });
    };
    App.prototype.show = function () {
        console.log("+App::show");
    };
    App.prototype.name = function () {
        return AppUtils_1.AppUtil.appName();
    };
    App._instance = null;
    return App;
}());
exports.App = App;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "jquery")))

/***/ }),

/***/ "../static_dirs/desktop/ts/App/AppComponents.ts":
/*!******************************************************!*\
  !*** ../static_dirs/desktop/ts/App/AppComponents.ts ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var HttpService_1 = __webpack_require__(/*! ./HttpService */ "../static_dirs/desktop/ts/App/HttpService.ts");
var AppNavbar = /** @class */ (function () {
    function AppNavbar(config) {
        this._config = { 'navbar_btn': '#navbar_btn' };
        AppUtils_1.ObjectUtil.merge(this._config, config);
        jquery_1.default(this._config['navbar_btn']).on('click', this._onNavClicked.bind(this));
    }
    AppNavbar.prototype._onNavClicked = function (e) {
        console.log("+AppNavBar::_onNavClicked");
        var appleft = document.getElementById("app_leftnav");
        var apppage = document.getElementById("app_page");
        if (appleft && apppage) {
            console.log("marginLeft: " + appleft.style.marginLeft);
            if (appleft.style.marginLeft !== "-20%") {
                appleft.style.marginLeft = "-20%";
                apppage.style.width = "95%";
                apppage.style.margin = "0 auto";
            }
            else {
                appleft.style.marginLeft = "0";
                apppage.style.marginLeft = "20%";
                apppage.style.width = "80%";
            }
        }
    };
    return AppNavbar;
}());
exports.AppNavbar = AppNavbar;
;
var AppSearchbar = /** @class */ (function () {
    function AppSearchbar(selector) {
        if (selector === void 0) { selector = "#app_search_input"; }
        jquery_1.default(selector).OptionList({
            'source': this.source,
            'itemCreate': this.itemCreate,
            'onItemSelect': this.onItemSelect,
            'onEnter': this.onEnter,
        }, { minLength: 2, });
    }
    AppSearchbar.prototype.source = function (key, respCB) {
        var http = new HttpService_1.HttpService();
        http.post('/search/offer/', { 'key': key }, function (status, json) {
            if (true == status) {
                respCB(json.data);
            }
            else {
                console.log('data : ' + JSON.stringify(json.data));
            }
        });
    };
    AppSearchbar.prototype.itemCreate = function (item) {
        var $item = "<li>\n                        <div class=\"wt-search-item\">\n                            <a style=\"display:block; padding: 0.5em;\" href=\"" + item.url + "\"> " + item.name + "</a>\n                        </div>\n                    </li>";
        return $item;
    };
    AppSearchbar.prototype.onItemSelect = function ($input, item) {
        $input.val(item.name);
    };
    AppSearchbar.prototype.onEnter = function ($input, item) {
        console.log('+onEnter');
        if (item) {
            location.href = item.url;
        }
    };
    return AppSearchbar;
}());
exports.AppSearchbar = AppSearchbar;
var AppHeader = /** @class */ (function () {
    function AppHeader() {
        this._navbar = null;
        this._searchbar = null;
        console.log("+AppHeader");
        this._navbar = new AppNavbar();
        this._searchbar = new AppSearchbar();
    }
    return AppHeader;
}());
exports.AppHeader = AppHeader;
;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/AppForm.ts":
/*!************************************************!*\
  !*** ../static_dirs/desktop/ts/App/AppForm.ts ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var HttpService_1 = __webpack_require__(/*! ./HttpService */ "../static_dirs/desktop/ts/App/HttpService.ts");
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var UINoti_1 = __webpack_require__(/*! ./UINoti */ "../static_dirs/desktop/ts/App/UINoti.ts");
var AjaxForm = /** @class */ (function () {
    function AjaxForm($form) {
        this.$_form = null;
        this.$_form = $form;
    }
    AjaxForm.make = function ($form) {
        return new this($form);
    };
    AjaxForm.prototype.submit = function (e) {
        console.log("+$AjaxFrom::submit");
        var $form = this.$_form;
        e.$form = $form;
        var action = $form.attr('action');
        if (!action)
            action = window.location.href;
        console.log('action : ' + action);
        var handler = $form.data('data-handler');
        handler = (handler) ? handler : window[$form.attr('data-delegate')];
        if (handler) {
            handler.before = (handler.before) ? handler.before : this.before;
            handler.after = (handler.after) ? handler.after : this.after;
        }
        else {
            handler = this;
        }
        if (handler.before(e) === false)
            return;
        function onResponse(status, json) {
            e.status = status;
            e.resp = json;
            handler.after(e);
        }
        var http = new HttpService_1.HttpService();
        var fileFields = $form.find('[type=file]');
        if (fileFields.exists()) {
            console.log('file is present');
            var httpResHandler = new HttpService_1.HttpResponseHandler({ complete: onResponse });
            var reqData = new FormData($form[0]);
            http.file(action, reqData, httpResHandler);
        }
        else {
            var reqData = $form.serialize();
            http.post(action, reqData, onResponse);
        }
    };
    AjaxForm.prototype.before = function (e) {
        console.log('+AjaxForm::before');
        return true;
    };
    AjaxForm.prototype.after = function (e) {
        console.log('+AjaxForm::after');
        if (e.status) {
            UINoti_1.UINoti.make({ title: "Successful", text: e.resp.message }).show();
        }
        else {
            var errors = '';
            for (var key in e.resp.data) {
                console.log(key + ' : ' + e.resp.data[key]);
                errors += e.resp.data[key] + '<br />';
            }
            UINoti_1.UINoti.make({ title: e.resp.message, text: errors }).show();
        }
    };
    return AjaxForm;
}());
exports.AjaxForm = AjaxForm;
;
var AppFormHandler = /** @class */ (function () {
    function AppFormHandler(config) {
        AppUtils_1.ObjectUtil.merge(this, config);
    }
    AppFormHandler.prototype.before = function (e) {
        console.log("+AppFormSaveHandler::before");
        return true;
    };
    AppFormHandler.prototype.after = function (e) {
        console.log("+AppFormSaveHandler::after");
        if (e.status) {
            var vals = e.resp.data;
            var $form = e.$form;
            for (var key in vals) {
                var val = vals[key];
                console.log(key + ' : ' + val);
                AppUtils_1.FormUtil.setValByName($form, key, val);
            }
            $form.find('input[type=button]').click();
            UINoti_1.UINoti.make({ title: 'Done!!', text: e.resp.message }).show();
        }
        else {
            var errors = '';
            for (var err in e.resp.data) {
                errors += e.resp.data[err] + '<br />';
            }
            UINoti_1.UINoti.make({ title: e.resp.message, text: errors }).show();
        }
    };
    return AppFormHandler;
}());
exports.AppFormHandler = AppFormHandler;
;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/AppHistory.ts":
/*!***************************************************!*\
  !*** ../static_dirs/desktop/ts/App/AppHistory.ts ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var HttpService_1 = __webpack_require__(/*! ./HttpService */ "../static_dirs/desktop/ts/App/HttpService.ts");
var App_1 = __webpack_require__(/*! ./App */ "../static_dirs/desktop/ts/App/App.ts");
var AppHistory = /** @class */ (function () {
    function AppHistory() {
        console.log("+AppHistory");
        this.init();
    }
    AppHistory.prototype.init = function () {
        console.log("+AppHistory::init");
        if (window.history && window.history.pushState) {
            var afterGetResponse_1 = function (status, data, state) {
                console.log('afterGetResponse');
                if (status) {
                    jquery_1.default(state.dest[0]).html(data);
                    history.pushState(state, state.title, state.url);
                    document.title = state.title;
                }
                else {
                    jquery_1.default(state.dest[0]).html("<h1>Failed to load page</h1>");
                    //$(state.dest[0]).html("<h1>Failed to load page</h1>"+"<br />"+JSON.stringify(data));
                }
            };
            var makeRequest_1 = function (state) {
                var httpService = new HttpService_1.HttpService();
                httpService.get(state.url, 'pid=' + state.dest[1], function (status, data) {
                    afterGetResponse_1(status, data, state);
                });
            };
            jquery_1.default(document).on('click', 'a[data-dest]', function (e) {
                e.preventDefault();
                console.log("+a");
                var This = jquery_1.default(this);
                var url = This.attr("href");
                var dest = This.attr("data-dest").split(':');
                var title = This.text() + ' | ' + App_1.App.Instance().name();
                var state = { url: url, title: title, dest: dest, };
                makeRequest_1(state);
            });
            window.addEventListener('popstate', function (e) {
                console.log('+popstate');
                console.log(JSON.stringify(e.state));
                if (e.state !== null) {
                    makeRequest_1(e.state);
                }
                else {
                    console.log("no history to load");
                    location.reload();
                    //window.history.go(-1);
                }
            });
        }
    };
    return AppHistory;
}());
exports.AppHistory = AppHistory;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/AppUtils.ts":
/*!*************************************************!*\
  !*** ../static_dirs/desktop/ts/App/AppUtils.ts ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var ObjectUtil = /** @class */ (function () {
    function ObjectUtil() {
    }
    ObjectUtil.type = function (o) {
        return (o) ? Object.prototype.toString.call(o).slice(8, -1) : 'undefined';
    };
    ObjectUtil.isArray = function (o) {
        return this.type(o) === 'Array';
    };
    ObjectUtil.isObject = function (o) {
        return this.type(o) === 'Object';
    };
    ObjectUtil.merge = function (a1, a2) {
        var res = a1;
        for (var k in a2) {
            if (a2.hasOwnProperty(k)) {
                if (typeof a2[k] === 'object') {
                    if (this.isArray(a2[k]))
                        res[k] = [];
                    else if (this.isObject(a2[k]))
                        res[k] = {};
                    res[k] = this.merge(res[k], a2[k]);
                }
                else {
                    res[k] = a2[k];
                }
            }
        }
        return res;
    };
    ObjectUtil.dump = function (obj) {
        var out = '';
        for (var k in obj) {
            out += k + ': ' + obj[k] + '; ';
        }
        console.log(out);
    };
    return ObjectUtil;
}());
exports.ObjectUtil = ObjectUtil;
var AppUtil = /** @class */ (function () {
    function AppUtil() {
    }
    AppUtil.csrfToken = function () {
        var $mt = jquery_1.default('meta[name=csrf-token]');
        var data = {};
        data[$mt.attr("key")] = $mt.attr("content");
        return data;
    };
    AppUtil.csrfField = function () {
        var csrfField = "";
        var token = this.csrfToken();
        for (var key in token) {
            csrfField = '<input type="hidden" name=' + key + ' value=' + token[key] + ' />';
        }
        return csrfField;
    };
    AppUtil.appName = function () {
        if (this._name == '') {
            var $mt = jquery_1.default('meta[name=app-name]');
            this._name = $mt.attr("content") || "/m\\";
        }
        return this._name;
    };
    AppUtil._name = '';
    return AppUtil;
}());
exports.AppUtil = AppUtil;
;
var FormUtil = /** @class */ (function () {
    function FormUtil() {
    }
    FormUtil.setValByName = function ($form, name, val) {
        console.log('+FormUtil::setValByName');
        var viewVal = val;
        var $editNode = $form.find('.ui-input[name=' + name + ']');
        var $viewNode = $form.find('[data-rel=' + name + ']');
        if ($editNode.exists()) {
            viewVal = this.setVal($editNode, val);
            $editNode.attr('data-value', val);
        }
        ($viewNode.exists() && $viewNode.html(viewVal));
    };
    FormUtil.setVal = function ($node, val) {
        console.log("+FormUtil::setVal");
        var retVal = val;
        switch ($node.prop("tagName").toLowerCase()) {
            case 'input':
                var type = $node.prop('type').toLowerCase();
                switch (type) {
                    case 'text':
                    case 'hidden':
                        $node.val(val);
                        break;
                    case 'password':
                        $node.val('');
                        break;
                    case 'radio':
                    case 'checkbox':
                        if (val) {
                            $node.prop('checked', true);
                        }
                        else {
                            $node.removeProp('checked');
                        }
                        retVal = $node.val();
                        break;
                }
                break;
            case 'select':
                retVal = $node.find('[value=' + val + ']').prop('selected', true).text();
                break;
            case 'textarea':
            default:
                $node.html(val);
                break;
        }
        console.log('retVal : ' + retVal);
        return retVal;
    };
    FormUtil.resetVal = function ($form) {
        console.log("+FormUtil::resetVal");
        var This = this;
        $form.find('input[type=text], select, textarea').each(function (index, node) {
            This.setVal(jquery_1.default(node), jquery_1.default(node).attr('data-value'));
        });
    };
    FormUtil.fillByName = function ($form, vals) {
        console.log("+FormUtil::fillByName");
        for (var key in vals) {
            var $node = $form.find('[name=' + key + ']');
            this.setVal($node, vals[key]);
        }
    };
    return FormUtil;
}());
exports.FormUtil = FormUtil;
;
var AppEvent = /** @class */ (function () {
    function AppEvent(name) {
        this._name = "AppEvent";
        this._set = [];
        if (name !== undefined) {
            this._name = name;
        }
    }
    AppEvent.prototype.sub = function (p) {
        console.log('+AppEvent::sub');
        if (this._set.indexOf(p) == -1)
            this._set.push(p);
    };
    AppEvent.prototype.unsub = function (p) {
        console.log('AppEvent::unsub');
        var pos = this._set.indexOf(p);
        if (pos > 1)
            this._set.splice(pos, 1);
    };
    AppEvent.prototype.trigger = function (e, data) {
        console.log('+AppEvent::trigger');
        var ret = true;
        for (var i in this._set) {
            var val = this._set[i](e, data);
            ret = ret && val;
        }
        return ret;
    };
    return AppEvent;
}());
exports.AppEvent = AppEvent;
var AppGeo = /** @class */ (function () {
    function AppGeo() {
    }
    AppGeo.locate = function (OnLocate) {
        console.log("+AppGeo::locate");
        navigator.geolocation.getCurrentPosition(function (pos) {
            var lat = pos.coords.latitude.toFixed(8);
            var lng = pos.coords.longitude.toFixed(8);
            var ts = pos.timestamp;
            var acc = pos.coords.accuracy;
            OnLocate(lat, lng);
        }, function () {
            console.log("Failed to get location");
            OnLocate();
        });
    };
    return AppGeo;
}());
exports.AppGeo = AppGeo;
;
var AppCookie = /** @class */ (function () {
    function AppCookie() {
    }
    AppCookie.get = function (cname) {
        var cv = null;
        if (document.cookie != 'undefined' && document.cookie !== '') {
            var cks = document.cookie.split(';');
            for (var i = 0; i < cks.length; i++) {
                var c = cks[i].trim();
                /* Does this cookie string begin with the name we want? */
                if (c.substring(0, cname.length + 1) === (name + '=')) {
                    cv = decodeURIComponent(c.substring(cname.length + 1));
                    break;
                }
            }
        }
        return cv;
    };
    AppCookie.set = function (cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    };
    AppCookie.has = function (cname) {
        return (this.get(cname) != null);
    };
    return AppCookie;
}());
exports.AppCookie = AppCookie;
;
var AppStorage = /** @class */ (function () {
    function AppStorage() {
    }
    AppStorage.get = function (key) {
        if (typeof (Storage) !== "undefined")
            return localStorage.getItem(key);
        return "";
    };
    AppStorage.set = function (key, val) {
        if (typeof (Storage) !== "undefined")
            localStorage.setItem(key, val);
    };
    return AppStorage;
}());
exports.AppStorage = AppStorage;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/GoogleMap.ts":
/*!**************************************************!*\
  !*** ../static_dirs/desktop/ts/App/GoogleMap.ts ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var UIToast_1 = __webpack_require__(/*! ./UIToast */ "../static_dirs/desktop/ts/App/UIToast.ts");
var url = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCMz94217XzpYaxnQRagzgCwpy4dfBM1Ho&libraries=places&callback=__onGoogleMapLoaded';
var GoogleMapsLoader = /** @class */ (function () {
    function GoogleMapsLoader() {
    }
    GoogleMapsLoader.load = function () {
        // First time 'load' is called?
        if (!GoogleMapsLoader.promise) {
            // Make promise to load
            GoogleMapsLoader.promise = new Promise(function (resolve) {
                // Set callback for when google maps is loaded.
                window['__onGoogleMapLoaded'] = function (ev) {
                    resolve('google maps api loaded');
                };
                var node = document.createElement('script');
                node.src = url;
                node.type = 'text/javascript';
                document.getElementsByTagName('head')[0].appendChild(node);
            });
        }
        // Always return promise. When 'load' is called many times, the promise is already resolved.
        return GoogleMapsLoader.promise;
    };
    return GoogleMapsLoader;
}());
exports.GoogleMapsLoader = GoogleMapsLoader;
var GoogleMap = /** @class */ (function () {
    function GoogleMap(mapBox, config) {
        this._IsInit = false;
        this._Map = null;
        this._Marker = null;
        this._Geocoder = null;
        this._Timeout = null;
        this._LatLong = { lat: 12.964914, lng: 77.596683 };
        this.AddressFoundEvent = new AppUtils_1.AppEvent();
        GoogleMapsLoader.load();
    }
    GoogleMap.prototype.attach = function (mapBox) {
        console.log("+GoogleMap::init");
        var This = this;
        var myLatlng = new google.maps.LatLng(This._LatLong.lat, This._LatLong.lng);
        var mapOpts = {
            zoom: 18,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        This._Map = new google.maps.Map(mapBox, mapOpts);
        This._Marker = new google.maps.Marker({
            position: myLatlng,
            map: This._Map,
            draggable: true,
            title: "Your Location"
        });
        This._Geocoder = new google.maps.Geocoder();
        google.maps.event.addListener(This._Marker, 'dragend', function (e) {
            This.updateLoc(e.latLng.lat(), e.latLng.lng());
        });
        google.maps.event.addListener(This._Map, 'drag', function (e) {
            var center = this.getCenter();
            clearTimeout(This._Timeout);
            This._Timeout = setTimeout(function () {
                This._Marker.setPosition(center);
                This.updateLoc(center.lat(), center.lng());
            }, 50);
        });
        This._IsInit = true;
        AppUtils_1.AppGeo.locate(function (lt, lg) {
            This.updateLoc(lt, lg);
        });
    };
    GoogleMap.prototype.initPlaceSearch = function (input) {
        console.log('+GoogleMap::initPlaceSearch');
        var This = this;
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.addListener('place_changed', function (e) {
            This._Marker.setVisible(false);
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                UIToast_1.UIToast.Instance().show("No details available for : '" + place.name + "'");
                return;
            }
            console.log(place);
            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                This._Map.fitBounds(place.geometry.viewport);
            }
            else {
                This._Map.setCenter(place.geometry.location);
                This._Map.setZoom(17);
            }
            This._Marker.setPosition(place.geometry.location);
            This._Marker.setVisible(true);
            This.AddressFoundEvent.trigger(e, { status: true, address: place });
        });
    };
    GoogleMap.prototype.update = function () {
        if (this._Map) {
            google.maps.event.trigger(this._Map, 'resize');
            if (this._Marker) {
                this._Map.setCenter(this._Marker.getPosition());
            }
        }
    };
    GoogleMap.prototype.updateLoc = function (lat, lng) {
        console.log('[' + lat + ' ### ' + lng + ']');
        if (lat != 0 && lng != 0) {
            var This_1 = this;
            var pos = new google.maps.LatLng(lat, lng);
            This_1._Marker.setPosition(pos);
            This_1._Map.panTo(pos);
            return This_1.getAddress(pos, function (data) {
                This_1.AddressFoundEvent.trigger({}, data);
            });
        }
    };
    GoogleMap.prototype.getAddress = function (loc, OnFound) {
        if (!this._IsInit)
            return;
        this._Geocoder.geocode({
            'location': loc
        }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                console.log(results[0]);
                OnFound({ status: true, 'address': results[0] });
            }
            else {
                console.log('Geocode failed reason: ' + status);
                OnFound({ status: false, address: '' });
            }
        });
    };
    return GoogleMap;
}());
exports.GoogleMap = GoogleMap;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/HttpService.ts":
/*!****************************************************!*\
  !*** ../static_dirs/desktop/ts/App/HttpService.ts ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var UIToast_1 = __webpack_require__(/*! ./UIToast */ "../static_dirs/desktop/ts/App/UIToast.ts");
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var HttpResponseHandler = /** @class */ (function () {
    function HttpResponseHandler(handlers) {
        this.progress_up = function (p) { console.log('default_progress_up'); };
        this.progress_dn = function (p) { console.log('default_progress_dn'); };
        this.complete = function (s, d) { console.log('default_complete'); };
        AppUtils_1.ObjectUtil.merge(this, handlers);
    }
    return HttpResponseHandler;
}());
exports.HttpResponseHandler = HttpResponseHandler;
;
var HttpService = /** @class */ (function () {
    function HttpService() {
        this._handle = null;
    }
    HttpService.prototype.abort = function () {
        if (this._handle) {
            this._handle.abort();
        }
    };
    HttpService.prototype.get = function (url, data, callback) {
        console.log('+get');
        var options = { type: 'GET', 'url': url, 'data': data };
        var handler = new HttpResponseHandler({ complete: callback });
        console.log(handler);
        return this._request(options, handler);
    };
    HttpService.prototype.post = function (url, data, callback) {
        console.log("+post");
        var options = { type: 'POST', 'url': url, 'data': data };
        var handler = new HttpResponseHandler({ complete: callback });
        console.log(handler);
        return this._request(options, handler);
    };
    HttpService.prototype.file = function (url, data, handler) {
        console.log("+file");
        var options = { type: 'POST', 'url': url, 'data': data, processData: false, contentType: false };
        return this._request(options, handler);
    };
    HttpService.prototype.request = function (options, handler) {
        console.log("+request");
        return this._request(options, handler);
    };
    HttpService.prototype._request = function (options, handler) {
        if (handler === void 0) { handler = HttpResponseHandler; }
        var methods = {
            dataType: 'text',
            xhr: function () {
                var xhr = jquery_1.default.ajaxSettings.xhr();
                xhr.upload.onprogress = function (evt) {
                    if (evt.lengthComputable) {
                        var percent = 100 * (evt.loaded / evt.total);
                        handler.progress_up(percent);
                    }
                };
                xhr.onprogress = function (evt) {
                    if (evt.lengthComputable) {
                        var percent = 100 * (evt.loaded / evt.total);
                        handler.progress_dn(percent);
                    }
                };
                return xhr;
            },
            complete: function (res) {
                console.log('+comeplete : ' + res.status);
            },
            success: function (data, status, xhr) {
                console.log('+success');
                var mimeType = xhr.getResponseHeader("content-type");
                console.log('content-type: ' + mimeType);
                if (mimeType.indexOf('json') > -1) {
                    console.log('data : ' + data);
                    var jsonObj = JSON.parse(data);
                    switch (jsonObj.status) {
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
                }
                else if (mimeType.indexOf('html') > -1) {
                    handler.complete(true, data);
                }
                else {
                    console.log('content-type: unknown');
                    handler.complete(false, { 'message': 'Unknown response', 'data': 'unexpected content type' });
                }
            },
            error: function (xhr, error) {
                console.log('+error : ' + xhr.status);
                UIToast_1.UIToast.Instance().show('Network error occured');
                handler.complete(false, { 'message': 'Network failed', 'data': { error: error } });
            }
        };
        jquery_1.default.extend(options, methods);
        this._handle = jquery_1.default.ajax(options);
    };
    return HttpService;
}());
exports.HttpService = HttpService;
;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/UINoti.ts":
/*!***********************************************!*\
  !*** ../static_dirs/desktop/ts/App/UINoti.ts ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var UINoti = /** @class */ (function () {
    function UINoti(config) {
        this.link = window.location.href;
        this.title = 'Alert';
        this.text = 'Notification';
        this.timeout = 5000;
        AppUtils_1.ObjectUtil.merge(this, config);
    }
    UINoti.make = function (config) {
        return new this(config);
    };
    UINoti.prototype.show = function () {
        var This = this;
        var $elm = jquery_1.default('#wt-noti').clone().removeAttr('id');
        $elm.fadeIn({ duration: 1000,
            start: function () {
                $elm.find('.wt-notititle').html(This.title);
                $elm.find('.wt-notibody').html(This.text);
                $elm.find('.wt-notilink').attr('href', This.link);
            }
        }).delay(This.timeout).fadeOut({
            duration: 1000,
            always: function () { $elm.remove(); }
        });
        jquery_1.default('.wt-notibox').append($elm);
    };
    return UINoti;
}());
exports.UINoti = UINoti;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/UIToast.ts":
/*!************************************************!*\
  !*** ../static_dirs/desktop/ts/App/UIToast.ts ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var UIToast = /** @class */ (function () {
    function UIToast() {
    }
    UIToast.Instance = function () {
        return this._instance || (this._instance = new this());
    };
    UIToast.prototype.show = function (text, timeout) {
        if (text === void 0) { text = 'Error'; }
        if (timeout === void 0) { timeout = 1800; }
        jquery_1.default('.wt-toast').fadeIn({
            duration: 500,
            start: function () { jquery_1.default(this).text(text); },
        }).delay(timeout).fadeOut(500);
    };
    UIToast.prototype.hide = function () {
        jquery_1.default('.wt-toast').hide();
    };
    UIToast._instance = null;
    return UIToast;
}());
exports.UIToast = UIToast;


/***/ }),

/***/ "../static_dirs/desktop/ts/App/UIWidgets.ts":
/*!**************************************************!*\
  !*** ../static_dirs/desktop/ts/App/UIWidgets.ts ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var AppUtils_1 = __webpack_require__(/*! ./AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
var HttpService_1 = __webpack_require__(/*! ./HttpService */ "../static_dirs/desktop/ts/App/HttpService.ts");
var KEYS = {
    BACK: 8,
    TAB: 9,
    ENTER: 13,
    ESCAPE: 27,
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40,
    DELETE: 46,
};
var UIOverlay = /** @class */ (function () {
    function UIOverlay() {
        this.$overlay = null;
        this.$closebtn = null;
        this.$body = null;
        this.$html = null;
        this.$html_def = null;
        this._shown = false;
        this._options_def = { closeBtn: true, closeOnEscape: true, closeOnClickOutside: true, onClose: function () { } };
        this._options = null;
        this.$overlay = jquery_1.default('#wt-overlay');
        this.$closebtn = this.$overlay.find('.wt-closebtn');
        this.$body = this.$overlay.find('.wt-overlay-body');
        this.$html_def = jquery_1.default('<div style="width:80%; height:inherit; margin: 0 auto; background:#fff;" data-type="none"></div>');
        this.$html = this.$html_def;
        this.$closebtn.on('click', this, this._onclose);
        this.$overlay.on('click', this, this._onclick);
        this.$overlay.on('keyup', this, this._onKeyUp);
        this._shown = false;
        this._options = AppUtils_1.ObjectUtil.merge(this._options_def, {});
    }
    UIOverlay.Instance = function () {
        return this._instance || (this._instance = new this());
    };
    UIOverlay.prototype._apply_options = function (options) {
        this._options = AppUtils_1.ObjectUtil.merge(this._options_def, options);
        if (this._options['closeBtn'] === false)
            this.$closebtn.hide();
        else
            this.$closebtn.show();
    };
    UIOverlay.prototype.shown = function () {
        return this._shown;
    };
    UIOverlay.prototype.show = function ($html, options) {
        if ($html === void 0) { $html = this.$html_def; }
        if (options === void 0) { options = {}; }
        this._apply_options(options);
        /* ordering matter for correct heights */
        this.$overlay.show();
        this.update($html);
        this.$overlay.focus();
        this._shown = true;
        jquery_1.default('body').toggleClass('ui-noscroll', this._shown);
        return this;
    };
    UIOverlay.prototype.hide = function () {
        this.$overlay.hide();
        this._shown = false;
        jquery_1.default('body').toggleClass('ui-noscroll', this._shown);
        return this;
    };
    UIOverlay.prototype.update = function ($html) {
        this.$html = jquery_1.default($html);
        this.$body.html(this.$html.show());
        var $scroll = this.$html.find(".wt-overlay-scroll");
        if ($scroll.exists()) {
            var h1 = this.$body.height();
            var h2 = this.$html.height();
            var h3 = $scroll.height();
            if (h1 < h2) {
                var h4 = h3 - (h2 - h1);
                console.log("h4 : " + h4);
                $scroll.height(h4);
            }
        }
        return this;
    };
    UIOverlay.prototype.clear = function () {
        this.update(this.$html_def);
        return this;
    };
    UIOverlay.prototype.close = function () {
        console.log("CLOSE OVERLAY");
        this.$closebtn.click();
    };
    UIOverlay.prototype._close = function (e) {
        var $html = this.$html.hide();
        if ($html.attr('data-type') == 'persist') {
            setTimeout(function () { $html.appendTo('body'); }, 100);
        }
        else {
            $html.remove();
        }
        this.hide();
    };
    UIOverlay.prototype._onclose = function (e) {
        console.log("ONCLOSE OVERLAY");
        e.data._close(e);
    };
    UIOverlay.prototype._onclick = function (e) {
        console.log("ONCLICK OVERLAY");
        var This = e.data;
        if (This._options["closeOnClickOutside"] === true && jquery_1.default(e.target).parent().is(This.$overlay)) {
            This._close(e);
        }
    };
    UIOverlay.prototype._onKeyUp = function (e) {
        console.log("ONKEYUP OVERLAY");
        var This = e.data;
        if (This._options["closeOnEscape"] === true && e.keyCode == KEYS.ESCAPE) {
            This._close(e);
        }
    };
    UIOverlay._instance = null;
    return UIOverlay;
}());
exports.UIOverlay = UIOverlay;
/* App Modal */
var UIModal = /** @class */ (function () {
    function UIModal() {
    }
    UIModal.prototype.show = function ($html, options) {
        UIOverlay.Instance().show($html, { closeOnClickOutside: true, onClose: this.onClose });
        return this;
    };
    UIModal.prototype.update = function ($html) {
        UIOverlay.Instance().update($html);
        return this;
    };
    UIModal.prototype.hide = function () {
        UIOverlay.Instance().hide();
        return this;
    };
    UIModal.prototype.close = function () {
        UIOverlay.Instance().close();
        return this;
    };
    UIModal.prototype.onClose = function (e) {
    };
    return UIModal;
}());
exports.UIModal = UIModal;
;
var UIDialog = /** @class */ (function () {
    function UIDialog() {
    }
    UIDialog.prototype.show = function ($html) {
        UIOverlay.Instance().show($html);
    };
    UIDialog.prototype.hide = function () {
        UIOverlay.Instance().hide();
    };
    UIDialog.prototype.close = function () {
        UIOverlay.Instance().close();
    };
    return UIDialog;
}());
exports.UIDialog = UIDialog;
;
var UIOptionList = /** @class */ (function () {
    function UIOptionList($Inst, overrides, config) {
        this._name = 'UIOptionList';
        this._count = 0;
        this._selectedIndex = 0;
        this._jsonItemsList = null;
        this._config = { minLength: 1, delay: 0 };
        this._overrides = { 'source': function (key, respCB) { console.log('implement source'); },
            'itemCreate': function (item) { console.log('implement itemCreate'); },
            'onItemSelect': function ($input, item) { console.log('implement onItemSelect'); },
            'onEnter': function ($input, item) { console.log('implement onEnter'); },
        };
        this._scrollTimer = null;
        this.$_self = null;
        this.$_list = null;
        this.$_selectedItem = null;
        console.log('+UIOptionList : ' + $Inst.prop("tagName"));
        this.$_self = $Inst;
        $Inst.optionsList = this;
        /* merge the options */
        AppUtils_1.ObjectUtil.merge(this._config, config);
        AppUtils_1.ObjectUtil.merge(this._overrides, overrides);
        this._create();
    }
    UIOptionList.prototype.source = function (key, respCB) {
        if (this._overrides.source)
            this._overrides.source(key, respCB);
    };
    UIOptionList.prototype.itemCreate = function (item) {
        if (this._overrides.itemCreate)
            return this._overrides.itemCreate(item);
        return '';
    };
    UIOptionList.prototype.onItemSelect = function ($input, item) {
        if (this._overrides.onItemSelect)
            this._overrides.onItemSelect($input, item);
    };
    UIOptionList.prototype.onEnter = function ($input, item) {
        if (this._overrides.onEnter)
            this._overrides.onEnter($input, item);
    };
    /* private methods */
    UIOptionList.prototype._create = function () {
        var This = this;
        console.log('+_create[' + This._name + ']');
        This.$_list = jquery_1.default('<ul class="wt-search-list wt-search-list-app" >');
        This.$_list.css({ width: This.$_self.css('width') });
        This.$_list.on('mouseenter', 'li', This._onItemHover.bind(This));
        This.$_list.on('click', 'li', This._onItemClick.bind(This));
        This.$_list.on('scroll', This._onListScroll.bind(This));
        This.$_self.on("keyup", This._onKeyUp.bind(This));
        This.$_self.on("keypress", This._onKeyPress.bind(This));
        This.$_self.on("focus", This._onFocus.bind(This));
        This.$_self.on("blur", This._onUnfocus.bind(This));
        This.$_self.on('DOMNodeRemoved', This._destroy.bind(This));
        This.$_self.after(This.$_list);
    };
    UIOptionList.prototype._destroy = function (e) {
        this.$_list.remove();
    };
    UIOptionList.prototype._onFocus = function (e) {
        console.log('+_onFocus');
        this.$_list.show();
    };
    UIOptionList.prototype._onUnfocus = function (e) {
        this.$_list.hide();
    };
    UIOptionList.prototype._onData = function (jsonItemsList) {
        console.log('+_onData');
        var This = this;
        This.$_list.html('');
        This._jsonItemsList = jsonItemsList;
        This._count = jsonItemsList.length;
        This._selectedIndex = 0;
        if (This._count > 0) {
            for (var i in jsonItemsList) {
                This.$_list.append(This.itemCreate(jsonItemsList[i]));
            }
            This.$_selectedItem = This.$_list.children().eq(This._selectedIndex);
            This.$_selectedItem.addClass('wt-search-item-a');
        }
        else {
            This.$_list.html('<div class="wt-search-item">No search results</div>');
        }
        This.$_list.show();
    };
    UIOptionList.prototype._setItemSelected = function (newIndex) {
        var This = this;
        var oldIndex = This._selectedIndex;
        console.log('oldIndex : ' + oldIndex + ' newIndex : ' + newIndex);
        if (newIndex >= 0 && newIndex < This._count) {
            if (oldIndex != newIndex) {
                var $children = This.$_list.children();
                $children.eq(oldIndex).removeClass('wt-search-item-a');
                This.$_selectedItem = $children.eq(newIndex).addClass('wt-search-item-a');
                This._selectedIndex = newIndex;
                This._notifyItemSelected();
            }
            var itemTop = This.$_selectedItem.position().top;
            var itemHeight = This.$_selectedItem.outerHeight();
            var bodyScroll = This.$_list.scrollTop();
            var bodyHeight = This.$_list.outerHeight();
            console.log('itemTop : ' + itemTop + ' itemHeight : ' + itemHeight);
            console.log('bodyScroll : ' + bodyScroll + ' bodyHeight : ' + bodyHeight);
            if (itemTop < 0) {
                console.log('scrollup');
                This.$_list.scrollTop(bodyScroll + itemTop);
            }
            else if (itemTop + itemHeight > bodyHeight) {
                console.log('scrolldown');
                This.$_list.scrollTop(bodyScroll + itemHeight - (bodyHeight - itemTop));
            }
            This.$_list.show();
        }
    };
    UIOptionList.prototype._onListScroll = function (e) {
        var This = this;
        This._scrollTimer = setTimeout(function () {
            This._scrollTimer = null;
        }, 300);
    };
    UIOptionList.prototype._onItemHover = function (e) {
        var This = this;
        console.log('+_onItemHover');
        if (!This._scrollTimer) {
            This._setItemSelected(jquery_1.default(e.target).index());
        }
    };
    UIOptionList.prototype._onItemClick = function (e) {
        console.log('+_onItemClick');
        this._setItemSelected(jquery_1.default(e.target).index());
    };
    UIOptionList.prototype._notifyItemSelected = function () {
        if (this._count > 0 && this._jsonItemsList) {
            this.onItemSelect(this.$_self, this._jsonItemsList[this._selectedIndex]);
        }
    };
    UIOptionList.prototype._onKeyPress = function (e) {
        console.log('+_onKeyPress : ' + e.keyCode);
        if (e.keyCode === KEYS.ENTER) {
            e.preventDefault();
            var item = (this._count > 0 && this._jsonItemsList) ? this._jsonItemsList[this._selectedIndex] : null;
            this.onEnter(this.$_self, item);
            this._onUnfocus(e);
        }
    };
    UIOptionList.prototype._onKeyUp = function (e) {
        console.log('+_onKeyUp');
        var This = this;
        var handled = true;
        switch (e.keyCode) {
            case KEYS.UP:
                This._setItemSelected(This._selectedIndex - 1);
                break;
            case KEYS.DOWN:
                This._setItemSelected(This._selectedIndex + 1);
                break;
            case KEYS.ENTER:
                break;
            case KEYS.LEFT:
            case KEYS.RIGHT:
                This._onFocus({});
                break;
            default:
                console.log('keycode : ' + e.keyCode);
                handled = false;
        }
        if (handled) {
            e.preventDefault();
            return;
        }
        var key = This.$_self.val();
        (key.length >= This._config.minLength && This.source(key, This._onData.bind(This)));
    };
    return UIOptionList;
}());
exports.UIOptionList = UIOptionList;
;
var UIProgressBar = /** @class */ (function () {
    function UIProgressBar(title, btnText) {
        this.$_ui = null;
        this.$_ui = "<div class=\"wt-progress-outer\" >\n                    <div class=\"wt-progress-inner\">\n                    <div class=\"wt-progress-filename\">" + title + "</div>\n                    <div class=\"wt-progress-bar\">&nbsp;0%</div></div>\n                    <div class=\"wt-progress-control\">\n                    <button class=\"ui-btn\">" + btnText + "</button>\n                    </div></div>";
    }
    UIProgressBar.prototype.show = function ($parent) {
        $parent.append(this.$_ui);
        this.$_ui.show();
    };
    return UIProgressBar;
}());
exports.UIProgressBar = UIProgressBar;
;
var UIFileUpload = /** @class */ (function () {
    function UIFileUpload($Inst, overrides, config) {
        this._name = 'UIFileUpload';
        this._uploads = [];
        this.$_hidden = null;
        this.$_ui = null;
        this.$_self = null;
        this._overrides = {};
        this._config = { maxFiles: 1, mimeType: 'image', maxSize: 1024, };
        console.log('+UIFileUpload : ' + $Inst.prop('tagName'));
        AppUtils_1.ObjectUtil.merge(this._overrides, overrides);
        AppUtils_1.ObjectUtil.merge(this._config, config);
        this.$_self = $Inst;
        this._create();
    }
    UIFileUpload.prototype._create = function () {
        var This = this;
        console.log('+_create[' + This._name + ']');
        This.$_ui = jquery_1.default('<div class="wt-progress-div" ></div>');
        This.$_ui.css({ width: This.$_self.css('width') });
        This.$_hidden = jquery_1.default('<input type="hidden" name="files" value="" >');
        This.$_self.before(This.$_hidden);
        This.$_self.after(This.$_ui);
        This.$_self.on('change', This._upload.bind(This));
        This.$_self.on('DOMNodeRemoved', This._destroy.bind(This));
    };
    UIFileUpload.prototype._destroy = function (e) {
        console.log('+_destroy[' + this._name + ']');
        this.$_ui.remove();
        this.$_hidden.remove();
    };
    UIFileUpload.prototype._upload = function (e) {
        console.log('+_upload');
        e.stopPropagation();
        e.preventDefault();
        var This = this;
        var FileField = e.target;
        var Files = jquery_1.default(FileField)[0].files;
        var count = This.$_ui.find('.wt-progress-outer').length;
        console.log('count : ' + count);
        var rem = This._config.maxFiles - count;
        if (rem == 0) {
            FileField.value = '';
            console.log('Already attached to max limit');
            return;
        }
        if (rem > Files.length) {
            rem = Files.length;
        }
        for (var i = 0; i < rem; ++i) {
            console.log('name : ' + Files[i].name + ' data : ' + Files[i]);
            This._uploadFile(Files[i]);
        }
    };
    UIFileUpload.prototype._uploadFile = function (file) {
        console.log('+_uploadFile');
        var This = this;
        var formData = new FormData();
        var fileName = file.name;
        var csrf = AppUtils_1.AppUtil.csrfToken();
        for (var key in csrf) {
            formData.append(key, csrf[key]);
        }
        formData.append('image', file);
        //(fileName.length > 20 && (fileName = fileName.substring(0, 20)));
        var $item = jquery_1.default("<div class=\"wt-progress-outer\" >'\n                        <div class=\"wt-progress-inner\">'\n                        <div class=\"wt-progress-filename\">" + fileName + "</div>'\n                        <div class=\"wt-progress-bar\">&nbsp;0%</div></div>'\n                        <div class=\"wt-progress-control\">'\n                        <button class=\"ui-btn\">Cancel</button>'\n                        </div></div>");
        var $cancelBtn = $item.find('.ui-btn');
        $cancelBtn.on('click', This._cancel.bind(This));
        This.$_ui.append($item);
        var callbacks = {
            progress_up: function (percent) {
                This._progress(percent);
            },
            complete: function (status, jsonObj) {
                if (status) {
                    console.log("upload finished");
                    var upload_ids = jsonObj.data.upload_ids;
                    This._uploads.push(upload_ids);
                    This.$_hidden.val(This._uploads.toString());
                    $cancelBtn.data('request', null);
                    $cancelBtn.data('upload_ids', upload_ids);
                    $cancelBtn.text('Remove');
                    console.log('ids : ' + This._uploads.toString());
                }
                else {
                    console.log('file upload failed reason : ' + JSON.stringify(jsonObj));
                    $cancelBtn.remove();
                }
            }
        };
        var handler = new HttpService_1.HttpResponseHandler(callbacks);
        var http = new HttpService_1.HttpService();
        http.file('/upload/file/', formData, handler);
        $cancelBtn.data('request', http);
    };
    UIFileUpload.prototype._cancel = function (e) {
        console.log('+_cancel');
        e.preventDefault();
        var This = this;
        var $item = jquery_1.default(e.target);
        console.log($item.text());
        if ($item.text() == 'Cancel') {
            var http = $item.data('request');
            http.abort();
            console.log('aborted');
        }
        else {
            var id = $item.data('upload_id');
            var index = This._uploads.indexOf(id);
            This._uploads.splice(index, 1);
            This.$_hidden.val(This._uploads);
            console.log('ids : ' + This._uploads.toString());
        }
        $item.parents('.wt-progress-outer').remove();
    };
    UIFileUpload.prototype._progress = function (progress) {
        console.log('progress : ' + progress + '%');
        var $pgbar = this.$_ui.find('.wt-progress-bar');
        $pgbar.css({ width: progress + '%' });
        $pgbar.html(progress + '%');
    };
    return UIFileUpload;
}());
exports.UIFileUpload = UIFileUpload;
var UITabs = /** @class */ (function () {
    function UITabs($Inst, overrides) {
        this._name = 'UITabs';
        this._total = 2;
        this._active = null;
        this._activeIndex = 0;
        this._overrides = { 'beforeLoad': function (num) { console.log("implement beforeLoad()"); },
            'afterLoad': function (num) { console.log("implement afterLoad()"); },
            'source': function (num) { console.log("implement source()"); }
        };
        this.$_self = null;
        console.log('+UITabs : ' + $Inst.prop('tagName'));
        this.$_self = $Inst;
        this._create();
    }
    UITabs.prototype._create = function () {
        var This = this;
        console.log('+_create[' + This._name + ']');
        var $elems = This.$_self.find(".wt-switchtab-nav > li > a[rel]");
        This._total = $elems.length;
        console.log("Tabs : " + This._total);
        This._active = $elems.eq(This._activeIndex);
        var rel = This._active.prop("rel");
        This.$_self.find(rel).show();
        $elems.on("click", function (e) {
            console.log("+tabClicked");
            e.preventDefault();
            var rel = This._active.prop("rel");
            This._active.removeClass("wt-switchtab-a");
            This.$_self.find(rel).hide();
            This._active = jquery_1.default(this);
            rel = This._active.prop("rel");
            This._active.prop("class", "wt-switchtab-a");
            This.$_self.find(rel).show();
        });
    };
    return UITabs;
}());
exports.UITabs = UITabs;
;


/***/ }),

/***/ "../static_dirs/desktop/ts/index.ts":
/*!******************************************!*\
  !*** ../static_dirs/desktop/ts/index.ts ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
//import * as $ from '../../libs/jquery/jquery-3.3.1.min';
//import * as $ from 'jquery'; // esModuleInterop:false in tsconfig.json
var jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "jquery"));
var App_1 = __webpack_require__(/*! ./App/App */ "../static_dirs/desktop/ts/App/App.ts");
var UIWidgets_1 = __webpack_require__(/*! ./App/UIWidgets */ "../static_dirs/desktop/ts/App/UIWidgets.ts");
var UIWidgets_2 = __webpack_require__(/*! ./App/UIWidgets */ "../static_dirs/desktop/ts/App/UIWidgets.ts");
exports.UIOverlay = UIWidgets_2.UIOverlay;
exports.UIModal = UIWidgets_2.UIModal;
exports.UIDialog = UIWidgets_2.UIDialog;
var AppForm_1 = __webpack_require__(/*! ./App/AppForm */ "../static_dirs/desktop/ts/App/AppForm.ts");
exports.AjaxForm = AppForm_1.AjaxForm;
exports.AppFormHandler = AppForm_1.AppFormHandler;
var UINoti_1 = __webpack_require__(/*! ./App/UINoti */ "../static_dirs/desktop/ts/App/UINoti.ts");
exports.UINoti = UINoti_1.UINoti;
var UIToast_1 = __webpack_require__(/*! ./App/UIToast */ "../static_dirs/desktop/ts/App/UIToast.ts");
exports.UIToast = UIToast_1.UIToast;
var HttpService_1 = __webpack_require__(/*! ./App/HttpService */ "../static_dirs/desktop/ts/App/HttpService.ts");
exports.HttpResponseHandler = HttpService_1.HttpResponseHandler;
exports.HttpService = HttpService_1.HttpService;
var GoogleMap_1 = __webpack_require__(/*! ./App/GoogleMap */ "../static_dirs/desktop/ts/App/GoogleMap.ts");
exports.GoogleMap = GoogleMap_1.GoogleMap;
var AppUtils_1 = __webpack_require__(/*! ./App/AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
exports.ObjectUtil = AppUtils_1.ObjectUtil;
exports.AppUtil = AppUtils_1.AppUtil;
exports.FormUtil = AppUtils_1.FormUtil;
var AppUtils_2 = __webpack_require__(/*! ./App/AppUtils */ "../static_dirs/desktop/ts/App/AppUtils.ts");
exports.AppEvent = AppUtils_2.AppEvent;
exports.AppGeo = AppUtils_2.AppGeo;
exports.AppCookie = AppUtils_2.AppCookie;
exports.AppStorage = AppUtils_2.AppStorage;
function initPlugins() {
    jquery_1.default.fn.extend({
        exists: function () { return this.length > 0; },
        OptionList: function (overrides, config) { new UIWidgets_1.UIOptionList(this, overrides, config); },
        Tabs: function (overrides, config) { new UIWidgets_1.UITabs(this, overrides); },
        FileUpload: function (overrides, config) { new UIWidgets_1.UIFileUpload(this, overrides, config); },
    });
}
jquery_1.default(function () {
    initPlugins();
    var app = App_1.App.Instance();
    app.show();
});


/***/ }),

/***/ "jquery":
/*!*************************!*\
  !*** external "jQuery" ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = jQuery;

/***/ })

/******/ });
//# sourceMappingURL=index.js.map