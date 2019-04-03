(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const AppHistory_1 = require("./AppHistory");
class AppFw {
    constructor() {
        this._history = new AppHistory_1.AppHistory();
        this.init();
    }
    init() {
        console.log("+AppFw::init");
    }
}
exports.AppFw = AppFw;

},{"./AppHistory":2}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class AppHistory {
    constructor() {
        console.log("+AppHistory");
    }
}
exports.AppHistory = AppHistory;

},{}],3:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const AppFw_1 = require("./AppFw");
let app = new AppFw_1.AppFw();

},{"./AppFw":1}]},{},[3])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCIuLi9kZXNrdG9wL3RzL0FwcEZ3LnRzIiwiLi4vZGVza3RvcC90cy9BcHBIaXN0b3J5LnRzIiwiLi4vZGVza3RvcC90cy9BcHBNYWluLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7QUNBQSw2Q0FBd0M7QUFHeEMsTUFBYSxLQUFLO0lBR2pCO1FBRUMsSUFBSSxDQUFDLFFBQVEsR0FBRyxJQUFJLHVCQUFVLEVBQUUsQ0FBQztRQUNqQyxJQUFJLENBQUMsSUFBSSxFQUFFLENBQUM7SUFDYixDQUFDO0lBRUQsSUFBSTtRQUVILE9BQU8sQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDN0IsQ0FBQztDQUNEO0FBYkQsc0JBYUM7Ozs7O0FDZkQsTUFBYSxVQUFVO0lBQ3RCO1FBRUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxhQUFhLENBQUMsQ0FBQztJQUM1QixDQUFDO0NBRUQ7QUFORCxnQ0FNQzs7Ozs7QUNQRCxtQ0FBOEI7QUFFOUIsSUFBSSxHQUFHLEdBQUcsSUFBSSxhQUFLLEVBQUUsQ0FBQyIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uKCl7ZnVuY3Rpb24gcihlLG4sdCl7ZnVuY3Rpb24gbyhpLGYpe2lmKCFuW2ldKXtpZighZVtpXSl7dmFyIGM9XCJmdW5jdGlvblwiPT10eXBlb2YgcmVxdWlyZSYmcmVxdWlyZTtpZighZiYmYylyZXR1cm4gYyhpLCEwKTtpZih1KXJldHVybiB1KGksITApO3ZhciBhPW5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIraStcIidcIik7dGhyb3cgYS5jb2RlPVwiTU9EVUxFX05PVF9GT1VORFwiLGF9dmFyIHA9bltpXT17ZXhwb3J0czp7fX07ZVtpXVswXS5jYWxsKHAuZXhwb3J0cyxmdW5jdGlvbihyKXt2YXIgbj1lW2ldWzFdW3JdO3JldHVybiBvKG58fHIpfSxwLHAuZXhwb3J0cyxyLGUsbix0KX1yZXR1cm4gbltpXS5leHBvcnRzfWZvcih2YXIgdT1cImZ1bmN0aW9uXCI9PXR5cGVvZiByZXF1aXJlJiZyZXF1aXJlLGk9MDtpPHQubGVuZ3RoO2krKylvKHRbaV0pO3JldHVybiBvfXJldHVybiByfSkoKSIsImltcG9ydCB7QXBwSGlzdG9yeX0gZnJvbSAnLi9BcHBIaXN0b3J5JztcblxuXG5leHBvcnQgY2xhc3MgQXBwRncge1xuXHRcblx0X2hpc3Rvcnk6IEFwcEhpc3Rvcnk7XG5cdGNvbnN0cnVjdG9yKClcblx0e1xuXHRcdHRoaXMuX2hpc3RvcnkgPSBuZXcgQXBwSGlzdG9yeSgpO1xuXHRcdHRoaXMuaW5pdCgpO1xuXHR9XG5cdFxuXHRpbml0KClcblx0e1xuXHRcdGNvbnNvbGUubG9nKFwiK0FwcEZ3Ojppbml0XCIpO1xuXHR9XG59XG4iLCJcbmV4cG9ydCBjbGFzcyBBcHBIaXN0b3J5IHtcblx0Y29uc3RydWN0b3IoKVxuXHR7XG5cdFx0Y29uc29sZS5sb2coXCIrQXBwSGlzdG9yeVwiKTtcblx0fVxuXG59XG4iLCJpbXBvcnQge0FwcEZ3fSBmcm9tICcuL0FwcEZ3JztcblxubGV0IGFwcCA9IG5ldyBBcHBGdygpO1xuIl19
