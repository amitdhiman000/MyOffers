(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var AppHistory_1 = require("./AppHistory");
var AppFw = /** @class */ (function () {
    function AppFw() {
        this._history = new AppHistory_1.AppHistory();
        this.init();
    }
    AppFw.prototype.init = function () {
        console.log("+AppFw::init");
    };
    return AppFw;
}());
exports.AppFw = AppFw;

},{"./AppHistory":2}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var AppHistory = /** @class */ (function () {
    function AppHistory() {
        console.log("+AppHistory");
    }
    return AppHistory;
}());
exports.AppHistory = AppHistory;

},{}],3:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var AppFw_1 = require("./AppFw");
var app = new AppFw_1.AppFw();

},{"./AppFw":1}]},{},[3])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCIuLi9kZXNrdG9wL3RzL0FwcEZ3LnRzIiwiLi4vZGVza3RvcC90cy9BcHBIaXN0b3J5LnRzIiwiLi4vZGVza3RvcC90cy9BcHBNYWluLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7QUNBQSwyQ0FBd0M7QUFHeEM7SUFHQztRQUVDLElBQUksQ0FBQyxRQUFRLEdBQUcsSUFBSSx1QkFBVSxFQUFFLENBQUM7UUFDakMsSUFBSSxDQUFDLElBQUksRUFBRSxDQUFDO0lBQ2IsQ0FBQztJQUVELG9CQUFJLEdBQUo7UUFFQyxPQUFPLENBQUMsR0FBRyxDQUFDLGNBQWMsQ0FBQyxDQUFDO0lBQzdCLENBQUM7SUFDRixZQUFDO0FBQUQsQ0FiQSxBQWFDLElBQUE7QUFiWSxzQkFBSzs7Ozs7QUNGbEI7SUFDQztRQUVDLE9BQU8sQ0FBQyxHQUFHLENBQUMsYUFBYSxDQUFDLENBQUM7SUFDNUIsQ0FBQztJQUVGLGlCQUFDO0FBQUQsQ0FOQSxBQU1DLElBQUE7QUFOWSxnQ0FBVTs7Ozs7QUNEdkIsaUNBQThCO0FBRTlCLElBQUksR0FBRyxHQUFHLElBQUksYUFBSyxFQUFFLENBQUMiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbigpe2Z1bmN0aW9uIHIoZSxuLHQpe2Z1bmN0aW9uIG8oaSxmKXtpZighbltpXSl7aWYoIWVbaV0pe3ZhciBjPVwiZnVuY3Rpb25cIj09dHlwZW9mIHJlcXVpcmUmJnJlcXVpcmU7aWYoIWYmJmMpcmV0dXJuIGMoaSwhMCk7aWYodSlyZXR1cm4gdShpLCEwKTt2YXIgYT1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK2krXCInXCIpO3Rocm93IGEuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixhfXZhciBwPW5baV09e2V4cG9ydHM6e319O2VbaV1bMF0uY2FsbChwLmV4cG9ydHMsZnVuY3Rpb24ocil7dmFyIG49ZVtpXVsxXVtyXTtyZXR1cm4gbyhufHxyKX0scCxwLmV4cG9ydHMscixlLG4sdCl9cmV0dXJuIG5baV0uZXhwb3J0c31mb3IodmFyIHU9XCJmdW5jdGlvblwiPT10eXBlb2YgcmVxdWlyZSYmcmVxdWlyZSxpPTA7aTx0Lmxlbmd0aDtpKyspbyh0W2ldKTtyZXR1cm4gb31yZXR1cm4gcn0pKCkiLCJpbXBvcnQge0FwcEhpc3Rvcnl9IGZyb20gJy4vQXBwSGlzdG9yeSc7XG5cblxuZXhwb3J0IGNsYXNzIEFwcEZ3IHtcblx0XG5cdF9oaXN0b3J5OiBBcHBIaXN0b3J5O1xuXHRjb25zdHJ1Y3RvcigpXG5cdHtcblx0XHR0aGlzLl9oaXN0b3J5ID0gbmV3IEFwcEhpc3RvcnkoKTtcblx0XHR0aGlzLmluaXQoKTtcblx0fVxuXHRcblx0aW5pdCgpXG5cdHtcblx0XHRjb25zb2xlLmxvZyhcIitBcHBGdzo6aW5pdFwiKTtcblx0fVxufVxuIiwiXG5leHBvcnQgY2xhc3MgQXBwSGlzdG9yeSB7XG5cdGNvbnN0cnVjdG9yKClcblx0e1xuXHRcdGNvbnNvbGUubG9nKFwiK0FwcEhpc3RvcnlcIik7XG5cdH1cblxufVxuIiwiaW1wb3J0IHtBcHBGd30gZnJvbSAnLi9BcHBGdyc7XG5cbmxldCBhcHAgPSBuZXcgQXBwRncoKTtcbiJdfQ==
