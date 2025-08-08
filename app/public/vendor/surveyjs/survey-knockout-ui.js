/*!
 * surveyjs - Survey JavaScript library v1.12.47
 * Copyright (c) 2015-2025 Devsoft Baltic OÜ  - http://surveyjs.io/
 * License: MIT (http://www.opensource.org/licenses/mit-license.php)
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("knockout"), require("survey-core"));
	else if(typeof define === 'function' && define.amd)
		define("survey-knockout-ui", ["knockout", "survey-core"], factory);
	else if(typeof exports === 'object')
		exports["survey-knockout-ui"] = factory(require("knockout"), require("survey-core"));
	else
		root["SurveyKnockout"] = factory(root["ko"], root["Survey"]);
})(this, function(__WEBPACK_EXTERNAL_MODULE_knockout__, __WEBPACK_EXTERNAL_MODULE_survey_core__) {
return /******/ (function(modules) { // webpackBootstrap
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/entries/knockout-ui.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/panel/panel.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/components/panel/panel.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko template: { name: 'survey-panel', data: question, as: 'question', afterRender: question.koPanelAfterRender } --><!-- /ko -->";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/popup/popup.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/components/popup/popup.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div>\n  <!-- ko with: popupViewModel -->\n  <div class=\"sv-popup\" tabindex=\"-1\"\n    data-bind=\"visible: isVisible, click: function(data, event) { clickOutside(event); return true; }, class: styleClass, event: { keydown: function(data, event) { onKeyDown(event); return true; } }\">\n    <div class=\"sv-popup__container\"\n      data-bind=\"style: { left: left, top: top, height: height, minWidth: minWidth, width: width }, click: function() { return true; }, clickBubble: false\">\n      <!-- ko if: $data.showHeader -->\n      <!-- ko template: { name: $data.popupHeaderTemplate, data: $data } -->\n      <!-- /ko -->\n      <!-- /ko -->\n      <div class=\"sv-popup__body-content\">\n        <!-- ko if: !!title  -->\n        <div class=\"sv-popup__body-header\" data-bind=\"text: title\"></div>\n        <!-- /ko -->\n        <div class=\"sv-popup__scrolling-content\">\n          <div class=\"sv-popup__content\"\n            data-bind=\"component: { name: contentComponentName, params: contentComponentData }\"></div>\n        </div>\n        <!-- ko if: showFooter  -->\n        <div class=\"sv-popup__body-footer\">\n          <!-- ko component: { name: \"sv-action-bar\", params: { model: $data.footerToolbar } } -->\n          <!-- /ko -->\n        </div>\n        <!-- /ko -->\n      </div>\n    </div>\n  </div>\n  <!-- /ko -->\n</div>\n";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/buttons.html":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/components/progress/buttons.html ***!
  \************************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: model.getRootCss(container), style: { maxWidth: model.progressWidth }\" role=\"progressbar\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-label=\"progress\">\n    <!-- ko if: canShowHeader -->\n    <div data-bind=\"css: survey.css.progressButtonsHeader\">\n        <div data-bind=\"css: survey.css.progressButtonsPageTitle, text: model.headerText, attr: { title: model.headerText }\"></div>\n    </div>\n    <!-- /ko -->\n    <div data-bind=\"css: survey.css.progressButtonsContainer\">\n        <div data-bind=\"css: getScrollButtonCss(true), click: clickScrollButton.bind($data, $element.nextElementSibling, true)\" role=\"button\"></div>\n        <div data-bind=\"css: survey.css.progressButtonsListContainer\">\n            <ul data-bind=\"foreach: survey.visiblePages, css: survey.css.progressButtonsList\">\n                <li data-bind=\"css: $parent.model.getListElementCss($index()), click: $parent.model.isListElementClickable($index()) ? $parent.model.clickListElement : null, attr: { 'data-page-number' : $parent.model.getItemNumber($data) }\">\n                    <div data-bind=\"css: css.progressButtonsConnector\"></div>\n                    <!-- ko if: $parent.canShowItemTitles -->\n                    <div data-bind=\"css: css.progressButtonsPageTitle, attr: { title: renderedNavigationTitle }\"><!-- ko template: { name: 'survey-string', data: locNavigationTitle } --><!-- /ko --></div>\n                    <div data-bind=\"css: css.progressButtonsPageDescription, text: locNavigationDescription.koRenderedHtml(), attr: { title: locNavigationDescription.koRenderedHtml() }\"></div>\n                    <!-- /ko -->\n                    <div data-bind=\"css: css.progressButtonsButton\"><div data-bind=\"css: css.progressButtonsButtonBackground\"></div><div data-bind=\"css: css.progressButtonsButtonContent\"></div><span data-bind=\"text: $parent.model.getItemNumber($data)\"></span></div>\n                </li>\n            </ul>\n        </div>\n        <div data-bind=\"css: getScrollButtonCss(false), click: clickScrollButton.bind($data, $element.previousElementSibling, false)\" role=\"button\"></div>\n    </div>\n    <!-- ko if: canShowFooter -->\n    <div data-bind=\"css: survey.css.progressButtonsFooter\">\n        <div data-bind=\"css: survey.css.progressButtonsPageTitle, text: model.footerText, attr: { title: model.footerText }\"></div>\n    </div>\n    <!-- /ko -->\n</div>";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/progress.html":
/*!*************************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/components/progress/progress.html ***!
  \*************************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: getProgressCssClasses()\">\n    <div data-bind=\"css: model.css.progressBar, style: { width: model.progressValue + '%' }\"\n        role=\"progressbar\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-label=\"progress\">\n        <span data-bind=\"text: model.progressText, css: getProgressTextInBarCss(model.css)\"></span>\n    </div>\n    <span data-bind=\"text: model.progressText, css: getProgressTextUnderBarCss(model.css)\"></span>\n</div>";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/toc.html":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/components/progress/toc.html ***!
  \********************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: tocModel -->\n<div data-bind=\"css: containerCss\">\n    <!-- ko ifnot: isMobile -->\n    <sv-list params=\"model: listModel\"></sv-list>\n    <!-- /ko -->\n    <!-- ko if: isMobile -->\n    <div class=\"\" data-bind=\"click: togglePopup, key2click\">\n        <sv-svg-icon class=\"\" params=\"iconName: icon, size: 24\"></sv-svg-icon>\n        <sv-popup params=\"model: popupModel\"></sv-popup>\n    </div>\n    <!-- /ko -->\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/templates/entry.html":
/*!************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/templates/entry.html ***!
  \************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports, __webpack_require__) {

module.exports = "" + __webpack_require__(/*! ./comment.html */ "./src/knockout/templates/comment.html") + "\n" + __webpack_require__(/*! ./flowpanel.html */ "./src/knockout/templates/flowpanel.html") + "\n" + __webpack_require__(/*! ./header.html */ "./src/knockout/templates/header.html") + "\n" + __webpack_require__(/*! ./index.html */ "./src/knockout/templates/index.html") + "\n" + __webpack_require__(/*! ./page.html */ "./src/knockout/templates/page.html") + "\n" + __webpack_require__(/*! ./panel.html */ "./src/knockout/templates/panel.html") + "\n" + __webpack_require__(/*! ./rows.html */ "./src/knockout/templates/rows.html") + "\n" + __webpack_require__(/*! ./row.html */ "./src/knockout/templates/row.html") + "\n" + __webpack_require__(/*! ./string.html */ "./src/knockout/templates/string.html") + "\n" + __webpack_require__(/*! ./timerpanel.html */ "./src/knockout/templates/timerpanel.html") + "\n" + __webpack_require__(/*! ./question.html */ "./src/knockout/templates/question.html") + "\n" + __webpack_require__(/*! ./questioncontent.html */ "./src/knockout/templates/questioncontent.html") + "\n" + __webpack_require__(/*! ./questiontitle.html */ "./src/knockout/templates/questiontitle.html") + "\n" + __webpack_require__(/*! ./question-boolean.html */ "./src/knockout/templates/question-boolean.html") + "\n" + __webpack_require__(/*! ./question-checkbox.html */ "./src/knockout/templates/question-checkbox.html") + "\n" + __webpack_require__(/*! ./question-tagbox.html */ "./src/knockout/templates/question-tagbox.html") + "\n" + __webpack_require__(/*! ./question-ranking.html */ "./src/knockout/templates/question-ranking.html") + "\n" + __webpack_require__(/*! ./question-comment.html */ "./src/knockout/templates/question-comment.html") + "\n" + __webpack_require__(/*! ./question-composite.html */ "./src/knockout/templates/question-composite.html") + "\n" + __webpack_require__(/*! ./question-custom.html */ "./src/knockout/templates/question-custom.html") + "\n" + __webpack_require__(/*! ./question-dropdown.html */ "./src/knockout/templates/question-dropdown.html") + "\n" + __webpack_require__(/*! ./question-empty.html */ "./src/knockout/templates/question-empty.html") + "\n" + __webpack_require__(/*! ./question-errors.html */ "./src/knockout/templates/question-errors.html") + "\n" + __webpack_require__(/*! ./question-expression.html */ "./src/knockout/templates/question-expression.html") + "\n" + __webpack_require__(/*! ./question-file.html */ "./src/knockout/templates/question-file.html") + "\n" + __webpack_require__(/*! ./question-html.html */ "./src/knockout/templates/question-html.html") + "\n" + __webpack_require__(/*! ./question-image.html */ "./src/knockout/templates/question-image.html") + "\n" + __webpack_require__(/*! ./question-imagepicker.html */ "./src/knockout/templates/question-imagepicker.html") + "\n" + __webpack_require__(/*! ./question-matrix.html */ "./src/knockout/templates/question-matrix.html") + "\n" + __webpack_require__(/*! ./question-matrixdynamic.html */ "./src/knockout/templates/question-matrixdynamic.html") + "\n" + __webpack_require__(/*! ./question-matrixdropdown.html */ "./src/knockout/templates/question-matrixdropdown.html") + "\n" + __webpack_require__(/*! ./question-multipletext.html */ "./src/knockout/templates/question-multipletext.html") + "\n" + __webpack_require__(/*! ./question-paneldynamic.html */ "./src/knockout/templates/question-paneldynamic.html") + "\n" + __webpack_require__(/*! ./question-paneldynamic-navigator.html */ "./src/knockout/templates/question-paneldynamic-navigator.html") + "\n" + __webpack_require__(/*! ./question-radiogroup.html */ "./src/knockout/templates/question-radiogroup.html") + "\n" + __webpack_require__(/*! ./question-rating.html */ "./src/knockout/templates/question-rating.html") + "\n" + __webpack_require__(/*! ./question-signaturepad.html */ "./src/knockout/templates/question-signaturepad.html") + "\n" + __webpack_require__(/*! ./question-text.html */ "./src/knockout/templates/question-text.html") + "\n" + __webpack_require__(/*! ./question-buttongroup.html */ "./src/knockout/templates/question-buttongroup.html") + "\n" + __webpack_require__(/*! ./popup-pointer.html */ "./src/knockout/templates/popup-pointer.html") + "";

/***/ }),

/***/ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/templates/window.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/html-loader?interpolate!./node_modules/val-loader!./src/knockout/templates/window.html ***!
  \*************************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: cssRoot, style:{width: renderedWidth, maxWidth: renderedWidth}, event: { scroll: $data.onScroll }\">\n    <div data-bind=\"css: cssRootContent\">\n        <div data-bind=\"css: cssHeaderRoot, {cssRootCollapsedMod: isCollapsed}\">\n\n            <!-- ko if: isCollapsed && !!locTitle -->  \n            <div data-bind=\"css: cssHeaderTitleCollapsed, text: locTitle.koRenderedHtml\"></div>\n            <!-- /ko -->\n    \n            <div data-bind=\"css: cssHeaderButtonsContainer\">\n                <!-- ko if: allowFullScreen -->      \n                <div data-bind=\"click:doToggleFullScreen, css: cssHeaderFullScreenButton\">\n                    <!-- ko if: isFullScreen-->  \n                    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-back-to-panel_16x16', size: '16' } } --><!-- /ko -->\n                    <!-- /ko -->\n                    \n                    <!-- ko if: !isFullScreen-->  \n                    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-full-screen_16x16', size: '16' } } --><!-- /ko -->\n                    <!-- /ko -->\n                </div>\n                <!-- /ko -->\n                <div data-bind=\"click:doExpand, css: cssHeaderCollapseButton\">\n                    <!-- ko if: isExpanded-->  \n                    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-minimize_16x16', size: '16' } } --><!-- /ko -->\n                    <!-- /ko -->\n                    \n                    <!-- ko if: isCollapsed-->  \n                    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-restore_16x16', size: '16' } } --><!-- /ko -->\n                    <!-- /ko -->\n                </div>\n                <!-- ko if: allowClose -->      \n                <div data-bind=\"click:doHide, css: cssHeaderCloseButton\">\n                <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-close_16x16', size: '16' } } --><!-- /ko -->\n                </div>\n                <!-- /ko -->\n            </div>\n        </div>\n        <div data-bind=\"visible:isExpanded, css: cssBody\">\n            <survey params=\"survey: survey\"></survey>\n        </div>\n    </div>\n</div>";

/***/ }),

/***/ "./packages/survey-core/src/images-v1 sync recursive \\.svg$":
/*!********************************************************!*\
  !*** ./packages/survey-core/src/images-v1 sync \.svg$ ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"./ModernBooleanCheckChecked.svg": "./packages/survey-core/src/images-v1/ModernBooleanCheckChecked.svg",
	"./ModernBooleanCheckInd.svg": "./packages/survey-core/src/images-v1/ModernBooleanCheckInd.svg",
	"./ModernBooleanCheckUnchecked.svg": "./packages/survey-core/src/images-v1/ModernBooleanCheckUnchecked.svg",
	"./ModernCheck.svg": "./packages/survey-core/src/images-v1/ModernCheck.svg",
	"./ModernRadio.svg": "./packages/survey-core/src/images-v1/ModernRadio.svg",
	"./ProgressButton.svg": "./packages/survey-core/src/images-v1/ProgressButton.svg",
	"./RemoveFile.svg": "./packages/survey-core/src/images-v1/RemoveFile.svg",
	"./TimerCircle.svg": "./packages/survey-core/src/images-v1/TimerCircle.svg",
	"./add-24x24.svg": "./packages/survey-core/src/images-v1/add-24x24.svg",
	"./arrowleft-16x16.svg": "./packages/survey-core/src/images-v1/arrowleft-16x16.svg",
	"./arrowright-16x16.svg": "./packages/survey-core/src/images-v1/arrowright-16x16.svg",
	"./camera-24x24.svg": "./packages/survey-core/src/images-v1/camera-24x24.svg",
	"./camera-32x32.svg": "./packages/survey-core/src/images-v1/camera-32x32.svg",
	"./cancel-24x24.svg": "./packages/survey-core/src/images-v1/cancel-24x24.svg",
	"./check-16x16.svg": "./packages/survey-core/src/images-v1/check-16x16.svg",
	"./check-24x24.svg": "./packages/survey-core/src/images-v1/check-24x24.svg",
	"./chevrondown-24x24.svg": "./packages/survey-core/src/images-v1/chevrondown-24x24.svg",
	"./chevronright-16x16.svg": "./packages/survey-core/src/images-v1/chevronright-16x16.svg",
	"./clear-16x16.svg": "./packages/survey-core/src/images-v1/clear-16x16.svg",
	"./clear-24x24.svg": "./packages/survey-core/src/images-v1/clear-24x24.svg",
	"./close-16x16.svg": "./packages/survey-core/src/images-v1/close-16x16.svg",
	"./close-24x24.svg": "./packages/survey-core/src/images-v1/close-24x24.svg",
	"./collapse-16x16.svg": "./packages/survey-core/src/images-v1/collapse-16x16.svg",
	"./collapsedetails-16x16.svg": "./packages/survey-core/src/images-v1/collapsedetails-16x16.svg",
	"./delete-24x24.svg": "./packages/survey-core/src/images-v1/delete-24x24.svg",
	"./drag-24x24.svg": "./packages/survey-core/src/images-v1/drag-24x24.svg",
	"./draghorizontal-24x16.svg": "./packages/survey-core/src/images-v1/draghorizontal-24x16.svg",
	"./expand-16x16.svg": "./packages/survey-core/src/images-v1/expand-16x16.svg",
	"./expanddetails-16x16.svg": "./packages/survey-core/src/images-v1/expanddetails-16x16.svg",
	"./file-72x72.svg": "./packages/survey-core/src/images-v1/file-72x72.svg",
	"./flip-24x24.svg": "./packages/survey-core/src/images-v1/flip-24x24.svg",
	"./folder-24x24.svg": "./packages/survey-core/src/images-v1/folder-24x24.svg",
	"./fullsize-16x16.svg": "./packages/survey-core/src/images-v1/fullsize-16x16.svg",
	"./image-48x48.svg": "./packages/survey-core/src/images-v1/image-48x48.svg",
	"./loading-48x48.svg": "./packages/survey-core/src/images-v1/loading-48x48.svg",
	"./maximize-16x16.svg": "./packages/survey-core/src/images-v1/maximize-16x16.svg",
	"./minimize-16x16.svg": "./packages/survey-core/src/images-v1/minimize-16x16.svg",
	"./more-24x24.svg": "./packages/survey-core/src/images-v1/more-24x24.svg",
	"./navmenu-24x24.svg": "./packages/survey-core/src/images-v1/navmenu-24x24.svg",
	"./noimage-48x48.svg": "./packages/survey-core/src/images-v1/noimage-48x48.svg",
	"./ranking-arrows.svg": "./packages/survey-core/src/images-v1/ranking-arrows.svg",
	"./rankingundefined-16x16.svg": "./packages/survey-core/src/images-v1/rankingundefined-16x16.svg",
	"./rating-star-2.svg": "./packages/survey-core/src/images-v1/rating-star-2.svg",
	"./rating-star-small-2.svg": "./packages/survey-core/src/images-v1/rating-star-small-2.svg",
	"./rating-star-small.svg": "./packages/survey-core/src/images-v1/rating-star-small.svg",
	"./rating-star.svg": "./packages/survey-core/src/images-v1/rating-star.svg",
	"./reorder-24x24.svg": "./packages/survey-core/src/images-v1/reorder-24x24.svg",
	"./restoredown-16x16.svg": "./packages/survey-core/src/images-v1/restoredown-16x16.svg",
	"./search-24x24.svg": "./packages/survey-core/src/images-v1/search-24x24.svg",
	"./smiley-rate1-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate1-24x24.svg",
	"./smiley-rate10-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate10-24x24.svg",
	"./smiley-rate2-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate2-24x24.svg",
	"./smiley-rate3-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate3-24x24.svg",
	"./smiley-rate4-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate4-24x24.svg",
	"./smiley-rate5-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate5-24x24.svg",
	"./smiley-rate6-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate6-24x24.svg",
	"./smiley-rate7-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate7-24x24.svg",
	"./smiley-rate8-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate8-24x24.svg",
	"./smiley-rate9-24x24.svg": "./packages/survey-core/src/images-v1/smiley-rate9-24x24.svg"
};


function webpackContext(req) {
	var id = webpackContextResolve(req);
	return __webpack_require__(id);
}
function webpackContextResolve(req) {
	if(!__webpack_require__.o(map, req)) {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	}
	return map[req];
}
webpackContext.keys = function webpackContextKeys() {
	return Object.keys(map);
};
webpackContext.resolve = webpackContextResolve;
module.exports = webpackContext;
webpackContext.id = "./packages/survey-core/src/images-v1 sync recursive \\.svg$";

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ModernBooleanCheckChecked.svg":
/*!**************************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ModernBooleanCheckChecked.svg ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><polygon points=\"19,10 14,10 14,5 10,5 10,10 5,10 5,14 10,14 10,19 14,19 14,14 19,14 \"></polygon></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ModernBooleanCheckInd.svg":
/*!**********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ModernBooleanCheckInd.svg ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><path d=\"M22,0H2C0.9,0,0,0.9,0,2v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V2C24,0.9,23.1,0,22,0z M21,18L6,3h15V18z M3,6l15,15H3V6z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ModernBooleanCheckUnchecked.svg":
/*!****************************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ModernBooleanCheckUnchecked.svg ***!
  \****************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><rect x=\"5\" y=\"10\" width=\"14\" height=\"4\"></rect></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ModernCheck.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ModernCheck.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\"><path d=\"M5,13l2-2l3,3l7-7l2,2l-9,9L5,13z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ModernRadio.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ModernRadio.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"-12 -12 24 24\"><circle r=\"6\" cx=\"0\" cy=\"0\"></circle></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ProgressButton.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ProgressButton.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 10 10\"><polygon points=\"2,2 0,4 5,9 10,4 8,2 5,5 \"></polygon></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/RemoveFile.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/RemoveFile.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\"><path d=\"M8,2C4.7,2,2,4.7,2,8s2.7,6,6,6s6-2.7,6-6S11.3,2,8,2z M11,10l-1,1L8,9l-2,2l-1-1l2-2L5,6l1-1l2,2l2-2l1,1L9,8 L11,10z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/TimerCircle.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/TimerCircle.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" viewBox=\"0 0 160 160\"><circle cx=\"80\" cy=\"80\" r=\"70\" style=\"stroke: var(--sd-timer-stroke-background-color); stroke-width: var(--sd-timer-stroke-background-width)\" stroke-dasharray=\"none\" stroke-dashoffset=\"none\"></circle><circle cx=\"80\" cy=\"80\" r=\"70\"></circle></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/add-24x24.svg":
/*!**********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/add-24x24.svg ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 11H17V13H13V17H11V13H7V11H11V7H13V11ZM23 12C23 18.1 18.1 23 12 23C5.9 23 1 18.1 1 12C1 5.9 5.9 1 12 1C18.1 1 23 5.9 23 12ZM21 12C21 7 17 3 12 3C7 3 3 7 3 12C3 17 7 21 12 21C17 21 21 17 21 12Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/arrowleft-16x16.svg":
/*!****************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/arrowleft-16x16.svg ***!
  \****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M15 8.99999H4.4L8.7 13.3L7.3 14.7L0.599998 7.99999L7.3 1.29999L8.7 2.69999L4.4 6.99999H15V8.99999Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/arrowright-16x16.svg":
/*!*****************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/arrowright-16x16.svg ***!
  \*****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M1 6.99999H11.6L7.3 2.69999L8.7 1.29999L15.4 7.99999L8.7 14.7L7.3 13.3L11.6 8.99999H1V6.99999Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/camera-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/camera-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M20.01 4H18.4C18.2 4 18.01 3.9 17.9 3.73L16.97 2.34C16.41 1.5 15.48 1 14.47 1H9.54C8.53 1 7.6 1.5 7.04 2.34L6.11 3.73C6 3.9 5.81 4 5.61 4H4C2.35 4 1 5.35 1 7V19C1 20.65 2.35 22 4 22H20C21.65 22 23 20.65 23 19V7C23 5.35 21.65 4 20 4H20.01ZM21.01 19C21.01 19.55 20.56 20 20.01 20H4.01C3.46 20 3.01 19.55 3.01 19V7C3.01 6.45 3.46 6 4.01 6H5.62C6.49 6 7.3 5.56 7.79 4.84L8.72 3.45C8.91 3.17 9.22 3 9.55 3H14.48C14.81 3 15.13 3.17 15.31 3.45L16.24 4.84C16.72 5.56 17.54 6 18.41 6H20.02C20.57 6 21.02 6.45 21.02 7V19H21.01ZM12.01 6C8.7 6 6.01 8.69 6.01 12C6.01 15.31 8.7 18 12.01 18C15.32 18 18.01 15.31 18.01 12C18.01 8.69 15.32 6 12.01 6ZM12.01 16C9.8 16 8.01 14.21 8.01 12C8.01 9.79 9.8 8 12.01 8C14.22 8 16.01 9.79 16.01 12C16.01 14.21 14.22 16 12.01 16ZM13.01 10C13.01 10.55 12.56 11 12.01 11C11.46 11 11.01 11.45 11.01 12C11.01 12.55 10.56 13 10.01 13C9.46 13 9.01 12.55 9.01 12C9.01 10.35 10.36 9 12.01 9C12.56 9 13.01 9.45 13.01 10Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/camera-32x32.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/camera-32x32.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 32 32\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M27 6H23.8C23.34 6 22.92 5.77 22.66 5.39L22.25 4.78C21.51 3.66 20.26 3 18.92 3H13.06C11.72 3 10.48 3.67 9.73 4.78L9.32 5.39C9.07 5.77 8.64 6 8.18 6H4.98C2.79 6 1 7.79 1 10V24C1 26.21 2.79 28 5 28H27C29.21 28 31 26.21 31 24V10C31 7.79 29.21 6 27 6ZM29 24C29 25.1 28.1 26 27 26H5C3.9 26 3 25.1 3 24V10C3 8.9 3.9 8 5 8H8.2C9.33 8 10.38 7.44 11 6.5L11.41 5.89C11.78 5.33 12.41 5 13.07 5H18.93C19.6 5 20.22 5.33 20.59 5.89L21 6.5C21.62 7.44 22.68 8 23.8 8H27C28.1 8 29 8.9 29 10V24ZM16 9C12.13 9 9 12.13 9 16C9 19.87 12.13 23 16 23C19.87 23 23 19.87 23 16C23 12.13 19.87 9 16 9ZM16 21C13.24 21 11 18.76 11 16C11 13.24 13.24 11 16 11C18.76 11 21 13.24 21 16C21 18.76 18.76 21 16 21ZM17 13C17 13.55 16.55 14 16 14C14.9 14 14 14.9 14 16C14 16.55 13.55 17 13 17C12.45 17 12 16.55 12 16C12 13.79 13.79 12 16 12C16.55 12 17 12.45 17 13Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/cancel-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/cancel-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M22.6 8.6L16.4 2.4C16 2 15.5 1.8 15 1.8C14.5 1.8 14 2 13.6 2.4L1.40005 14.6C0.600049 15.4 0.600049 16.6 1.40005 17.4L6.00005 22H12L22.6 11.4C23.3 10.6 23.3 9.3 22.6 8.6ZM11.1 20H6.80005L2.80005 16L6.20005 12.6L12.4 18.8L11.1 20ZM13.8 17.4L7.60005 11.2L15 3.8L21.2 10L13.8 17.4ZM16 20H23V22H14L16 20Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/check-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/check-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M5.003 14.413L0.292999 9.70303L1.703 8.29303L5.003 11.583L14.293 2.29303L15.703 3.70303L5.003 14.413Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/check-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/check-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M9 20.1L1 12L3.1 9.9L9 15.9L20.9 4L23 6.1L9 20.1Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/chevrondown-24x24.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/chevrondown-24x24.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 15L17 10H7L12 15Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/chevronright-16x16.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/chevronright-16x16.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M5.64648 12.6465L6.34648 13.3465L11.7465 8.04648L6.34648 2.64648L5.64648 3.34648L10.2465 8.04648L5.64648 12.6465Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/clear-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/clear-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.35 3.34999L12.65 2.64999L8.05002 7.24999L3.35002 2.64999L2.65002 3.34999L7.25002 8.04999L2.65002 12.65L3.35002 13.35L8.05002 8.74999L12.65 13.35L13.35 12.65L8.75002 8.04999L13.35 3.34999Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/clear-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/clear-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M22.6 8.6L16.4 2.4C16 2 15.5 1.8 15 1.8C14.5 1.8 14 2 13.6 2.4L1.40005 14.6C0.600049 15.4 0.600049 16.6 1.40005 17.4L6.00005 22H12L22.6 11.4C23.3 10.6 23.3 9.3 22.6 8.6ZM11.1 20H6.80005L2.80005 16L6.20005 12.6L12.4 18.8L11.1 20ZM13.8 17.4L7.60005 11.2L15 3.8L21.2 10L13.8 17.4ZM16 20H23V22H14L16 20Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/close-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/close-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M9.43 8.0025L13.7 3.7225C14.09 3.3325 14.09 2.6925 13.7 2.2925C13.31 1.9025 12.67 1.9025 12.27 2.2925L7.99 6.5725L3.72 2.3025C3.33 1.9025 2.69 1.9025 2.3 2.3025C1.9 2.6925 1.9 3.3325 2.3 3.7225L6.58 8.0025L2.3 12.2825C1.91 12.6725 1.91 13.3125 2.3 13.7125C2.69 14.1025 3.33 14.1025 3.73 13.7125L8.01 9.4325L12.29 13.7125C12.68 14.1025 13.32 14.1025 13.72 13.7125C14.11 13.3225 14.11 12.6825 13.72 12.2825L9.44 8.0025H9.43Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/close-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/close-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.4101 12L20.7001 4.71C21.0901 4.32 21.0901 3.69 20.7001 3.3C20.3101 2.91 19.6801 2.91 19.2901 3.3L12.0001 10.59L4.71006 3.29C4.32006 2.9 3.68006 2.9 3.29006 3.29C2.90006 3.68 2.90006 4.32 3.29006 4.71L10.5801 12L3.29006 19.29C2.90006 19.68 2.90006 20.31 3.29006 20.7C3.49006 20.9 3.74006 20.99 4.00006 20.99C4.26006 20.99 4.51006 20.89 4.71006 20.7L12.0001 13.41L19.2901 20.7C19.4901 20.9 19.7401 20.99 20.0001 20.99C20.2601 20.99 20.5101 20.89 20.7101 20.7C21.1001 20.31 21.1001 19.68 20.7101 19.29L13.4201 12H13.4101Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/collapse-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/collapse-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M2 6L3 5L8 10L13 5L14 6L8 12L2 6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/collapsedetails-16x16.svg":
/*!**********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/collapsedetails-16x16.svg ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 7H3V9H13V7Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/delete-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/delete-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M22 4H20H16V2C16 0.9 15.1 0 14 0H10C8.9 0 8 0.9 8 2V4H4H2V6H4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V6H22V4ZM10 2H14V4H10V2ZM18 20H6V6H8H16H18V20ZM14 8H16V18H14V8ZM11 8H13V18H11V8ZM8 8H10V18H8V8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/drag-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/drag-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 6C13 4.9 13.9 4 15 4C16.1 4 17 4.9 17 6C17 7.1 16.1 8 15 8C13.9 8 13 7.1 13 6ZM9 4C7.9 4 7 4.9 7 6C7 7.1 7.9 8 9 8C10.1 8 11 7.1 11 6C11 4.9 10.1 4 9 4ZM15 10C13.9 10 13 10.9 13 12C13 13.1 13.9 14 15 14C16.1 14 17 13.1 17 12C17 10.9 16.1 10 15 10ZM9 10C7.9 10 7 10.9 7 12C7 13.1 7.9 14 9 14C10.1 14 11 13.1 11 12C11 10.9 10.1 10 9 10ZM15 16C13.9 16 13 16.9 13 18C13 19.1 13.9 20 15 20C16.1 20 17 19.1 17 18C17 16.9 16.1 16 15 16ZM9 16C7.9 16 7 16.9 7 18C7 19.1 7.9 20 9 20C10.1 20 11 19.1 11 18C11 16.9 10.1 16 9 16Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/draghorizontal-24x16.svg":
/*!*********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/draghorizontal-24x16.svg ***!
  \*********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M18 9C19.1 9 20 9.9 20 11C20 12.1 19.1 13 18 13C16.9 13 16 12.1 16 11C16 9.9 16.9 9 18 9ZM20 5C20 3.9 19.1 3 18 3C16.9 3 16 3.9 16 5C16 6.1 16.9 7 18 7C19.1 7 20 6.1 20 5ZM14 11C14 9.9 13.1 9 12 9C10.9 9 10 9.9 10 11C10 12.1 10.9 13 12 13C13.1 13 14 12.1 14 11ZM14 5C14 3.9 13.1 3 12 3C10.9 3 10 3.9 10 5C10 6.1 10.9 7 12 7C13.1 7 14 6.1 14 5ZM8 11C8 9.9 7.1 9 6 9C4.9 9 4 9.9 4 11C4 12.1 4.9 13 6 13C7.1 13 8 12.1 8 11ZM8 5C8 3.9 7.1 3 6 3C4.9 3 4 3.9 4 5C4 6.1 4.9 7 6 7C7.1 7 8 6.1 8 5Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/expand-16x16.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/expand-16x16.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M6 14L5 13L10 8L5 3L6 2L12 8L6 14Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/expanddetails-16x16.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/expanddetails-16x16.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 7H9V3H7V7H3V9H7V13H9V9H13V7Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/file-72x72.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/file-72x72.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 72 72\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M62.83 12.83L53.17 3.17C52.7982 2.79866 52.357 2.50421 51.8714 2.30346C51.3858 2.1027 50.8654 1.99959 50.34 2H14C12.4087 2 10.8826 2.63214 9.75735 3.75736C8.63214 4.88258 8 6.4087 8 8V64C8 65.5913 8.63214 67.1174 9.75735 68.2426C10.8826 69.3679 12.4087 70 14 70H58C59.5913 70 61.1174 69.3679 62.2426 68.2426C63.3679 67.1174 64 65.5913 64 64V15.66C64.0004 15.1346 63.8973 14.6142 63.6965 14.1286C63.4958 13.643 63.2013 13.2018 62.83 12.83ZM52 4.83L61.17 14H56C54.9391 14 53.9217 13.5786 53.1716 12.8284C52.4214 12.0783 52 11.0609 52 10V4.83ZM62 64C62 65.0609 61.5786 66.0783 60.8284 66.8284C60.0783 67.5786 59.0609 68 58 68H14C12.9391 68 11.9217 67.5786 11.1716 66.8284C10.4214 66.0783 10 65.0609 10 64V8C10 6.93914 10.4214 5.92172 11.1716 5.17157C11.9217 4.42143 12.9391 4 14 4H50V10C50 11.5913 50.6321 13.1174 51.7574 14.2426C52.8826 15.3679 54.4087 16 56 16H62V64ZM22 26H50V28H22V26ZM22 32H50V34H22V32ZM22 38H50V40H22V38ZM22 44H50V46H22V44Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/flip-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/flip-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M23 12.0037C23 14.2445 21.7794 16.3052 19.5684 17.8257C19.3984 17.9458 19.1983 18.0058 19.0082 18.0058C18.688 18.0058 18.3779 17.8557 18.1778 17.5756C17.8677 17.1155 17.9777 16.4953 18.4379 16.1852C20.0887 15.0448 21.0091 13.5643 21.0091 12.0138C21.0091 8.70262 16.9673 6.01171 12.005 6.01171C11.4948 6.01171 10.9945 6.04172 10.5043 6.09173L11.7149 7.30215C12.105 7.69228 12.105 8.32249 11.7149 8.71263C11.5148 8.9127 11.2647 9.00273 11.0045 9.00273C10.7444 9.00273 10.4943 8.90269 10.2942 8.71263L6.58254 5.00136L10.2842 1.2901C10.6744 0.899964 11.3047 0.899964 11.6949 1.2901C12.085 1.68023 12.085 2.31045 11.6949 2.70058L10.3042 4.09105C10.8545 4.03103 11.4147 4.00102 11.985 4.00102C18.0578 4.00102 22.99 7.59225 22.99 12.0037H23ZM12.2851 15.2949C11.895 15.685 11.895 16.3152 12.2851 16.7054L13.4957 17.9158C13.0055 17.9758 12.4952 17.9958 11.995 17.9958C7.03274 17.9958 2.99091 15.3049 2.99091 11.9937C2.99091 10.4332 3.90132 8.95271 5.56207 7.82232C6.02228 7.51222 6.13233 6.89201 5.82219 6.43185C5.51205 5.97169 4.89177 5.86166 4.43156 6.17176C2.22055 7.69228 1 9.76299 1 11.9937C1 16.4052 5.93224 19.9965 12.005 19.9965C12.5753 19.9965 13.1355 19.9665 13.6858 19.9064L12.2951 21.2969C11.905 21.6871 11.905 22.3173 12.2951 22.7074C12.4952 22.9075 12.7453 22.9975 13.0055 22.9975C13.2656 22.9975 13.5157 22.8975 13.7158 22.7074L17.4275 18.9961L13.7158 15.2849C13.3256 14.8947 12.6953 14.8947 12.3051 15.2849L12.2851 15.2949Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/folder-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/folder-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M21.93 9H21V7C21 6.46957 20.7893 5.96086 20.4142 5.58579C20.0391 5.21071 19.5304 5 19 5H10L8 3H4C3.46957 3 2.96086 3.21071 2.58579 3.58579C2.21071 3.96086 2 4.46957 2 5L2 21H21L23.89 11.63C23.9916 11.3244 24.0179 10.9988 23.9667 10.6809C23.9155 10.363 23.7882 10.0621 23.5958 9.80392C23.4034 9.54571 23.1514 9.33779 22.8614 9.19782C22.5714 9.05786 22.2519 8.99 21.93 9ZM4 5H7.17L8.59 6.41L9.17 7H19V9H6L4 15V5ZM22 11L19.54 19H4.77L7.44 11H22Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/fullsize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/fullsize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 13H4C2.9 13 2 12.1 2 11V5C2 3.9 2.9 3 4 3H12C13.1 3 14 3.9 14 5V11C14 12.1 13.1 13 12 13ZM4 5V11H12V5H4Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/image-48x48.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/image-48x48.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M36 8H12C9.79 8 8 9.79 8 12V36C8 38.21 9.79 40 12 40H36C38.21 40 40 38.21 40 36V12C40 9.79 38.21 8 36 8ZM38 36C38 37.1 37.1 38 36 38H12C10.9 38 10 37.1 10 36V12C10 10.9 10.9 10 12 10H36C37.1 10 38 10.9 38 12V36ZM14 17C14 15.34 15.34 14 17 14C18.66 14 20 15.34 20 17C20 18.66 18.66 20 17 20C15.34 20 14 18.66 14 17ZM27 24L36 36H12L19 27L23 29L27 24Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/loading-48x48.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/loading-48x48.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><g clip-path=\"url(#clip0_19679_369428)\"><path opacity=\"0.1\" d=\"M24 40C15.18 40 8 32.82 8 24C8 15.18 15.18 8 24 8C32.82 8 40 15.18 40 24C40 32.82 32.82 40 24 40ZM24 12C17.38 12 12 17.38 12 24C12 30.62 17.38 36 24 36C30.62 36 36 30.62 36 24C36 17.38 30.62 12 24 12Z\" fill=\"black\" fill-opacity=\"0.91\"></path><path d=\"M10 26C8.9 26 8 25.1 8 24C8 15.18 15.18 8 24 8C25.1 8 26 8.9 26 10C26 11.1 25.1 12 24 12C17.38 12 12 17.38 12 24C12 25.1 11.1 26 10 26Z\" fill=\"#19B394\"></path></g><defs><clipPath id=\"clip0_19679_369428\"><rect width=\"32\" height=\"32\" fill=\"white\" transform=\"translate(8 8)\"></rect></clipPath></defs></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/maximize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/maximize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M6.71 10.71L4.42 13H6.01C6.56 13 7.01 13.45 7.01 14C7.01 14.55 6.56 15 6.01 15H2C1.45 15 1 14.55 1 14V10C1 9.45 1.45 9 2 9C2.55 9 3 9.45 3 10V11.59L5.29 9.3C5.68 8.91 6.31 8.91 6.7 9.3C7.09 9.69 7.09 10.32 6.7 10.71H6.71ZM14 1H10C9.45 1 9 1.45 9 2C9 2.55 9.45 3 10 3H11.59L9.3 5.29C8.91 5.68 8.91 6.31 9.3 6.7C9.5 6.9 9.75 6.99 10.01 6.99C10.27 6.99 10.52 6.89 10.72 6.7L13.01 4.41V6C13.01 6.55 13.46 7 14.01 7C14.56 7 15.01 6.55 15.01 6V2C15.01 1.45 14.56 1 14.01 1H14Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/minimize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/minimize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 9H3C2.45 9 2 8.55 2 8C2 7.45 2.45 7 3 7H13C13.55 7 14 7.45 14 8C14 8.55 13.55 9 13 9Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/more-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v1/more-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M6 12C6 13.1 5.1 14 4 14C2.9 14 2 13.1 2 12C2 10.9 2.9 10 4 10C5.1 10 6 10.9 6 12ZM12 10C10.9 10 10 10.9 10 12C10 13.1 10.9 14 12 14C13.1 14 14 13.1 14 12C14 10.9 13.1 10 12 10ZM20 10C18.9 10 18 10.9 18 12C18 13.1 18.9 14 20 14C21.1 14 22 13.1 22 12C22 10.9 21.1 10 20 10Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/navmenu-24x24.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/navmenu-24x24.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M16 7H2V5H16V7ZM2 11V13H22V11H2ZM2 19H10V17H2V19Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/noimage-48x48.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/noimage-48x48.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14 17.01C14 16.4167 14.1759 15.8366 14.5056 15.3433C14.8352 14.8499 15.3038 14.4654 15.8519 14.2384C16.4001 14.0113 17.0033 13.9519 17.5853 14.0676C18.1672 14.1834 18.7018 14.4691 19.1213 14.8887C19.5409 15.3082 19.8266 15.8428 19.9424 16.4247C20.0581 17.0067 19.9987 17.6099 19.7716 18.1581C19.5446 18.7062 19.1601 19.1748 18.6667 19.5044C18.1734 19.8341 17.5933 20.01 17 20.01C16.2044 20.01 15.4413 19.6939 14.8787 19.1313C14.3161 18.5687 14 17.8056 14 17.01ZM27.09 24.14L20 36.01H36L27.09 24.14ZM36.72 8.14L35.57 10.01H36C36.5304 10.01 37.0391 10.2207 37.4142 10.5958C37.7893 10.9709 38 11.4796 38 12.01V36.01C38 36.5404 37.7893 37.0491 37.4142 37.4242C37.0391 37.7993 36.5304 38.01 36 38.01H18.77L17.57 40.01H36C37.0609 40.01 38.0783 39.5886 38.8284 38.8384C39.5786 38.0883 40 37.0709 40 36.01V12.01C39.9966 11.0765 39.6668 10.1737 39.0678 9.45778C38.4688 8.74188 37.6382 8.25802 36.72 8.09V8.14ZM36.86 4.5L12.86 44.5L11.14 43.5L13.23 40.01H12C10.9391 40.01 9.92172 39.5886 9.17157 38.8384C8.42143 38.0883 8 37.0709 8 36.01V12.01C8 10.9491 8.42143 9.93172 9.17157 9.18157C9.92172 8.43143 10.9391 8.01 12 8.01H32.43L35.14 3.5L36.86 4.5ZM14.43 38.01L15.63 36.01H12L19 27.01L20.56 27.8L31.23 10.01H12C11.4696 10.01 10.9609 10.2207 10.5858 10.5958C10.2107 10.9709 10 11.4796 10 12.01V36.01C10 36.5404 10.2107 37.0491 10.5858 37.4242C10.9609 37.7993 11.4696 38.01 12 38.01H14.43Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/ranking-arrows.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/ranking-arrows.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 10 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M10 5L5 0L0 5H4V9H6V5H10Z\"></path><path d=\"M6 19V15H4V19H0L5 24L10 19H6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/rankingundefined-16x16.svg":
/*!***********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/rankingundefined-16x16.svg ***!
  \***********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13 7H3V9H13V7Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/rating-star-2.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/rating-star-2.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M24 39.5057L11.7226 45.9839C10.4095 46.6739 8.87606 45.5622 9.12525 44.096L11.4734 30.373L1.54411 20.6556C0.480254 19.6207 1.06489 17.8095 2.53128 17.5986L16.2559 15.5957L22.3994 3.10891C23.0512 1.77685 24.9488 1.77685 25.6102 3.10891L31.7441 15.5957L45.4687 17.5986C46.9351 17.8095 47.5197 19.6207 46.4559 20.6556L36.5266 30.373L38.8748 44.096C39.1239 45.5622 37.5905 46.6835 36.2774 45.9839L24 39.5057Z\" fill=\"none\" stroke-width=\"2\"></path><path d=\"M24.3981 33.1305L24 32.9206L23.6019 33.1305L15.8715 37.2059L17.3542 28.5663L17.43 28.1246L17.1095 27.8113L10.83 21.6746L19.4965 20.4049L19.9405 20.3399L20.1387 19.9373L24 12.0936L27.8613 19.9373L28.0595 20.3399L28.5035 20.4049L37.17 21.6746L30.8905 27.8113L30.57 28.1246L30.6458 28.5663L32.1285 37.2059L24.3981 33.1305Z\" stroke-width=\"1.70746\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/rating-star-small-2.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/rating-star-small-2.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 19.3373L6.13001 22.4373C5.50001 22.7673 4.77001 22.2373 4.89001 21.5373L6.01001 14.9773L1.26001 10.3273C0.750007 9.83728 1.03001 8.96728 1.73001 8.86728L8.29001 7.90728L11.23 1.93728C11.54 1.29728 12.45 1.29728 12.77 1.93728L15.7 7.90728L22.26 8.86728C22.96 8.96728 23.24 9.83728 22.73 10.3273L17.98 14.9773L19.1 21.5373C19.22 22.2373 18.49 22.7773 17.86 22.4373L11.99 19.3373H12Z\" fill=\"none\" stroke-width=\"2\"></path><path d=\"M12 15.9472L8.58001 17.7572L9.23001 13.9272L6.45001 11.2072L10.29 10.6472L12 7.17725L13.71 10.6472L17.55 11.2072L14.77 13.9272L15.42 17.7572L12 15.9472Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/rating-star-small.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/rating-star-small.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><g><path d=\"M12 19.3373L6.13001 22.4373C5.50001 22.7673 4.77001 22.2373 4.89001 21.5373L6.01001 14.9773L1.26001 10.3273C0.750007 9.83728 1.03001 8.96728 1.73001 8.86728L8.29001 7.90728L11.23 1.93728C11.54 1.29728 12.45 1.29728 12.77 1.93728L15.7 7.90728L22.26 8.86728C22.96 8.96728 23.24 9.83728 22.73 10.3273L17.98 14.9773L19.1 21.5373C19.22 22.2373 18.49 22.7773 17.86 22.4373L11.99 19.3373H12Z\"></path></g></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/rating-star.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/rating-star.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><g><path d=\"M24 39.5057L11.7226 45.9839C10.4095 46.6739 8.87606 45.5622 9.12525 44.096L11.4734 30.373L1.54411 20.6556C0.480254 19.6207 1.06489 17.8095 2.53128 17.5986L16.2559 15.5957L22.3994 3.10891C23.0512 1.77685 24.9488 1.77685 25.6102 3.10891L31.7441 15.5957L45.4687 17.5986C46.9351 17.8095 47.5197 19.6207 46.4559 20.6556L36.5266 30.373L38.8748 44.096C39.1239 45.5622 37.5905 46.6835 36.2774 45.9839L24 39.5057Z\"></path></g></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/reorder-24x24.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/reorder-24x24.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M17 5L12 0L7 5H11V9H13V5H17Z\"></path><path d=\"M13 19V15H11V19H7L12 24L17 19H13Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/restoredown-16x16.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/restoredown-16x16.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M15 6C15 6.55 14.55 7 14 7H10C9.45 7 9 6.55 9 6V2C9 1.45 9.45 1 10 1C10.55 1 11 1.45 11 2V3.59L13.29 1.29C13.49 1.09 13.74 1 14 1C14.26 1 14.51 1.1 14.71 1.29C15.1 1.68 15.1 2.31 14.71 2.7L12.42 4.99H14.01C14.56 4.99 15.01 5.44 15.01 5.99L15 6ZM6 9H2C1.45 9 0.999998 9.45 0.999998 10C0.999998 10.55 1.45 11 2 11H3.59L1.29 13.29C0.899998 13.68 0.899998 14.31 1.29 14.7C1.68 15.09 2.31 15.09 2.7 14.7L4.99 12.41V14C4.99 14.55 5.44 15 5.99 15C6.54 15 6.99 14.55 6.99 14V10C6.99 9.45 6.54 9 5.99 9H6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/search-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/search-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14 2C9.6 2 6 5.6 6 10C6 11.8 6.6 13.5 7.7 14.9L2.3 20.3C1.9 20.7 1.9 21.3 2.3 21.7C2.5 21.9 2.7 22 3 22C3.3 22 3.5 21.9 3.7 21.7L9.1 16.3C10.5 17.4 12.2 18 14 18C18.4 18 22 14.4 22 10C22 5.6 18.4 2 14 2ZM14 16C10.7 16 8 13.3 8 10C8 6.7 10.7 4 14 4C17.3 4 20 6.7 20 10C20 13.3 17.3 16 14 16Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate1-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate1-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M4 4.9938C4 4.44362 4.45 3.99348 5 3.99348H6.59L5.3 2.70306C4.91 2.31293 4.91 1.68272 5.3 1.2926C5.69 0.902468 6.32 0.902468 6.71 1.2926L9.71 4.29357C9.8 4.3836 9.88 4.49364 9.93 4.62368C10.03 4.86376 10.03 5.14385 9.93 5.38393C9.88 5.50397 9.81 5.614 9.71 5.71404L6.71 8.71501C6.51 8.91508 6.26 9.00511 6 9.00511C5.74 9.00511 5.49 8.90508 5.29 8.71501C4.9 8.32489 4.9 7.69468 5.29 7.30456L6.58 6.01413H4.99C4.44 6.01413 3.99 5.56399 3.99 5.01381L4 4.9938ZM14.08 5.37393C14.13 5.49397 14.2 5.604 14.3 5.70403L17.3 8.70501C17.5 8.90508 17.75 8.99511 18.01 8.99511C18.27 8.99511 18.52 8.89507 18.72 8.70501C19.11 8.31488 19.11 7.68468 18.72 7.29455L17.43 6.00413H19.02C19.57 6.00413 20.02 5.55399 20.02 5.00381C20.02 4.45363 19.57 4.00348 19.02 4.00348H17.43L18.72 2.71306C19.11 2.32293 19.11 1.69273 18.72 1.3026C18.33 0.912471 17.7 0.912471 17.31 1.3026L14.31 4.30358C14.22 4.39361 14.14 4.50364 14.09 4.63368C13.99 4.87376 13.99 5.15385 14.09 5.39393L14.08 5.37393ZM22 14.9971V20.999C22 22.6496 20.65 24 19 24H5C3.35 24 2 22.6496 2 20.999V14.9971C2 13.3465 3.35 11.9961 5 11.9961H19C20.65 11.9961 22 13.3465 22 14.9971ZM19 13.9967H16V16.9977H20V14.9971C20 14.4469 19.55 13.9967 19 13.9967ZM14 16.9977V13.9967H10V16.9977H14ZM10 18.9984V21.9993H14V18.9984H10ZM4 14.9971V16.9977H8V13.9967H5C4.45 13.9967 4 14.4469 4 14.9971ZM5 21.9993H8V18.9984H4V20.999C4 21.5492 4.45 21.9993 5 21.9993ZM20 20.999V18.9984H16V21.9993H19C19.55 21.9993 20 21.5492 20 20.999Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate10-24x24.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate10-24x24.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 23C6.85721 23 1.15412 19.9621 0.0134987 13.1669C-0.0765501 12.6272 0.293651 12.1076 0.833944 12.0177C1.38424 11.9277 1.89452 12.2975 1.98457 12.8371C2.92508 18.4732 7.69767 20.9914 12 20.9914C16.3023 20.9914 21.0749 18.4732 22.0154 12.8371C22.1055 12.2975 22.6158 11.9277 23.1661 12.0177C23.7063 12.1076 24.0765 12.6272 23.9865 13.1669C22.8559 19.9521 17.1428 23 11.99 23H12.01ZM21.165 6.15177C22.3056 5.01257 22.3056 3.16386 21.165 2.02465L21.0049 1.85477C19.9143 0.765533 18.1633 0.725561 17.0227 1.71487C15.8821 0.715568 14.1312 0.765533 13.0406 1.85477L12.8705 2.01466C11.7299 3.15386 11.7299 5.00257 12.8705 6.14178L17.0227 10.2889L21.175 6.14178L21.165 6.15177ZM15.742 3.27378L17.0127 4.54289L18.2834 3.27378C18.6436 2.91403 19.2239 2.91403 19.5841 3.27378L19.7442 3.43367C20.1044 3.79342 20.1044 4.37301 19.7442 4.73276L17.0127 7.46086L14.2812 4.73276C13.921 4.37301 13.921 3.79342 14.2812 3.43367L14.4413 3.27378C14.6214 3.09391 14.8515 3.00397 15.0917 3.00397C15.3318 3.00397 15.5619 3.09391 15.742 3.27378ZM11.1595 6.15177C12.3002 5.01257 12.3002 3.16386 11.1595 2.02465L10.9995 1.85477C9.90886 0.765533 8.15792 0.725561 7.0173 1.71487C5.87668 0.715568 4.12573 0.765533 3.03514 1.85477L2.86505 2.01466C1.72443 3.15386 1.72443 5.00257 2.86505 6.14178L7.0173 10.2889L11.1695 6.14178L11.1595 6.15177ZM5.7366 3.27378L7.00729 4.54289L8.27798 3.27378C8.63818 2.91403 9.21849 2.91403 9.57869 3.27378L9.73877 3.43367C10.099 3.79342 10.099 4.37301 9.73877 4.73276L7.00729 7.46086L4.27581 4.73276C3.91562 4.37301 3.91562 3.79342 4.27581 3.43367L4.4359 3.27378C4.61599 3.09391 4.84612 3.00397 5.08625 3.00397C5.32638 3.00397 5.5565 3.09391 5.7366 3.27378Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate2-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate2-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><g clip-path=\"url(#clip0_15894_140103)\"><path d=\"M4.88291 4.51001C4.47291 4.51001 4.08291 4.25001 3.94291 3.84001C3.76291 3.32001 4.03291 2.75001 4.55291 2.57001L8.32291 1.25001C8.84291 1.06001 9.41291 1.34001 9.59291 1.86001C9.77291 2.38001 9.50291 2.95001 8.98291 3.13001L5.20291 4.45001C5.09291 4.49001 4.98291 4.51001 4.87291 4.51001H4.88291ZM19.8129 3.89001C20.0229 3.38001 19.7729 2.79001 19.2629 2.59001L15.5529 1.07001C15.0429 0.860007 14.4529 1.11001 14.2529 1.62001C14.0429 2.13001 14.2929 2.72001 14.8029 2.92001L18.5029 4.43001C18.6229 4.48001 18.7529 4.50001 18.8829 4.50001C19.2729 4.50001 19.6529 4.27001 19.8129 3.88001V3.89001ZM3.50291 6.00001C2.64291 6.37001 1.79291 6.88001 1.00291 7.48001C0.79291 7.64001 0.64291 7.87001 0.59291 8.14001C0.48291 8.73001 0.87291 9.29001 1.45291 9.40001C2.04291 9.51001 2.60291 9.12001 2.71291 8.54001C2.87291 7.69001 3.12291 6.83001 3.50291 5.99001V6.00001ZM21.0429 8.55001C21.6029 10.48 24.2429 8.84001 22.7529 7.48001C21.9629 6.88001 21.1129 6.37001 20.2529 6.00001C20.6329 6.84001 20.8829 7.70001 21.0429 8.55001ZM21.5729 13.2C21.2529 14.2 22.5429 15.09 23.3629 14.39C23.8529 14 23.9229 13.29 23.5429 12.81C21.7429 10.67 22.1329 10.55 21.5829 13.2H21.5729ZM1.75291 11C1.22291 11.79 -0.14709 12.64 0.0129102 13.75C0.15291 14.36 0.75291 14.74 1.35291 14.6C2.98291 14.1 1.80291 12.22 1.75291 11ZM19.8829 17C19.8829 13.14 16.2929 10 11.8829 10C7.47291 10 3.88291 13.14 3.88291 17C3.88291 20.86 7.47291 24 11.8829 24C16.2929 24 19.8829 20.86 19.8829 17ZM17.8829 17C17.8829 19.76 15.1929 22 11.8829 22C8.57291 22 5.88291 19.76 5.88291 17C5.88291 14.24 8.57291 12 11.8829 12C15.1929 12 17.8829 14.24 17.8829 17Z\"></path></g><defs><clipPath id=\"clip0_15894_140103\"><rect width=\"24\" height=\"24\" fill=\"white\"></rect></clipPath></defs></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate3-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate3-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.01915 7C6.46961 7 6.01998 6.55 6.01998 6V2C6.01998 1.45 6.46961 1 7.01915 1C7.56869 1 8.01832 1.45 8.01832 2V6C8.01832 6.55 7.56869 7 7.01915 7ZM18.01 6V2C18.01 1.45 17.5604 1 17.0108 1C16.4613 1 16.0117 1.45 16.0117 2V6C16.0117 6.55 16.4613 7 17.0108 7C17.5604 7 18.01 6.55 18.01 6ZM16.4213 21.58L18.01 19.99L19.2989 21.28C19.6886 21.67 20.3181 21.67 20.7077 21.28C21.0974 20.89 21.0974 20.26 20.7077 19.87L19.4188 18.58C18.6395 17.8 17.3705 17.8 16.5912 18.58L15.0025 20.17L13.4138 18.58C12.6345 17.8 11.3655 17.8 10.5862 18.58L8.9975 20.17L7.40883 18.58C6.62948 17.8 5.36053 17.8 4.58118 18.58L3.29226 19.87C2.90258 20.26 2.90258 20.89 3.29226 21.28C3.68193 21.67 4.31141 21.67 4.70108 21.28L5.99001 19.99L7.57868 21.58C8.35803 22.36 9.62698 22.36 10.4063 21.58L11.995 19.99L13.5837 21.58C13.9734 21.97 14.4829 22.16 14.9925 22.16C15.5021 22.16 16.0117 21.97 16.4013 21.58H16.4213Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate4-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate4-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.06927 7C6.51927 7 6.06927 6.55 6.06927 6V2C6.06927 1.45 6.51927 1 7.06927 1C7.61927 1 8.06927 1.45 8.06927 2V6C8.06927 6.55 7.61927 7 7.06927 7ZM18.0693 6V2C18.0693 1.45 17.6193 1 17.0693 1C16.5193 1 16.0693 1.45 16.0693 2V6C16.0693 6.55 16.5193 7 17.0693 7C17.6193 7 18.0693 6.55 18.0693 6ZM22.5693 21.9C23.0693 21.66 23.2793 21.07 23.0393 20.57C21.1093 16.52 16.9093 14 12.0693 14C7.22927 14 3.02927 16.52 1.09927 20.57C0.859273 21.07 1.06927 21.67 1.56927 21.9C2.06927 22.14 2.65927 21.93 2.89927 21.43C4.49927 18.08 8.00927 16 12.0593 16C16.1093 16 19.6293 18.08 21.2193 21.43C21.3893 21.79 21.7493 22 22.1193 22C22.2593 22 22.4093 21.97 22.5493 21.9H22.5693Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate5-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate5-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.00572 7C6.45572 7 6.00572 6.55 6.00572 6V2C6.00572 1.45 6.45572 1 7.00572 1C7.55572 1 8.00572 1.45 8.00572 2V6C8.00572 6.55 7.55572 7 7.00572 7ZM18.0057 6V2C18.0057 1.45 17.5557 1 17.0057 1C16.4557 1 16.0057 1.45 16.0057 2V6C16.0057 6.55 16.4557 7 17.0057 7C17.5557 7 18.0057 6.55 18.0057 6ZM19.9457 21.33C20.1257 20.81 19.8557 20.24 19.3357 20.05C14.5457 18.35 9.45572 18.35 4.66572 20.05C4.14572 20.23 3.87572 20.81 4.05572 21.33C4.23572 21.85 4.80572 22.12 5.33572 21.94C9.69572 20.4 14.3057 20.4 18.6657 21.94C18.7757 21.98 18.8857 22 18.9957 22C19.4057 22 19.7957 21.74 19.9357 21.33H19.9457Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate6-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate6-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7 7C6.45 7 6 6.55 6 6V2C6 1.45 6.45 1 7 1C7.55 1 8 1.45 8 2V6C8 6.55 7.55 7 7 7ZM18 6V2C18 1.45 17.55 1 17 1C16.45 1 16 1.45 16 2V6C16 6.55 16.45 7 17 7C17.55 7 18 6.55 18 6ZM21 21C21 20.45 20.55 20 20 20H4C3.45 20 3 20.45 3 21C3 21.55 3.45 22 4 22H20C20.55 22 21 21.55 21 21Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate7-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate7-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.0022 23.99C11.452 23.99 11.0018 23.5402 11.0018 22.9904C11.0018 22.4407 11.452 21.9909 12.0022 21.9909C16.3137 21.9909 21.0755 19.472 22.0158 13.8344C22.1058 13.2947 22.616 12.9248 23.1662 13.0148C23.7064 13.1047 24.0765 13.6245 23.9865 14.1643C22.8561 20.9513 17.144 24 11.9922 24L12.0022 23.99ZM8.00072 5.99783V1.99957C8.00072 1.4498 7.55056 1 7.00036 1C6.45016 1 6 1.4498 6 1.99957V5.99783C6 6.54759 6.45016 6.99739 7.00036 6.99739C7.55056 6.99739 8.00072 6.54759 8.00072 5.99783ZM18.0043 5.99783V1.99957C18.0043 1.4498 17.5542 1 17.004 1C16.4538 1 16.0036 1.4498 16.0036 1.99957V5.99783C16.0036 6.54759 16.4538 6.99739 17.004 6.99739C17.5542 6.99739 18.0043 6.54759 18.0043 5.99783Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate8-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate8-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 24C6.85721 24 1.15412 20.96 0.0134987 14.16C-0.0765501 13.62 0.293651 13.1 0.833944 13.01C1.38424 12.92 1.89452 13.29 1.98457 13.83C2.92508 19.47 7.69767 21.99 12 21.99C16.3023 21.99 21.0749 19.47 22.0154 13.83C22.1055 13.29 22.6158 12.92 23.1661 13.01C23.7063 13.1 24.0765 13.62 23.9865 14.16C22.8559 20.95 17.1428 24 11.99 24H12.01ZM8.00783 6V2C8.00783 1.45 7.55759 1 7.00729 1C6.45699 1 6.00675 1.45 6.00675 2V6C6.00675 6.55 6.45699 7 7.00729 7C7.55759 7 8.00783 6.55 8.00783 6ZM18.0133 6V2C18.0133 1.45 17.563 1 17.0127 1C16.4624 1 16.0122 1.45 16.0122 2V6C16.0122 6.55 16.4624 7 17.0127 7C17.563 7 18.0133 6.55 18.0133 6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v1/smiley-rate9-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v1/smiley-rate9-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 24C6.85767 24 1.15509 20.96 0.0145752 14.16C-0.0354475 13.87 0.0445888 13.57 0.234675 13.35C0.424761 13.13 0.704888 13 0.995019 13H23.005C23.2951 13 23.5752 13.13 23.7653 13.35C23.9554 13.57 24.0354 13.87 23.9854 14.16C22.8549 20.95 17.1423 24 11.99 24H12.01ZM2.25559 15C3.61621 19.82 8.0182 22 12.01 22C16.0018 22 20.4038 19.82 21.7644 15H2.25559ZM8.00819 6V2C8.00819 1.45 7.55799 1 7.00774 1C6.45749 1 6.00729 1.45 6.00729 2V6C6.00729 6.55 6.45749 7 7.00774 7C7.55799 7 8.00819 6.55 8.00819 6ZM18.0127 6V2C18.0127 1.45 17.5625 1 17.0123 1C16.462 1 16.0118 1.45 16.0118 2V6C16.0118 6.55 16.462 7 17.0123 7C17.5625 7 18.0127 6.55 18.0127 6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2 sync recursive \\.svg$":
/*!********************************************************!*\
  !*** ./packages/survey-core/src/images-v2 sync \.svg$ ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"./ModernBooleanCheckChecked.svg": "./packages/survey-core/src/images-v2/ModernBooleanCheckChecked.svg",
	"./ModernBooleanCheckInd.svg": "./packages/survey-core/src/images-v2/ModernBooleanCheckInd.svg",
	"./ModernBooleanCheckUnchecked.svg": "./packages/survey-core/src/images-v2/ModernBooleanCheckUnchecked.svg",
	"./ModernCheck.svg": "./packages/survey-core/src/images-v2/ModernCheck.svg",
	"./ModernRadio.svg": "./packages/survey-core/src/images-v2/ModernRadio.svg",
	"./ProgressButton.svg": "./packages/survey-core/src/images-v2/ProgressButton.svg",
	"./RemoveFile.svg": "./packages/survey-core/src/images-v2/RemoveFile.svg",
	"./TimerCircle.svg": "./packages/survey-core/src/images-v2/TimerCircle.svg",
	"./add-24x24.svg": "./packages/survey-core/src/images-v2/add-24x24.svg",
	"./arrowleft-16x16.svg": "./packages/survey-core/src/images-v2/arrowleft-16x16.svg",
	"./arrowright-16x16.svg": "./packages/survey-core/src/images-v2/arrowright-16x16.svg",
	"./camera-24x24.svg": "./packages/survey-core/src/images-v2/camera-24x24.svg",
	"./camera-32x32.svg": "./packages/survey-core/src/images-v2/camera-32x32.svg",
	"./cancel-24x24.svg": "./packages/survey-core/src/images-v2/cancel-24x24.svg",
	"./check-16x16.svg": "./packages/survey-core/src/images-v2/check-16x16.svg",
	"./check-24x24.svg": "./packages/survey-core/src/images-v2/check-24x24.svg",
	"./chevrondown-24x24.svg": "./packages/survey-core/src/images-v2/chevrondown-24x24.svg",
	"./chevronright-16x16.svg": "./packages/survey-core/src/images-v2/chevronright-16x16.svg",
	"./clear-16x16.svg": "./packages/survey-core/src/images-v2/clear-16x16.svg",
	"./clear-24x24.svg": "./packages/survey-core/src/images-v2/clear-24x24.svg",
	"./close-16x16.svg": "./packages/survey-core/src/images-v2/close-16x16.svg",
	"./close-24x24.svg": "./packages/survey-core/src/images-v2/close-24x24.svg",
	"./collapse-16x16.svg": "./packages/survey-core/src/images-v2/collapse-16x16.svg",
	"./collapsedetails-16x16.svg": "./packages/survey-core/src/images-v2/collapsedetails-16x16.svg",
	"./delete-24x24.svg": "./packages/survey-core/src/images-v2/delete-24x24.svg",
	"./drag-24x24.svg": "./packages/survey-core/src/images-v2/drag-24x24.svg",
	"./draghorizontal-24x16.svg": "./packages/survey-core/src/images-v2/draghorizontal-24x16.svg",
	"./expand-16x16.svg": "./packages/survey-core/src/images-v2/expand-16x16.svg",
	"./expanddetails-16x16.svg": "./packages/survey-core/src/images-v2/expanddetails-16x16.svg",
	"./file-72x72.svg": "./packages/survey-core/src/images-v2/file-72x72.svg",
	"./flip-24x24.svg": "./packages/survey-core/src/images-v2/flip-24x24.svg",
	"./folder-24x24.svg": "./packages/survey-core/src/images-v2/folder-24x24.svg",
	"./fullsize-16x16.svg": "./packages/survey-core/src/images-v2/fullsize-16x16.svg",
	"./image-48x48.svg": "./packages/survey-core/src/images-v2/image-48x48.svg",
	"./loading-48x48.svg": "./packages/survey-core/src/images-v2/loading-48x48.svg",
	"./maximize-16x16.svg": "./packages/survey-core/src/images-v2/maximize-16x16.svg",
	"./minimize-16x16.svg": "./packages/survey-core/src/images-v2/minimize-16x16.svg",
	"./more-24x24.svg": "./packages/survey-core/src/images-v2/more-24x24.svg",
	"./navmenu-24x24.svg": "./packages/survey-core/src/images-v2/navmenu-24x24.svg",
	"./noimage-48x48.svg": "./packages/survey-core/src/images-v2/noimage-48x48.svg",
	"./ranking-arrows.svg": "./packages/survey-core/src/images-v2/ranking-arrows.svg",
	"./rankingundefined-16x16.svg": "./packages/survey-core/src/images-v2/rankingundefined-16x16.svg",
	"./rating-star-2.svg": "./packages/survey-core/src/images-v2/rating-star-2.svg",
	"./rating-star-small-2.svg": "./packages/survey-core/src/images-v2/rating-star-small-2.svg",
	"./rating-star-small.svg": "./packages/survey-core/src/images-v2/rating-star-small.svg",
	"./rating-star.svg": "./packages/survey-core/src/images-v2/rating-star.svg",
	"./reorder-24x24.svg": "./packages/survey-core/src/images-v2/reorder-24x24.svg",
	"./restoredown-16x16.svg": "./packages/survey-core/src/images-v2/restoredown-16x16.svg",
	"./search-24x24.svg": "./packages/survey-core/src/images-v2/search-24x24.svg",
	"./smiley-rate1-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate1-24x24.svg",
	"./smiley-rate10-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate10-24x24.svg",
	"./smiley-rate2-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate2-24x24.svg",
	"./smiley-rate3-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate3-24x24.svg",
	"./smiley-rate4-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate4-24x24.svg",
	"./smiley-rate5-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate5-24x24.svg",
	"./smiley-rate6-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate6-24x24.svg",
	"./smiley-rate7-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate7-24x24.svg",
	"./smiley-rate8-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate8-24x24.svg",
	"./smiley-rate9-24x24.svg": "./packages/survey-core/src/images-v2/smiley-rate9-24x24.svg"
};


function webpackContext(req) {
	var id = webpackContextResolve(req);
	return __webpack_require__(id);
}
function webpackContextResolve(req) {
	if(!__webpack_require__.o(map, req)) {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	}
	return map[req];
}
webpackContext.keys = function webpackContextKeys() {
	return Object.keys(map);
};
webpackContext.resolve = webpackContextResolve;
module.exports = webpackContext;
webpackContext.id = "./packages/survey-core/src/images-v2 sync recursive \\.svg$";

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ModernBooleanCheckChecked.svg":
/*!**************************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ModernBooleanCheckChecked.svg ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><polygon points=\"19,10 14,10 14,5 10,5 10,10 5,10 5,14 10,14 10,19 14,19 14,14 19,14 \"></polygon></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ModernBooleanCheckInd.svg":
/*!**********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ModernBooleanCheckInd.svg ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><path d=\"M22,0H2C0.9,0,0,0.9,0,2v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V2C24,0.9,23.1,0,22,0z M21,18L6,3h15V18z M3,6l15,15H3V6z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ModernBooleanCheckUnchecked.svg":
/*!****************************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ModernBooleanCheckUnchecked.svg ***!
  \****************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\"><rect x=\"5\" y=\"10\" width=\"14\" height=\"4\"></rect></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ModernCheck.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ModernCheck.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\"><path d=\"M5,13l2-2l3,3l7-7l2,2l-9,9L5,13z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ModernRadio.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ModernRadio.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"-12 -12 24 24\"><circle r=\"6\" cx=\"0\" cy=\"0\"></circle></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ProgressButton.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ProgressButton.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 10 10\"><polygon points=\"2,2 0,4 5,9 10,4 8,2 5,5 \"></polygon></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/RemoveFile.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/RemoveFile.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\"><path d=\"M8,2C4.7,2,2,4.7,2,8s2.7,6,6,6s6-2.7,6-6S11.3,2,8,2z M11,10l-1,1L8,9l-2,2l-1-1l2-2L5,6l1-1l2,2l2-2l1,1L9,8 L11,10z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/TimerCircle.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/TimerCircle.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" viewBox=\"0 0 160 160\"><circle cx=\"80\" cy=\"80\" r=\"70\" style=\"stroke: var(--sd-timer-stroke-background-color); stroke-width: var(--sd-timer-stroke-background-width)\" stroke-dasharray=\"none\" stroke-dashoffset=\"none\"></circle><circle cx=\"80\" cy=\"80\" r=\"70\"></circle></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/add-24x24.svg":
/*!**********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/add-24x24.svg ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M15.75 12C15.75 12.41 15.41 12.75 15 12.75H12.75V15C12.75 15.41 12.41 15.75 12 15.75C11.59 15.75 11.25 15.41 11.25 15V12.75H9C8.59 12.75 8.25 12.41 8.25 12C8.25 11.59 8.59 11.25 9 11.25H11.25V9C11.25 8.59 11.59 8.25 12 8.25C12.41 8.25 12.75 8.59 12.75 9V11.25H15C15.41 11.25 15.75 11.59 15.75 12ZM21.75 12C21.75 17.38 17.38 21.75 12 21.75C6.62 21.75 2.25 17.38 2.25 12C2.25 6.62 6.62 2.25 12 2.25C17.38 2.25 21.75 6.62 21.75 12ZM20.25 12C20.25 7.45 16.55 3.75 12 3.75C7.45 3.75 3.75 7.45 3.75 12C3.75 16.55 7.45 20.25 12 20.25C16.55 20.25 20.25 16.55 20.25 12Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/arrowleft-16x16.svg":
/*!****************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/arrowleft-16x16.svg ***!
  \****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14.7475 7.9975C14.7475 8.4075 14.4075 8.7475 13.9975 8.7475H3.8075L7.5275 12.4675C7.8175 12.7575 7.8175 13.2375 7.5275 13.5275C7.3775 13.6775 7.1875 13.7475 6.9975 13.7475C6.8075 13.7475 6.6175 13.6775 6.4675 13.5275L1.4675 8.5275C1.1775 8.2375 1.1775 7.7575 1.4675 7.4675L6.4675 2.4675C6.7575 2.1775 7.2375 2.1775 7.5275 2.4675C7.8175 2.7575 7.8175 3.2375 7.5275 3.5275L3.8075 7.2475H13.9975C14.4075 7.2475 14.7475 7.5875 14.7475 7.9975Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/arrowright-16x16.svg":
/*!*****************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/arrowright-16x16.svg ***!
  \*****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14.53 8.5275L9.53 13.5275C9.38 13.6775 9.19 13.7475 9 13.7475C8.81 13.7475 8.62 13.6775 8.47 13.5275C8.18 13.2375 8.18 12.7575 8.47 12.4675L12.19 8.7475H2C1.59 8.7475 1.25 8.4075 1.25 7.9975C1.25 7.5875 1.59 7.2475 2 7.2475H12.19L8.47 3.5275C8.18 3.2375 8.18 2.7575 8.47 2.4675C8.76 2.1775 9.24 2.1775 9.53 2.4675L14.53 7.4675C14.82 7.7575 14.82 8.2375 14.53 8.5275Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/camera-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/camera-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M19.19 4.25H17.12C16.72 4.25 16.35 4.03 16.17 3.67C15.73 2.8 14.86 2.25 13.88 2.25H10.12C9.14 2.25 8.27 2.79 7.83 3.67C7.65 4.03 7.29 4.25 6.88 4.25H4.81C3.4 4.25 2.25 5.4 2.25 6.81V18.19C2.25 19.6 3.4 20.75 4.81 20.75H19.19C20.6 20.75 21.75 19.6 21.75 18.19V6.81C21.75 5.4 20.6 4.25 19.19 4.25ZM20.25 18.19C20.25 18.77 19.78 19.25 19.19 19.25H4.81C4.23 19.25 3.75 18.78 3.75 18.19V6.81C3.75 6.23 4.22 5.75 4.81 5.75H6.88C7.86 5.75 8.73 5.21 9.17 4.33C9.35 3.97 9.71 3.75 10.12 3.75H13.88C14.28 3.75 14.65 3.97 14.83 4.33C15.27 5.2 16.14 5.75 17.12 5.75H19.19C19.77 5.75 20.25 6.22 20.25 6.81V18.19ZM12 6.25C8.83 6.25 6.25 8.83 6.25 12C6.25 15.17 8.83 17.75 12 17.75C15.17 17.75 17.75 15.17 17.75 12C17.75 8.83 15.17 6.25 12 6.25ZM12 16.25C9.66 16.25 7.75 14.34 7.75 12C7.75 9.66 9.66 7.75 12 7.75C14.34 7.75 16.25 9.66 16.25 12C16.25 14.34 14.34 16.25 12 16.25ZM14.75 12C14.75 13.52 13.52 14.75 12 14.75C11.59 14.75 11.25 14.41 11.25 14C11.25 13.59 11.59 13.25 12 13.25C12.69 13.25 13.25 12.69 13.25 12C13.25 11.59 13.59 11.25 14 11.25C14.41 11.25 14.75 11.59 14.75 12Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/camera-32x32.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/camera-32x32.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 32 32\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M25 7.25H22.19C21.73 7.25 21.31 7 21.09 6.59L20.89 6.22C20.23 5.01 18.97 4.25 17.59 4.25H14.41C13.03 4.25 11.77 5 11.11 6.22L10.91 6.6C10.69 7 10.27 7.26 9.81 7.26H7C4.93 7.26 3.25 8.94 3.25 11.01V24.01C3.25 26.08 4.93 27.76 7 27.76H25C27.07 27.76 28.75 26.08 28.75 24.01V11C28.75 8.93 27.07 7.25 25 7.25ZM27.25 24C27.25 25.24 26.24 26.25 25 26.25H7C5.76 26.25 4.75 25.24 4.75 24V11C4.75 9.76 5.76 8.75 7 8.75H9.81C10.82 8.75 11.75 8.2 12.23 7.31L12.43 6.94C12.82 6.21 13.58 5.76 14.41 5.76H17.59C18.42 5.76 19.18 6.21 19.57 6.94L19.77 7.31C20.25 8.2 21.18 8.76 22.19 8.76H25C26.24 8.76 27.25 9.77 27.25 11.01V24.01V24ZM16 10.25C12.28 10.25 9.25 13.28 9.25 17C9.25 20.72 12.28 23.75 16 23.75C19.72 23.75 22.75 20.72 22.75 17C22.75 13.28 19.72 10.25 16 10.25ZM16 22.25C13.11 22.25 10.75 19.89 10.75 17C10.75 14.11 13.11 11.75 16 11.75C18.89 11.75 21.25 14.11 21.25 17C21.25 19.89 18.89 22.25 16 22.25ZM19.75 17C19.75 19.07 18.07 20.75 16 20.75C15.59 20.75 15.25 20.41 15.25 20C15.25 19.59 15.59 19.25 16 19.25C17.24 19.25 18.25 18.24 18.25 17C18.25 16.59 18.59 16.25 19 16.25C19.41 16.25 19.75 16.59 19.75 17Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/cancel-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/cancel-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.8099 11.75L15.2799 9.28C15.5699 8.99 15.5699 8.51 15.2799 8.22C14.9899 7.93 14.5099 7.93 14.2199 8.22L11.7499 10.69L9.27994 8.22C8.98994 7.93 8.50994 7.93 8.21994 8.22C7.92994 8.51 7.92994 8.99 8.21994 9.28L10.6899 11.75L8.21994 14.22C7.92994 14.51 7.92994 14.99 8.21994 15.28C8.36994 15.43 8.55994 15.5 8.74994 15.5C8.93994 15.5 9.12994 15.43 9.27994 15.28L11.7499 12.81L14.2199 15.28C14.3699 15.43 14.5599 15.5 14.7499 15.5C14.9399 15.5 15.1299 15.43 15.2799 15.28C15.5699 14.99 15.5699 14.51 15.2799 14.22L12.8099 11.75Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/check-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/check-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14.0275 5.0275L6.5275 12.5275C6.3775 12.6775 6.1875 12.7475 5.9975 12.7475C5.8075 12.7475 5.6175 12.6775 5.4675 12.5275L2.4675 9.5275C2.1775 9.2375 2.1775 8.7575 2.4675 8.4675C2.7575 8.1775 3.2375 8.1775 3.5275 8.4675L5.9975 10.9375L12.9675 3.9675C13.2575 3.6775 13.7375 3.6775 14.0275 3.9675C14.3175 4.2575 14.3175 4.7375 14.0275 5.0275Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/check-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/check-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M19.5275 7.5275L9.5275 17.5275C9.3775 17.6775 9.1875 17.7475 8.9975 17.7475C8.8075 17.7475 8.6175 17.6775 8.4675 17.5275L4.4675 13.5275C4.1775 13.2375 4.1775 12.7575 4.4675 12.4675C4.7575 12.1775 5.2375 12.1775 5.5275 12.4675L8.9975 15.9375L18.4675 6.4675C18.7575 6.1775 19.2375 6.1775 19.5275 6.4675C19.8175 6.7575 19.8175 7.2375 19.5275 7.5275Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/chevrondown-24x24.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/chevrondown-24x24.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M16.5275 10.5275L12.5275 14.5275C12.3775 14.6775 12.1875 14.7475 11.9975 14.7475C11.8075 14.7475 11.6175 14.6775 11.4675 14.5275L7.4675 10.5275C7.1775 10.2375 7.1775 9.7575 7.4675 9.4675C7.7575 9.1775 8.2375 9.1775 8.5275 9.4675L11.9975 12.9375L15.4675 9.4675C15.7575 9.1775 16.2375 9.1775 16.5275 9.4675C16.8175 9.7575 16.8175 10.2375 16.5275 10.5275Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/chevronright-16x16.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/chevronright-16x16.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.35 8.34627L7.35 12.3463C7.25 12.4463 7.12 12.4963 7 12.4963C6.88 12.4963 6.74 12.4463 6.65 12.3463C6.45 12.1463 6.45 11.8363 6.65 11.6363L10.3 7.98627L6.65 4.34627C6.45 4.15627 6.45 3.83627 6.65 3.64627C6.85 3.45627 7.16 3.44627 7.35 3.64627L11.35 7.64627C11.55 7.84627 11.55 8.15627 11.35 8.35627V8.34627Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/clear-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/clear-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.35 11.65C12.55 11.85 12.55 12.16 12.35 12.36C12.25 12.46 12.12 12.51 12 12.51C11.88 12.51 11.74 12.46 11.65 12.36L8 8.71L4.35 12.36C4.25 12.46 4.12 12.51 4 12.51C3.88 12.51 3.74 12.46 3.65 12.36C3.45 12.16 3.45 11.85 3.65 11.65L7.3 8L3.65 4.35C3.45 4.16 3.45 3.84 3.65 3.65C3.85 3.46 4.16 3.45 4.35 3.65L8 7.3L11.65 3.65C11.85 3.45 12.16 3.45 12.36 3.65C12.56 3.85 12.56 4.16 12.36 4.36L8.71 8.01L12.36 11.66L12.35 11.65Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/clear-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/clear-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M20.12 10.9325C20.64 10.4125 20.93 9.7225 20.93 8.9925C20.93 8.2625 20.64 7.5725 20.12 7.0525L16.95 3.8825C15.88 2.8125 14.13 2.8125 13.06 3.8825L3.88 13.0525C3.36 13.5725 3.07 14.2625 3.07 14.9925C3.07 15.7225 3.36 16.4125 3.88 16.9325L5.64 18.6925C6.57 19.6225 7.78 20.0825 9 20.0825C10.22 20.0825 11.43 19.6225 12.36 18.6925L20.12 10.9325ZM14.12 4.9325C14.36 4.6925 14.67 4.5625 15 4.5625C15.33 4.5625 15.65 4.6925 15.88 4.9325L19.05 8.1025C19.54 8.5925 19.54 9.3825 19.05 9.8725L12.99 15.9325L8.05 10.9925L14.12 4.9325ZM6.7 17.6325L4.94 15.8725C4.45 15.3825 4.45 14.5925 4.94 14.1025L7 12.0425L11.94 16.9825L11.3 17.6225C10.07 18.8525 7.93 18.8525 6.7 17.6225V17.6325ZM22.75 20.9925C22.75 21.4025 22.41 21.7425 22 21.7425H14C13.59 21.7425 13.25 21.4025 13.25 20.9925C13.25 20.5825 13.59 20.2425 14 20.2425H22C22.41 20.2425 22.75 20.5825 22.75 20.9925ZM4.75 20.9925C4.75 21.4025 4.41 21.7425 4 21.7425H2C1.59 21.7425 1.25 21.4025 1.25 20.9925C1.25 20.5825 1.59 20.2425 2 20.2425H4C4.41 20.2425 4.75 20.5825 4.75 20.9925Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/close-16x16.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/close-16x16.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.5275 12.4675C13.8175 12.7575 13.8175 13.2375 13.5275 13.5275C13.3775 13.6775 13.1875 13.7475 12.9975 13.7475C12.8075 13.7475 12.6175 13.6775 12.4675 13.5275L7.9975 9.0575L3.5275 13.5275C3.3775 13.6775 3.1875 13.7475 2.9975 13.7475C2.8075 13.7475 2.6175 13.6775 2.4675 13.5275C2.1775 13.2375 2.1775 12.7575 2.4675 12.4675L6.9375 7.9975L2.4675 3.5275C2.1775 3.2375 2.1775 2.7575 2.4675 2.4675C2.7575 2.1775 3.2375 2.1775 3.5275 2.4675L7.9975 6.9375L12.4675 2.4675C12.7575 2.1775 13.2375 2.1775 13.5275 2.4675C13.8175 2.7575 13.8175 3.2375 13.5275 3.5275L9.0575 7.9975L13.5275 12.4675Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/close-24x24.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/close-24x24.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M19.5275 18.4675C19.8175 18.7575 19.8175 19.2375 19.5275 19.5275C19.3775 19.6775 19.1875 19.7475 18.9975 19.7475C18.8075 19.7475 18.6175 19.6775 18.4675 19.5275L11.9975 13.0575L5.5275 19.5275C5.3775 19.6775 5.1875 19.7475 4.9975 19.7475C4.8075 19.7475 4.6175 19.6775 4.4675 19.5275C4.1775 19.2375 4.1775 18.7575 4.4675 18.4675L10.9375 11.9975L4.4675 5.5275C4.1775 5.2375 4.1775 4.7575 4.4675 4.4675C4.7575 4.1775 5.2375 4.1775 5.5275 4.4675L11.9975 10.9375L18.4675 4.4675C18.7575 4.1775 19.2375 4.1775 19.5275 4.4675C19.8175 4.7575 19.8175 5.2375 19.5275 5.5275L13.0575 11.9975L19.5275 18.4675Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/collapse-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/collapse-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.75 8C11.75 8.41 11.41 8.75 11 8.75H5C4.59 8.75 4.25 8.41 4.25 8C4.25 7.59 4.59 7.25 5 7.25H11C11.41 7.25 11.75 7.59 11.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/collapsedetails-16x16.svg":
/*!**********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/collapsedetails-16x16.svg ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.75 8C11.75 8.41 11.41 8.75 11 8.75H5C4.59 8.75 4.25 8.41 4.25 8C4.25 7.59 4.59 7.25 5 7.25H11C11.41 7.25 11.75 7.59 11.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/delete-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/delete-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.75 9V17C12.75 17.41 12.41 17.75 12 17.75C11.59 17.75 11.25 17.41 11.25 17V9C11.25 8.59 11.59 8.25 12 8.25C12.41 8.25 12.75 8.59 12.75 9ZM14.25 9V17C14.25 17.41 14.59 17.75 15 17.75C15.41 17.75 15.75 17.41 15.75 17V9C15.75 8.59 15.41 8.25 15 8.25C14.59 8.25 14.25 8.59 14.25 9ZM9 8.25C8.59 8.25 8.25 8.59 8.25 9V17C8.25 17.41 8.59 17.75 9 17.75C9.41 17.75 9.75 17.41 9.75 17V9C9.75 8.59 9.41 8.25 9 8.25ZM20.75 6C20.75 6.41 20.41 6.75 20 6.75H18.75V18C18.75 19.52 17.52 20.75 16 20.75H8C6.48 20.75 5.25 19.52 5.25 18V6.75H4C3.59 6.75 3.25 6.41 3.25 6C3.25 5.59 3.59 5.25 4 5.25H8.25V4C8.25 3.04 9.04 2.25 10 2.25H14C14.96 2.25 15.75 3.04 15.75 4V5.25H20C20.41 5.25 20.75 5.59 20.75 6ZM9.75 5.25H14.25V4C14.25 3.86 14.14 3.75 14 3.75H10C9.86 3.75 9.75 3.86 9.75 4V5.25ZM17.25 6.75H6.75V18C6.75 18.69 7.31 19.25 8 19.25H16C16.69 19.25 17.25 18.69 17.25 18V6.75Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/drag-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/drag-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14.5 8.75C15.19 8.75 15.75 8.19 15.75 7.5C15.75 6.81 15.19 6.25 14.5 6.25C13.81 6.25 13.25 6.81 13.25 7.5C13.25 8.19 13.81 8.75 14.5 8.75ZM14.5 7.25C14.64 7.25 14.75 7.36 14.75 7.5C14.75 7.78 14.25 7.78 14.25 7.5C14.25 7.36 14.36 7.25 14.5 7.25ZM9.5 6.25C8.81 6.25 8.25 6.81 8.25 7.5C8.25 8.19 8.81 8.75 9.5 8.75C10.19 8.75 10.75 8.19 10.75 7.5C10.75 6.81 10.19 6.25 9.5 6.25ZM9.25 7.5C9.25 7.36 9.36 7.25 9.5 7.25C9.64 7.25 9.75 7.36 9.75 7.5C9.75 7.78 9.25 7.78 9.25 7.5ZM14.5 11.25C13.81 11.25 13.25 11.81 13.25 12.5C13.25 13.19 13.81 13.75 14.5 13.75C15.19 13.75 15.75 13.19 15.75 12.5C15.75 11.81 15.19 11.25 14.5 11.25ZM14.25 12.5C14.25 12.36 14.36 12.25 14.5 12.25C14.64 12.25 14.75 12.36 14.75 12.5C14.75 12.78 14.25 12.78 14.25 12.5ZM9.5 11.25C8.81 11.25 8.25 11.81 8.25 12.5C8.25 13.19 8.81 13.75 9.5 13.75C10.19 13.75 10.75 13.19 10.75 12.5C10.75 11.81 10.19 11.25 9.5 11.25ZM9.25 12.5C9.25 12.36 9.36 12.25 9.5 12.25C9.64 12.25 9.75 12.36 9.75 12.5C9.75 12.78 9.25 12.78 9.25 12.5ZM14.5 16.25C13.81 16.25 13.25 16.81 13.25 17.5C13.25 18.19 13.81 18.75 14.5 18.75C15.19 18.75 15.75 18.19 15.75 17.5C15.75 16.81 15.19 16.25 14.5 16.25ZM14.25 17.5C14.25 17.36 14.36 17.25 14.5 17.25C14.64 17.25 14.75 17.36 14.75 17.5C14.75 17.78 14.25 17.78 14.25 17.5ZM9.5 16.25C8.81 16.25 8.25 16.81 8.25 17.5C8.25 18.19 8.81 18.75 9.5 18.75C10.19 18.75 10.75 18.19 10.75 17.5C10.75 16.81 10.19 16.25 9.5 16.25ZM9.25 17.5C9.25 17.36 9.36 17.25 9.5 17.25C9.64 17.25 9.75 17.36 9.75 17.5C9.75 17.78 9.25 17.78 9.25 17.5Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/draghorizontal-24x16.svg":
/*!*********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/draghorizontal-24x16.svg ***!
  \*********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M17.5 9.25C16.81 9.25 16.25 9.81 16.25 10.5C16.25 11.19 16.81 11.75 17.5 11.75C18.19 11.75 18.75 11.19 18.75 10.5C18.75 9.81 18.19 9.25 17.5 9.25ZM17.25 10.5C17.25 10.36 17.36 10.25 17.5 10.25C17.64 10.25 17.75 10.36 17.75 10.5C17.75 10.78 17.25 10.78 17.25 10.5ZM17.5 6.75C18.19 6.75 18.75 6.19 18.75 5.5C18.75 4.81 18.19 4.25 17.5 4.25C16.81 4.25 16.25 4.81 16.25 5.5C16.25 6.19 16.81 6.75 17.5 6.75ZM17.5 5.25C17.64 5.25 17.75 5.36 17.75 5.5C17.75 5.78 17.25 5.78 17.25 5.5C17.25 5.36 17.36 5.25 17.5 5.25ZM12.5 9.25C11.81 9.25 11.25 9.81 11.25 10.5C11.25 11.19 11.81 11.75 12.5 11.75C13.19 11.75 13.75 11.19 13.75 10.5C13.75 9.81 13.19 9.25 12.5 9.25ZM12.25 10.5C12.25 10.36 12.36 10.25 12.5 10.25C12.64 10.25 12.75 10.36 12.75 10.5C12.75 10.78 12.25 10.78 12.25 10.5ZM12.5 4.25C11.81 4.25 11.25 4.81 11.25 5.5C11.25 6.19 11.81 6.75 12.5 6.75C13.19 6.75 13.75 6.19 13.75 5.5C13.75 4.81 13.19 4.25 12.5 4.25ZM12.25 5.5C12.25 5.36 12.36 5.25 12.5 5.25C12.64 5.25 12.75 5.36 12.75 5.5C12.75 5.78 12.25 5.78 12.25 5.5ZM7.5 9.25C6.81 9.25 6.25 9.81 6.25 10.5C6.25 11.19 6.81 11.75 7.5 11.75C8.19 11.75 8.75 11.19 8.75 10.5C8.75 9.81 8.19 9.25 7.5 9.25ZM7.25 10.5C7.25 10.36 7.36 10.25 7.5 10.25C7.64 10.25 7.75 10.36 7.75 10.5C7.75 10.78 7.25 10.78 7.25 10.5ZM7.5 4.25C6.81 4.25 6.25 4.81 6.25 5.5C6.25 6.19 6.81 6.75 7.5 6.75C8.19 6.75 8.75 6.19 8.75 5.5C8.75 4.81 8.19 4.25 7.5 4.25ZM7.25 5.5C7.25 5.36 7.36 5.25 7.5 5.25C7.64 5.25 7.75 5.36 7.75 5.5C7.75 5.78 7.25 5.78 7.25 5.5Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/expand-16x16.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/expand-16x16.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.75 8C11.75 8.41 11.41 8.75 11 8.75H8.75V11C8.75 11.41 8.41 11.75 8 11.75C7.59 11.75 7.25 11.41 7.25 11V8.75H5C4.59 8.75 4.25 8.41 4.25 8C4.25 7.59 4.59 7.25 5 7.25H7.25V5C7.25 4.59 7.59 4.25 8 4.25C8.41 4.25 8.75 4.59 8.75 5V7.25H11C11.41 7.25 11.75 7.59 11.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/expanddetails-16x16.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/expanddetails-16x16.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.75 8C11.75 8.41 11.41 8.75 11 8.75H8.75V11C8.75 11.41 8.41 11.75 8 11.75C7.59 11.75 7.25 11.41 7.25 11V8.75H5C4.59 8.75 4.25 8.41 4.25 8C4.25 7.59 4.59 7.25 5 7.25H7.25V5C7.25 4.59 7.59 4.25 8 4.25C8.41 4.25 8.75 4.59 8.75 5V7.25H11C11.41 7.25 11.75 7.59 11.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/file-72x72.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/file-72x72.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 72 72\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M62.83 12.83L53.17 3.17C52.7982 2.79866 52.357 2.50421 51.8714 2.30346C51.3858 2.1027 50.8654 1.99959 50.34 2H14C12.4087 2 10.8826 2.63214 9.75735 3.75736C8.63214 4.88258 8 6.4087 8 8V64C8 65.5913 8.63214 67.1174 9.75735 68.2426C10.8826 69.3679 12.4087 70 14 70H58C59.5913 70 61.1174 69.3679 62.2426 68.2426C63.3679 67.1174 64 65.5913 64 64V15.66C64.0004 15.1346 63.8973 14.6142 63.6965 14.1286C63.4958 13.643 63.2013 13.2018 62.83 12.83ZM52 4.83L61.17 14H56C54.9391 14 53.9217 13.5786 53.1716 12.8284C52.4214 12.0783 52 11.0609 52 10V4.83ZM62 64C62 65.0609 61.5786 66.0783 60.8284 66.8284C60.0783 67.5786 59.0609 68 58 68H14C12.9391 68 11.9217 67.5786 11.1716 66.8284C10.4214 66.0783 10 65.0609 10 64V8C10 6.93914 10.4214 5.92172 11.1716 5.17157C11.9217 4.42143 12.9391 4 14 4H50V10C50 11.5913 50.6321 13.1174 51.7574 14.2426C52.8826 15.3679 54.4087 16 56 16H62V64ZM22 26H50V28H22V26ZM22 32H50V34H22V32ZM22 38H50V40H22V38ZM22 44H50V46H22V44Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/flip-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/flip-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14.53 17.4775C14.82 17.7675 14.82 18.2475 14.53 18.5375L11.53 21.5375C11.38 21.6875 11.19 21.7575 11 21.7575C10.81 21.7575 10.62 21.6875 10.47 21.5375C10.18 21.2475 10.18 20.7675 10.47 20.4775L12.2 18.7475C12.13 18.7475 12.07 18.7475 12 18.7475C6.62 18.7475 2.25 15.7475 2.25 12.0575C2.25 10.2975 3.22 8.6375 4.99 7.3875C5.33 7.1475 5.8 7.2275 6.03 7.5675C6.27 7.9075 6.19 8.3775 5.85 8.6075C4.49 9.5675 3.74 10.7875 3.74 12.0575C3.74 14.9175 7.44 17.2475 11.99 17.2475C12.05 17.2475 12.11 17.2475 12.17 17.2475L10.46 15.5375C10.17 15.2475 10.17 14.7675 10.46 14.4775C10.75 14.1875 11.23 14.1875 11.52 14.4775L14.52 17.4775H14.53ZM12 5.2575C11.93 5.2575 11.87 5.2575 11.8 5.2575L13.53 3.5275C13.82 3.2375 13.82 2.7575 13.53 2.4675C13.24 2.1775 12.76 2.1775 12.47 2.4675L9.47 5.4675C9.18 5.7575 9.18 6.2375 9.47 6.5275L12.47 9.5275C12.62 9.6775 12.81 9.7475 13 9.7475C13.19 9.7475 13.38 9.6775 13.53 9.5275C13.82 9.2375 13.82 8.7575 13.53 8.4675L11.82 6.7575C11.88 6.7575 11.94 6.7575 12 6.7575C16.55 6.7575 20.25 9.0875 20.25 11.9475C20.25 13.2075 19.5 14.4375 18.14 15.3975C17.8 15.6375 17.72 16.1075 17.96 16.4475C18.11 16.6575 18.34 16.7675 18.57 16.7675C18.72 16.7675 18.87 16.7275 19 16.6275C20.77 15.3775 21.75 13.7175 21.75 11.9575C21.75 8.2675 17.38 5.2675 12 5.2675V5.2575Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/folder-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/folder-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M21.72 9.24C21.45 8.92 21.12 8.67 20.75 8.5V8C20.75 6.48 19.52 5.25 18 5.25H10.65C10.32 4.1 9.26 3.25 8 3.25H6C4.48 3.25 3.25 4.48 3.25 6V18C3.25 19.52 4.48 20.75 6 20.75H18.33C19.66 20.75 20.8 19.8 21.04 18.49L22.31 11.49C22.46 10.69 22.24 9.86 21.72 9.24ZM4.75 18V6C4.75 5.31 5.31 4.75 6 4.75H8C8.69 4.75 9.25 5.31 9.25 6C9.25 6.41 9.59 6.75 10 6.75H18C18.69 6.75 19.25 7.31 19.25 8V8.25H9.27C7.94 8.25 6.8 9.2 6.56 10.51L5.29 17.51C5.19 18.07 5.27 18.64 5.51 19.15C5.06 18.96 4.75 18.52 4.75 18ZM20.83 11.22L19.56 18.22C19.45 18.81 18.94 19.25 18.33 19.25H8C7.63 19.25 7.28 19.09 7.04 18.8C6.8 18.51 6.7 18.14 6.77 17.78L8.04 10.78C8.15 10.19 8.66 9.75 9.27 9.75H19.6C19.97 9.75 20.32 9.91 20.56 10.2C20.8 10.49 20.9 10.86 20.83 11.22Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/fullsize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/fullsize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 3.25H4C3.04 3.25 2.25 4.04 2.25 5V11C2.25 11.96 3.04 12.75 4 12.75H12C12.96 12.75 13.75 11.96 13.75 11V5C13.75 4.04 12.96 3.25 12 3.25ZM12.25 11C12.25 11.14 12.14 11.25 12 11.25H4C3.86 11.25 3.75 11.14 3.75 11V5C3.75 4.86 3.86 4.75 4 4.75H12C12.14 4.75 12.25 4.86 12.25 5V11Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/image-48x48.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/image-48x48.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M33 10.25H15C12.38 10.25 10.25 12.38 10.25 15V33C10.25 35.62 12.38 37.75 15 37.75H33C35.62 37.75 37.75 35.62 37.75 33V15C37.75 12.38 35.62 10.25 33 10.25ZM36.25 33C36.25 34.79 34.79 36.25 33 36.25H15C13.21 36.25 11.75 34.79 11.75 33V15C11.75 13.21 13.21 11.75 15 11.75H33C34.79 11.75 36.25 13.21 36.25 15V33ZM30.5 14.25C28.71 14.25 27.25 15.71 27.25 17.5C27.25 19.29 28.71 20.75 30.5 20.75C32.29 20.75 33.75 19.29 33.75 17.5C33.75 15.71 32.29 14.25 30.5 14.25ZM30.5 19.25C29.54 19.25 28.75 18.46 28.75 17.5C28.75 16.54 29.54 15.75 30.5 15.75C31.46 15.75 32.25 16.54 32.25 17.5C32.25 18.46 31.46 19.25 30.5 19.25ZM29.26 26.28C28.94 25.92 28.49 25.71 28.01 25.7C27.54 25.68 27.07 25.87 26.73 26.2L24.95 27.94L22.28 25.23C21.94 24.89 21.5 24.71 21 24.71C20.52 24.71 20.06 24.93 19.74 25.28L14.74 30.78C14.25 31.3 14.12 32.06 14.41 32.72C14.69 33.36 15.28 33.75 15.95 33.75H32.07C32.74 33.75 33.33 33.35 33.61 32.72C33.89 32.06 33.77 31.31 33.29 30.79L29.27 26.29L29.26 26.28ZM32.22 32.12C32.18 32.2 32.13 32.25 32.06 32.25H15.94C15.87 32.25 15.81 32.21 15.78 32.12C15.77 32.09 15.71 31.93 15.83 31.8L20.84 26.29C20.9 26.22 20.99 26.21 21.02 26.21C21.06 26.21 21.14 26.22 21.2 26.29L24.4 29.54C24.69 29.83 25.16 29.84 25.46 29.54L27.77 27.27C27.83 27.21 27.9 27.2 27.94 27.2C28.01 27.2 28.06 27.21 28.13 27.28L32.16 31.79C32.16 31.79 32.16 31.79 32.17 31.8C32.29 31.93 32.23 32.09 32.22 32.12Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/loading-48x48.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/loading-48x48.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><g clip-path=\"url(#clip0_19679_369428)\"><path opacity=\"0.1\" d=\"M24 40C15.18 40 8 32.82 8 24C8 15.18 15.18 8 24 8C32.82 8 40 15.18 40 24C40 32.82 32.82 40 24 40ZM24 12C17.38 12 12 17.38 12 24C12 30.62 17.38 36 24 36C30.62 36 36 30.62 36 24C36 17.38 30.62 12 24 12Z\" fill=\"black\" fill-opacity=\"0.91\"></path><path d=\"M10 26C8.9 26 8 25.1 8 24C8 15.18 15.18 8 24 8C25.1 8 26 8.9 26 10C26 11.1 25.1 12 24 12C17.38 12 12 17.38 12 24C12 25.1 11.1 26 10 26Z\" fill=\"#19B394\"></path></g><defs><clipPath id=\"clip0_19679_369428\"><rect width=\"32\" height=\"32\" fill=\"white\" transform=\"translate(8 8)\"></rect></clipPath></defs></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/maximize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/maximize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.75 3V7C13.75 7.41 13.41 7.75 13 7.75C12.59 7.75 12.25 7.41 12.25 7V4.81L9.53 7.53C9.38 7.68 9.19 7.75 9 7.75C8.81 7.75 8.62 7.68 8.47 7.53C8.18 7.24 8.18 6.76 8.47 6.47L11.19 3.75H9C8.59 3.75 8.25 3.41 8.25 3C8.25 2.59 8.59 2.25 9 2.25H13C13.1 2.25 13.19 2.27 13.29 2.31C13.47 2.39 13.62 2.53 13.7 2.72C13.74 2.81 13.76 2.91 13.76 3.01L13.75 3ZM7.53 8.47C7.24 8.18 6.76 8.18 6.47 8.47L3.75 11.19V9C3.75 8.59 3.41 8.25 3 8.25C2.59 8.25 2.25 8.59 2.25 9V13C2.25 13.1 2.27 13.19 2.31 13.29C2.39 13.47 2.53 13.62 2.72 13.7C2.81 13.74 2.91 13.76 3.01 13.76H7.01C7.42 13.76 7.76 13.42 7.76 13.01C7.76 12.6 7.42 12.26 7.01 12.26H4.82L7.54 9.54C7.83 9.25 7.83 8.77 7.54 8.48L7.53 8.47Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/minimize-16x16.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/minimize-16x16.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.75 8C13.75 8.41 13.41 8.75 13 8.75H3C2.59 8.75 2.25 8.41 2.25 8C2.25 7.59 2.59 7.25 3 7.25H13C13.41 7.25 13.75 7.59 13.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/more-24x24.svg":
/*!***********************************************************!*\
  !*** ./packages/survey-core/src/images-v2/more-24x24.svg ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 10.25C11.04 10.25 10.25 11.04 10.25 12C10.25 12.96 11.04 13.75 12 13.75C12.96 13.75 13.75 12.96 13.75 12C13.75 11.04 12.96 10.25 12 10.25ZM11.75 12C11.75 11.86 11.86 11.75 12 11.75C12.14 11.75 12.25 11.86 12.25 12C12.25 12.28 11.75 12.28 11.75 12ZM19 10.25C18.04 10.25 17.25 11.04 17.25 12C17.25 12.96 18.04 13.75 19 13.75C19.96 13.75 20.75 12.96 20.75 12C20.75 11.04 19.96 10.25 19 10.25ZM18.75 12C18.75 11.86 18.86 11.75 19 11.75C19.14 11.75 19.25 11.86 19.25 12C19.25 12.28 18.75 12.28 18.75 12ZM5 10.25C4.04 10.25 3.25 11.04 3.25 12C3.25 12.96 4.04 13.75 5 13.75C5.96 13.75 6.75 12.96 6.75 12C6.75 11.04 5.96 10.25 5 10.25ZM4.75 12C4.75 11.86 4.86 11.75 5 11.75C5.14 11.75 5.25 11.86 5.25 12C5.25 12.28 4.75 12.28 4.75 12Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/navmenu-24x24.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/navmenu-24x24.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M3.25 7C3.25 6.59 3.59 6.25 4 6.25H15C15.41 6.25 15.75 6.59 15.75 7C15.75 7.41 15.41 7.75 15 7.75H4C3.59 7.75 3.25 7.41 3.25 7ZM20 11.25H4C3.59 11.25 3.25 11.59 3.25 12C3.25 12.41 3.59 12.75 4 12.75H20C20.41 12.75 20.75 12.41 20.75 12C20.75 11.59 20.41 11.25 20 11.25ZM9 16.25H4C3.59 16.25 3.25 16.59 3.25 17C3.25 17.41 3.59 17.75 4 17.75H9C9.41 17.75 9.75 17.41 9.75 17C9.75 16.59 9.41 16.25 9 16.25Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/noimage-48x48.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/noimage-48x48.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M30.4975 14.2475C28.7075 14.2475 27.2475 15.7075 27.2475 17.4975C27.2475 19.2875 28.7075 20.7475 30.4975 20.7475C32.2875 20.7475 33.7475 19.2875 33.7475 17.4975C33.7475 15.7075 32.2875 14.2475 30.4975 14.2475ZM30.4975 19.2475C29.5375 19.2475 28.7475 18.4575 28.7475 17.4975C28.7475 16.5375 29.5375 15.7475 30.4975 15.7475C31.4575 15.7475 32.2475 16.5375 32.2475 17.4975C32.2475 18.4575 31.4575 19.2475 30.4975 19.2475ZM13.5175 11.2175C13.4375 10.8075 13.7075 10.4175 14.1175 10.3375C14.4275 10.2775 14.7175 10.2475 14.9975 10.2475H32.9975C35.6175 10.2475 37.7475 12.3775 37.7475 14.9975V32.9975C37.7475 33.2775 37.7175 33.5675 37.6575 33.8775C37.5875 34.2375 37.2775 34.4875 36.9175 34.4875C36.8675 34.4875 36.8275 34.4875 36.7775 34.4775C36.3675 34.3975 36.1075 34.0075 36.1775 33.5975C36.2175 33.3775 36.2375 33.1775 36.2375 32.9975V14.9975C36.2375 13.2075 34.7775 11.7475 32.9875 11.7475H14.9975C14.8075 11.7475 14.6175 11.7675 14.3975 11.8075C13.9875 11.8875 13.5975 11.6175 13.5175 11.2075V11.2175ZM34.4775 36.7775C34.5575 37.1875 34.2875 37.5775 33.8775 37.6575C33.5675 37.7175 33.2775 37.7475 32.9975 37.7475H14.9975C12.3775 37.7475 10.2475 35.6175 10.2475 32.9975V14.9975C10.2475 14.7175 10.2775 14.4275 10.3375 14.1175C10.4175 13.7075 10.8075 13.4375 11.2175 13.5175C11.6275 13.5975 11.8875 13.9875 11.8175 14.3975C11.7775 14.6175 11.7575 14.8175 11.7575 14.9975V32.9975C11.7575 34.7875 13.2175 36.2475 15.0075 36.2475H33.0075C33.1975 36.2475 33.3875 36.2275 33.6075 36.1875C34.0075 36.1075 34.4075 36.3775 34.4875 36.7875L34.4775 36.7775ZM15.8275 31.7975C15.6975 31.9375 15.7575 32.0875 15.7775 32.1175C15.8175 32.1975 15.8675 32.2475 15.9375 32.2475H29.8175C30.2275 32.2475 30.5675 32.5875 30.5675 32.9975C30.5675 33.4075 30.2275 33.7475 29.8175 33.7475H15.9375C15.2675 33.7475 14.6775 33.3475 14.3975 32.7175C14.1075 32.0575 14.2375 31.2975 14.7275 30.7775L19.7275 25.2775C20.0475 24.9275 20.5075 24.7175 20.9875 24.7075C21.4875 24.7275 21.9375 24.8875 22.2675 25.2275L25.4675 28.4775C25.7575 28.7675 25.7575 29.2475 25.4675 29.5375C25.1675 29.8275 24.6975 29.8275 24.4075 29.5375L21.2075 26.2875C21.1475 26.2175 21.0675 26.1875 21.0275 26.2075C20.9875 26.2075 20.9075 26.2175 20.8475 26.2875L15.8375 31.7975H15.8275ZM38.5275 38.5275C38.3775 38.6775 38.1875 38.7475 37.9975 38.7475C37.8075 38.7475 37.6175 38.6775 37.4675 38.5275L9.4675 10.5275C9.1775 10.2375 9.1775 9.7575 9.4675 9.4675C9.7575 9.1775 10.2375 9.1775 10.5275 9.4675L38.5275 37.4675C38.8175 37.7575 38.8175 38.2375 38.5275 38.5275Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/ranking-arrows.svg":
/*!***************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/ranking-arrows.svg ***!
  \***************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 10 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M10 5L5 0L0 5H4V9H6V5H10Z\"></path><path d=\"M6 19V15H4V19H0L5 24L10 19H6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/rankingundefined-16x16.svg":
/*!***********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/rankingundefined-16x16.svg ***!
  \***********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M11.75 8C11.75 8.41 11.41 8.75 11 8.75H5C4.59 8.75 4.25 8.41 4.25 8C4.25 7.59 4.59 7.25 5 7.25H11C11.41 7.25 11.75 7.59 11.75 8Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/rating-star-2.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/rating-star-2.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M24 39.5057L11.7226 45.9839C10.4095 46.6739 8.87606 45.5622 9.12525 44.096L11.4734 30.373L1.54411 20.6556C0.480254 19.6207 1.06489 17.8095 2.53128 17.5986L16.2559 15.5957L22.3994 3.10891C23.0512 1.77685 24.9488 1.77685 25.6102 3.10891L31.7441 15.5957L45.4687 17.5986C46.9351 17.8095 47.5197 19.6207 46.4559 20.6556L36.5266 30.373L38.8748 44.096C39.1239 45.5622 37.5905 46.6835 36.2774 45.9839L24 39.5057Z\" fill=\"none\" stroke-width=\"2\"></path><path d=\"M24.3981 33.1305L24 32.9206L23.6019 33.1305L15.8715 37.2059L17.3542 28.5663L17.43 28.1246L17.1095 27.8113L10.83 21.6746L19.4965 20.4049L19.9405 20.3399L20.1387 19.9373L24 12.0936L27.8613 19.9373L28.0595 20.3399L28.5035 20.4049L37.17 21.6746L30.8905 27.8113L30.57 28.1246L30.6458 28.5663L32.1285 37.2059L24.3981 33.1305Z\" stroke-width=\"1.70746\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/rating-star-small-2.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/rating-star-small-2.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 19.3373L6.13001 22.4373C5.50001 22.7673 4.77001 22.2373 4.89001 21.5373L6.01001 14.9773L1.26001 10.3273C0.750007 9.83728 1.03001 8.96728 1.73001 8.86728L8.29001 7.90728L11.23 1.93728C11.54 1.29728 12.45 1.29728 12.77 1.93728L15.7 7.90728L22.26 8.86728C22.96 8.96728 23.24 9.83728 22.73 10.3273L17.98 14.9773L19.1 21.5373C19.22 22.2373 18.49 22.7773 17.86 22.4373L11.99 19.3373H12Z\" fill=\"none\" stroke-width=\"2\"></path><path d=\"M12 15.9472L8.58001 17.7572L9.23001 13.9272L6.45001 11.2072L10.29 10.6472L12 7.17725L13.71 10.6472L17.55 11.2072L14.77 13.9272L15.42 17.7572L12 15.9472Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/rating-star-small.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/rating-star-small.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><g><path d=\"M12 19.3373L6.13001 22.4373C5.50001 22.7673 4.77001 22.2373 4.89001 21.5373L6.01001 14.9773L1.26001 10.3273C0.750007 9.83728 1.03001 8.96728 1.73001 8.86728L8.29001 7.90728L11.23 1.93728C11.54 1.29728 12.45 1.29728 12.77 1.93728L15.7 7.90728L22.26 8.86728C22.96 8.96728 23.24 9.83728 22.73 10.3273L17.98 14.9773L19.1 21.5373C19.22 22.2373 18.49 22.7773 17.86 22.4373L11.99 19.3373H12Z\"></path></g></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/rating-star.svg":
/*!************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/rating-star.svg ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><g><path d=\"M24 39.5057L11.7226 45.9839C10.4095 46.6739 8.87606 45.5622 9.12525 44.096L11.4734 30.373L1.54411 20.6556C0.480254 19.6207 1.06489 17.8095 2.53128 17.5986L16.2559 15.5957L22.3994 3.10891C23.0512 1.77685 24.9488 1.77685 25.6102 3.10891L31.7441 15.5957L45.4687 17.5986C46.9351 17.8095 47.5197 19.6207 46.4559 20.6556L36.5266 30.373L38.8748 44.096C39.1239 45.5622 37.5905 46.6835 36.2774 45.9839L24 39.5057Z\"></path></g></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/reorder-24x24.svg":
/*!**************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/reorder-24x24.svg ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M8.9444 10.75H15.0544C15.7144 10.75 16.3144 10.39 16.6144 9.80002C16.9144 9.22002 16.8644 8.52002 16.4844 7.98002L13.4244 3.71002C12.7644 2.79002 11.2344 2.79002 10.5744 3.71002L7.5244 7.99002C7.1444 8.53002 7.0944 9.22002 7.3944 9.81002C7.6944 10.4 8.2944 10.76 8.9544 10.76L8.9444 10.75ZM8.7444 8.86002L11.7944 4.58002C11.8644 4.49002 11.9544 4.48002 11.9944 4.48002C12.0344 4.48002 12.1344 4.49002 12.1944 4.58002L15.2544 8.86002C15.3344 8.97002 15.3044 9.07002 15.2744 9.12002C15.2444 9.17002 15.1844 9.26002 15.0544 9.26002H8.9444C8.8144 9.26002 8.7444 9.18002 8.7244 9.12002C8.7044 9.06002 8.6644 8.97002 8.7444 8.86002ZM15.0544 13.25H8.9444C8.2844 13.25 7.6844 13.61 7.3844 14.2C7.0844 14.78 7.1344 15.48 7.5144 16.02L10.5744 20.3C10.9044 20.76 11.4344 21.03 11.9944 21.03C12.5544 21.03 13.0944 20.76 13.4144 20.3L16.4744 16.02C16.8544 15.48 16.9044 14.79 16.6044 14.2C16.3044 13.61 15.7044 13.25 15.0444 13.25H15.0544ZM15.2644 15.15L12.2044 19.43C12.0744 19.61 11.9244 19.61 11.7944 19.43L8.7344 15.15C8.6544 15.04 8.6844 14.94 8.7144 14.89C8.7444 14.84 8.8044 14.75 8.9344 14.75H15.0444C15.1744 14.75 15.2444 14.83 15.2644 14.89C15.2844 14.95 15.3244 15.04 15.2444 15.15H15.2644Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/restoredown-16x16.svg":
/*!******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/restoredown-16x16.svg ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.69 8.71C7.73 8.8 7.75 8.9 7.75 9V13C7.75 13.41 7.41 13.75 7 13.75C6.59 13.75 6.25 13.41 6.25 13V10.81L3.53 13.53C3.38 13.68 3.19 13.75 3 13.75C2.81 13.75 2.62 13.68 2.47 13.53C2.18 13.24 2.18 12.76 2.47 12.47L5.19 9.75H3C2.59 9.75 2.25 9.41 2.25 9C2.25 8.59 2.59 8.25 3 8.25H7C7.1 8.25 7.19 8.27 7.29 8.31C7.47 8.39 7.62 8.53 7.7 8.72L7.69 8.71ZM13 6.25H10.81L13.53 3.53C13.82 3.24 13.82 2.76 13.53 2.47C13.24 2.18 12.76 2.18 12.47 2.47L9.75 5.19V3C9.75 2.59 9.41 2.25 9 2.25C8.59 2.25 8.25 2.59 8.25 3V7C8.25 7.1 8.27 7.19 8.31 7.29C8.39 7.47 8.53 7.62 8.72 7.7C8.81 7.74 8.91 7.76 9.01 7.76H13.01C13.42 7.76 13.76 7.42 13.76 7.01C13.76 6.6 13.42 6.26 13.01 6.26L13 6.25Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/search-24x24.svg":
/*!*************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/search-24x24.svg ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M13.9975 2.25C9.7275 2.25 6.2475 5.73 6.2475 10C6.2475 11.87 6.9075 13.58 8.0175 14.92L2.4675 20.47C2.1775 20.76 2.1775 21.24 2.4675 21.53C2.6175 21.68 2.8075 21.75 2.9975 21.75C3.1875 21.75 3.3775 21.68 3.5275 21.53L9.0775 15.98C10.4175 17.08 12.1275 17.75 13.9975 17.75C18.2675 17.75 21.7475 14.27 21.7475 10C21.7475 5.73 18.2675 2.25 13.9975 2.25ZM13.9975 16.25C10.5475 16.25 7.7475 13.45 7.7475 10C7.7475 6.55 10.5475 3.75 13.9975 3.75C17.4475 3.75 20.2475 6.55 20.2475 10C20.2475 13.45 17.4475 16.25 13.9975 16.25Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate1-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate1-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M4 4.9938C4 4.44362 4.45 3.99348 5 3.99348H6.59L5.3 2.70306C4.91 2.31293 4.91 1.68272 5.3 1.2926C5.69 0.902468 6.32 0.902468 6.71 1.2926L9.71 4.29357C9.8 4.3836 9.88 4.49364 9.93 4.62368C10.03 4.86376 10.03 5.14385 9.93 5.38393C9.88 5.50397 9.81 5.614 9.71 5.71404L6.71 8.71501C6.51 8.91508 6.26 9.00511 6 9.00511C5.74 9.00511 5.49 8.90508 5.29 8.71501C4.9 8.32489 4.9 7.69468 5.29 7.30456L6.58 6.01413H4.99C4.44 6.01413 3.99 5.56399 3.99 5.01381L4 4.9938ZM14.08 5.37393C14.13 5.49397 14.2 5.604 14.3 5.70403L17.3 8.70501C17.5 8.90508 17.75 8.99511 18.01 8.99511C18.27 8.99511 18.52 8.89507 18.72 8.70501C19.11 8.31488 19.11 7.68468 18.72 7.29455L17.43 6.00413H19.02C19.57 6.00413 20.02 5.55399 20.02 5.00381C20.02 4.45363 19.57 4.00348 19.02 4.00348H17.43L18.72 2.71306C19.11 2.32293 19.11 1.69273 18.72 1.3026C18.33 0.912471 17.7 0.912471 17.31 1.3026L14.31 4.30358C14.22 4.39361 14.14 4.50364 14.09 4.63368C13.99 4.87376 13.99 5.15385 14.09 5.39393L14.08 5.37393ZM22 14.9971V20.999C22 22.6496 20.65 24 19 24H5C3.35 24 2 22.6496 2 20.999V14.9971C2 13.3465 3.35 11.9961 5 11.9961H19C20.65 11.9961 22 13.3465 22 14.9971ZM19 13.9967H16V16.9977H20V14.9971C20 14.4469 19.55 13.9967 19 13.9967ZM14 16.9977V13.9967H10V16.9977H14ZM10 18.9984V21.9993H14V18.9984H10ZM4 14.9971V16.9977H8V13.9967H5C4.45 13.9967 4 14.4469 4 14.9971ZM5 21.9993H8V18.9984H4V20.999C4 21.5492 4.45 21.9993 5 21.9993ZM20 20.999V18.9984H16V21.9993H19C19.55 21.9993 20 21.5492 20 20.999Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate10-24x24.svg":
/*!********************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate10-24x24.svg ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 23C6.85721 23 1.15412 19.9621 0.0134987 13.1669C-0.0765501 12.6272 0.293651 12.1076 0.833944 12.0177C1.38424 11.9277 1.89452 12.2975 1.98457 12.8371C2.92508 18.4732 7.69767 20.9914 12 20.9914C16.3023 20.9914 21.0749 18.4732 22.0154 12.8371C22.1055 12.2975 22.6158 11.9277 23.1661 12.0177C23.7063 12.1076 24.0765 12.6272 23.9865 13.1669C22.8559 19.9521 17.1428 23 11.99 23H12.01ZM21.165 6.15177C22.3056 5.01257 22.3056 3.16386 21.165 2.02465L21.0049 1.85477C19.9143 0.765533 18.1633 0.725561 17.0227 1.71487C15.8821 0.715568 14.1312 0.765533 13.0406 1.85477L12.8705 2.01466C11.7299 3.15386 11.7299 5.00257 12.8705 6.14178L17.0227 10.2889L21.175 6.14178L21.165 6.15177ZM15.742 3.27378L17.0127 4.54289L18.2834 3.27378C18.6436 2.91403 19.2239 2.91403 19.5841 3.27378L19.7442 3.43367C20.1044 3.79342 20.1044 4.37301 19.7442 4.73276L17.0127 7.46086L14.2812 4.73276C13.921 4.37301 13.921 3.79342 14.2812 3.43367L14.4413 3.27378C14.6214 3.09391 14.8515 3.00397 15.0917 3.00397C15.3318 3.00397 15.5619 3.09391 15.742 3.27378ZM11.1595 6.15177C12.3002 5.01257 12.3002 3.16386 11.1595 2.02465L10.9995 1.85477C9.90886 0.765533 8.15792 0.725561 7.0173 1.71487C5.87668 0.715568 4.12573 0.765533 3.03514 1.85477L2.86505 2.01466C1.72443 3.15386 1.72443 5.00257 2.86505 6.14178L7.0173 10.2889L11.1695 6.14178L11.1595 6.15177ZM5.7366 3.27378L7.00729 4.54289L8.27798 3.27378C8.63818 2.91403 9.21849 2.91403 9.57869 3.27378L9.73877 3.43367C10.099 3.79342 10.099 4.37301 9.73877 4.73276L7.00729 7.46086L4.27581 4.73276C3.91562 4.37301 3.91562 3.79342 4.27581 3.43367L4.4359 3.27378C4.61599 3.09391 4.84612 3.00397 5.08625 3.00397C5.32638 3.00397 5.5565 3.09391 5.7366 3.27378Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate2-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate2-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><g clip-path=\"url(#clip0_15894_140103)\"><path d=\"M4.88291 4.51001C4.47291 4.51001 4.08291 4.25001 3.94291 3.84001C3.76291 3.32001 4.03291 2.75001 4.55291 2.57001L8.32291 1.25001C8.84291 1.06001 9.41291 1.34001 9.59291 1.86001C9.77291 2.38001 9.50291 2.95001 8.98291 3.13001L5.20291 4.45001C5.09291 4.49001 4.98291 4.51001 4.87291 4.51001H4.88291ZM19.8129 3.89001C20.0229 3.38001 19.7729 2.79001 19.2629 2.59001L15.5529 1.07001C15.0429 0.860007 14.4529 1.11001 14.2529 1.62001C14.0429 2.13001 14.2929 2.72001 14.8029 2.92001L18.5029 4.43001C18.6229 4.48001 18.7529 4.50001 18.8829 4.50001C19.2729 4.50001 19.6529 4.27001 19.8129 3.88001V3.89001ZM3.50291 6.00001C2.64291 6.37001 1.79291 6.88001 1.00291 7.48001C0.79291 7.64001 0.64291 7.87001 0.59291 8.14001C0.48291 8.73001 0.87291 9.29001 1.45291 9.40001C2.04291 9.51001 2.60291 9.12001 2.71291 8.54001C2.87291 7.69001 3.12291 6.83001 3.50291 5.99001V6.00001ZM21.0429 8.55001C21.6029 10.48 24.2429 8.84001 22.7529 7.48001C21.9629 6.88001 21.1129 6.37001 20.2529 6.00001C20.6329 6.84001 20.8829 7.70001 21.0429 8.55001ZM21.5729 13.2C21.2529 14.2 22.5429 15.09 23.3629 14.39C23.8529 14 23.9229 13.29 23.5429 12.81C21.7429 10.67 22.1329 10.55 21.5829 13.2H21.5729ZM1.75291 11C1.22291 11.79 -0.14709 12.64 0.0129102 13.75C0.15291 14.36 0.75291 14.74 1.35291 14.6C2.98291 14.1 1.80291 12.22 1.75291 11ZM19.8829 17C19.8829 13.14 16.2929 10 11.8829 10C7.47291 10 3.88291 13.14 3.88291 17C3.88291 20.86 7.47291 24 11.8829 24C16.2929 24 19.8829 20.86 19.8829 17ZM17.8829 17C17.8829 19.76 15.1929 22 11.8829 22C8.57291 22 5.88291 19.76 5.88291 17C5.88291 14.24 8.57291 12 11.8829 12C15.1929 12 17.8829 14.24 17.8829 17Z\"></path></g><defs><clipPath id=\"clip0_15894_140103\"><rect width=\"24\" height=\"24\" fill=\"white\"></rect></clipPath></defs></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate3-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate3-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.01915 7C6.46961 7 6.01998 6.55 6.01998 6V2C6.01998 1.45 6.46961 1 7.01915 1C7.56869 1 8.01832 1.45 8.01832 2V6C8.01832 6.55 7.56869 7 7.01915 7ZM18.01 6V2C18.01 1.45 17.5604 1 17.0108 1C16.4613 1 16.0117 1.45 16.0117 2V6C16.0117 6.55 16.4613 7 17.0108 7C17.5604 7 18.01 6.55 18.01 6ZM16.4213 21.58L18.01 19.99L19.2989 21.28C19.6886 21.67 20.3181 21.67 20.7077 21.28C21.0974 20.89 21.0974 20.26 20.7077 19.87L19.4188 18.58C18.6395 17.8 17.3705 17.8 16.5912 18.58L15.0025 20.17L13.4138 18.58C12.6345 17.8 11.3655 17.8 10.5862 18.58L8.9975 20.17L7.40883 18.58C6.62948 17.8 5.36053 17.8 4.58118 18.58L3.29226 19.87C2.90258 20.26 2.90258 20.89 3.29226 21.28C3.68193 21.67 4.31141 21.67 4.70108 21.28L5.99001 19.99L7.57868 21.58C8.35803 22.36 9.62698 22.36 10.4063 21.58L11.995 19.99L13.5837 21.58C13.9734 21.97 14.4829 22.16 14.9925 22.16C15.5021 22.16 16.0117 21.97 16.4013 21.58H16.4213Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate4-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate4-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.06927 7C6.51927 7 6.06927 6.55 6.06927 6V2C6.06927 1.45 6.51927 1 7.06927 1C7.61927 1 8.06927 1.45 8.06927 2V6C8.06927 6.55 7.61927 7 7.06927 7ZM18.0693 6V2C18.0693 1.45 17.6193 1 17.0693 1C16.5193 1 16.0693 1.45 16.0693 2V6C16.0693 6.55 16.5193 7 17.0693 7C17.6193 7 18.0693 6.55 18.0693 6ZM22.5693 21.9C23.0693 21.66 23.2793 21.07 23.0393 20.57C21.1093 16.52 16.9093 14 12.0693 14C7.22927 14 3.02927 16.52 1.09927 20.57C0.859273 21.07 1.06927 21.67 1.56927 21.9C2.06927 22.14 2.65927 21.93 2.89927 21.43C4.49927 18.08 8.00927 16 12.0593 16C16.1093 16 19.6293 18.08 21.2193 21.43C21.3893 21.79 21.7493 22 22.1193 22C22.2593 22 22.4093 21.97 22.5493 21.9H22.5693Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate5-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate5-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7.00572 7C6.45572 7 6.00572 6.55 6.00572 6V2C6.00572 1.45 6.45572 1 7.00572 1C7.55572 1 8.00572 1.45 8.00572 2V6C8.00572 6.55 7.55572 7 7.00572 7ZM18.0057 6V2C18.0057 1.45 17.5557 1 17.0057 1C16.4557 1 16.0057 1.45 16.0057 2V6C16.0057 6.55 16.4557 7 17.0057 7C17.5557 7 18.0057 6.55 18.0057 6ZM19.9457 21.33C20.1257 20.81 19.8557 20.24 19.3357 20.05C14.5457 18.35 9.45572 18.35 4.66572 20.05C4.14572 20.23 3.87572 20.81 4.05572 21.33C4.23572 21.85 4.80572 22.12 5.33572 21.94C9.69572 20.4 14.3057 20.4 18.6657 21.94C18.7757 21.98 18.8857 22 18.9957 22C19.4057 22 19.7957 21.74 19.9357 21.33H19.9457Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate6-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate6-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M7 7C6.45 7 6 6.55 6 6V2C6 1.45 6.45 1 7 1C7.55 1 8 1.45 8 2V6C8 6.55 7.55 7 7 7ZM18 6V2C18 1.45 17.55 1 17 1C16.45 1 16 1.45 16 2V6C16 6.55 16.45 7 17 7C17.55 7 18 6.55 18 6ZM21 21C21 20.45 20.55 20 20 20H4C3.45 20 3 20.45 3 21C3 21.55 3.45 22 4 22H20C20.55 22 21 21.55 21 21Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate7-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate7-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.0022 23.99C11.452 23.99 11.0018 23.5402 11.0018 22.9904C11.0018 22.4407 11.452 21.9909 12.0022 21.9909C16.3137 21.9909 21.0755 19.472 22.0158 13.8344C22.1058 13.2947 22.616 12.9248 23.1662 13.0148C23.7064 13.1047 24.0765 13.6245 23.9865 14.1643C22.8561 20.9513 17.144 24 11.9922 24L12.0022 23.99ZM8.00072 5.99783V1.99957C8.00072 1.4498 7.55056 1 7.00036 1C6.45016 1 6 1.4498 6 1.99957V5.99783C6 6.54759 6.45016 6.99739 7.00036 6.99739C7.55056 6.99739 8.00072 6.54759 8.00072 5.99783ZM18.0043 5.99783V1.99957C18.0043 1.4498 17.5542 1 17.004 1C16.4538 1 16.0036 1.4498 16.0036 1.99957V5.99783C16.0036 6.54759 16.4538 6.99739 17.004 6.99739C17.5542 6.99739 18.0043 6.54759 18.0043 5.99783Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate8-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate8-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 24C6.85721 24 1.15412 20.96 0.0134987 14.16C-0.0765501 13.62 0.293651 13.1 0.833944 13.01C1.38424 12.92 1.89452 13.29 1.98457 13.83C2.92508 19.47 7.69767 21.99 12 21.99C16.3023 21.99 21.0749 19.47 22.0154 13.83C22.1055 13.29 22.6158 12.92 23.1661 13.01C23.7063 13.1 24.0765 13.62 23.9865 14.16C22.8559 20.95 17.1428 24 11.99 24H12.01ZM8.00783 6V2C8.00783 1.45 7.55759 1 7.00729 1C6.45699 1 6.00675 1.45 6.00675 2V6C6.00675 6.55 6.45699 7 7.00729 7C7.55759 7 8.00783 6.55 8.00783 6ZM18.0133 6V2C18.0133 1.45 17.563 1 17.0127 1C16.4624 1 16.0122 1.45 16.0122 2V6C16.0122 6.55 16.4624 7 17.0127 7C17.563 7 18.0133 6.55 18.0133 6Z\"></path></svg>"

/***/ }),

/***/ "./packages/survey-core/src/images-v2/smiley-rate9-24x24.svg":
/*!*******************************************************************!*\
  !*** ./packages/survey-core/src/images-v2/smiley-rate9-24x24.svg ***!
  \*******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12.01 24C6.85767 24 1.15509 20.96 0.0145752 14.16C-0.0354475 13.87 0.0445888 13.57 0.234675 13.35C0.424761 13.13 0.704888 13 0.995019 13H23.005C23.2951 13 23.5752 13.13 23.7653 13.35C23.9554 13.57 24.0354 13.87 23.9854 14.16C22.8549 20.95 17.1423 24 11.99 24H12.01ZM2.25559 15C3.61621 19.82 8.0182 22 12.01 22C16.0018 22 20.4038 19.82 21.7644 15H2.25559ZM8.00819 6V2C8.00819 1.45 7.55799 1 7.00774 1C6.45749 1 6.00729 1.45 6.00729 2V6C6.00729 6.55 6.45749 7 7.00774 7C7.55799 7 8.00819 6.55 8.00819 6ZM18.0127 6V2C18.0127 1.45 17.5625 1 17.0123 1C16.462 1 16.0118 1.45 16.0118 2V6C16.0118 6.55 16.462 7 17.0123 7C17.5625 7 18.0127 6.55 18.0127 6Z\"></path></svg>"

/***/ }),

/***/ "./src/entries/knockout-ui.ts":
/*!*************************************************!*\
  !*** ./src/entries/knockout-ui.ts + 92 modules ***!
  \*************************************************/
/*! exports provided: Survey, Model, PopupSurvey, SurveyWindow, ImplementorBase, QuestionRow, Page, Panel, FlowPanel, QuestionImplementor, QuestionSelectBaseImplementor, QuestionCheckboxBaseImplementor, QuestionCheckbox, QuestionTagbox, QuestionRanking, QuestionComment, QuestionDropdown, QuestionFile, QuestionHtml, QuestionMatrix, QuestionMatrixDropdown, QuestionMatrixDynamicImplementor, QuestionMatrixDynamic, QuestionPanelDynamic, MultipleTextItem, QuestionMultipleText, QuestionRadiogroup, QuestionRating, QuestionRatingImplementor, QuestionText, QuestionBoolean, QuestionEmpty, QuestionExpression, QuestionImagePicker, PopupSurveyImplementor, SurveyTemplateText, QuestionImage, QuestionSignaturePad, QuestionCustom, QuestionButtonGroup, TextAreaViewModel, ActionBarItemViewModel, ActionBarItemDropdownViewModel, ActionBarSeparatorViewModel, ActionContainerImplementor, CheckboxViewModel, BooleanRadioItemViewModel, BooleanRadioViewModel, PanelViewModel, PopupViewModel, showModal, showDialog, ProgressButtonsViewModel, ProgressViewModel, ComponentsContainer, TitleElementViewModel, TitleContentViewModel, TitleActionViewModel, StringEditorViewModel, StringViewerViewModel, LogoImageViewModel, Skeleton, CharacterCounterComponent, RatingItemViewComponent, RatingDropdownViewModel, RatingItemViewModel, RatingItemStarViewModel, RatingItemSmileyViewModel, DropdownViewModel, DropdownSelectViewModel, TagboxViewComponent, TagboxViewModel, SurveyFilePreview, SurveyFilePage, SurveyFileItem, ListItemViewComponent, ListItemContentViewComponent, ListItemGroupViewComponent, ListViewComponent, SvgIconViewModel, SurveyQuestionMatrixDynamicRemoveButton, SurveyQuestionMatrixDetailButton, SurveyQuestionMatrixDynamicDragDropIcon, ButtonGroupItemViewModel, SurveyNavigationButton, SurveyQuestionPaneldynamicActioons, BrandInfoComponent, QuestionErrorComponent, NotifierViewModel, LoadingIndicatorViewModel, SurveyModel, SurveyWindowModel, settings, surveyLocalization, surveyStrings */
/*! ModuleConcatenation bailout: Cannot concat with external {"root":"Survey","commonjs2":"survey-core","commonjs":"survey-core","amd":"survey-core"} (<- Module is not an ECMAScript module) */
/*! ModuleConcatenation bailout: Cannot concat with external {"root":"ko","commonjs2":"knockout","commonjs":"knockout","amd":"knockout"} (<- Module is not an ECMAScript module) */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, "Survey", function() { return /* reexport */ kosurvey_Survey; });
__webpack_require__.d(__webpack_exports__, "Model", function() { return /* reexport */ kosurvey_Survey; });
__webpack_require__.d(__webpack_exports__, "PopupSurvey", function() { return /* reexport */ PopupSurvey; });
__webpack_require__.d(__webpack_exports__, "SurveyWindow", function() { return /* reexport */ SurveyWindow; });
__webpack_require__.d(__webpack_exports__, "ImplementorBase", function() { return /* reexport */ kobase_ImplementorBase; });
__webpack_require__.d(__webpack_exports__, "QuestionRow", function() { return /* reexport */ kopage_QuestionRow; });
__webpack_require__.d(__webpack_exports__, "Page", function() { return /* reexport */ kopage_Page; });
__webpack_require__.d(__webpack_exports__, "Panel", function() { return /* reexport */ kopage_Panel; });
__webpack_require__.d(__webpack_exports__, "FlowPanel", function() { return /* reexport */ koflowpanel_FlowPanel; });
__webpack_require__.d(__webpack_exports__, "QuestionImplementor", function() { return /* reexport */ koquestion_QuestionImplementor; });
__webpack_require__.d(__webpack_exports__, "QuestionSelectBaseImplementor", function() { return /* reexport */ QuestionSelectBaseImplementor; });
__webpack_require__.d(__webpack_exports__, "QuestionCheckboxBaseImplementor", function() { return /* reexport */ QuestionCheckboxBaseImplementor; });
__webpack_require__.d(__webpack_exports__, "QuestionCheckbox", function() { return /* reexport */ koquestion_checkbox_QuestionCheckbox; });
__webpack_require__.d(__webpack_exports__, "QuestionTagbox", function() { return /* reexport */ koquestion_tagbox_QuestionTagbox; });
__webpack_require__.d(__webpack_exports__, "QuestionRanking", function() { return /* reexport */ koquestion_ranking_QuestionRanking; });
__webpack_require__.d(__webpack_exports__, "QuestionComment", function() { return /* reexport */ koquestion_comment_QuestionComment; });
__webpack_require__.d(__webpack_exports__, "QuestionDropdown", function() { return /* reexport */ koquestion_dropdown_QuestionDropdown; });
__webpack_require__.d(__webpack_exports__, "QuestionFile", function() { return /* reexport */ QuestionFile; });
__webpack_require__.d(__webpack_exports__, "QuestionHtml", function() { return /* reexport */ koquestion_html_QuestionHtml; });
__webpack_require__.d(__webpack_exports__, "QuestionMatrix", function() { return /* reexport */ koquestion_matrix_QuestionMatrix; });
__webpack_require__.d(__webpack_exports__, "QuestionMatrixDropdown", function() { return /* reexport */ QuestionMatrixDropdown; });
__webpack_require__.d(__webpack_exports__, "QuestionMatrixDynamicImplementor", function() { return /* reexport */ koquestion_matrixdynamic_QuestionMatrixDynamicImplementor; });
__webpack_require__.d(__webpack_exports__, "QuestionMatrixDynamic", function() { return /* reexport */ koquestion_matrixdynamic_QuestionMatrixDynamic; });
__webpack_require__.d(__webpack_exports__, "QuestionPanelDynamic", function() { return /* reexport */ QuestionPanelDynamic; });
__webpack_require__.d(__webpack_exports__, "MultipleTextItem", function() { return /* reexport */ MultipleTextItem; });
__webpack_require__.d(__webpack_exports__, "QuestionMultipleText", function() { return /* reexport */ koquestion_multipletext_QuestionMultipleText; });
__webpack_require__.d(__webpack_exports__, "QuestionRadiogroup", function() { return /* reexport */ koquestion_radiogroup_QuestionRadiogroup; });
__webpack_require__.d(__webpack_exports__, "QuestionRating", function() { return /* reexport */ QuestionRating; });
__webpack_require__.d(__webpack_exports__, "QuestionRatingImplementor", function() { return /* reexport */ QuestionRatingImplementor; });
__webpack_require__.d(__webpack_exports__, "QuestionText", function() { return /* reexport */ QuestionText; });
__webpack_require__.d(__webpack_exports__, "QuestionBoolean", function() { return /* reexport */ koquestion_boolean_QuestionBoolean; });
__webpack_require__.d(__webpack_exports__, "QuestionEmpty", function() { return /* reexport */ koquestion_empty_QuestionEmpty; });
__webpack_require__.d(__webpack_exports__, "QuestionExpression", function() { return /* reexport */ koquestion_expression_QuestionExpression; });
__webpack_require__.d(__webpack_exports__, "QuestionImagePicker", function() { return /* reexport */ QuestionImagePicker; });
__webpack_require__.d(__webpack_exports__, "PopupSurveyImplementor", function() { return /* reexport */ koPopupSurvey_PopupSurveyImplementor; });
__webpack_require__.d(__webpack_exports__, "SurveyTemplateText", function() { return /* reexport */ SurveyTemplateText; });
__webpack_require__.d(__webpack_exports__, "QuestionImage", function() { return /* reexport */ koquestion_image_QuestionImage; });
__webpack_require__.d(__webpack_exports__, "QuestionSignaturePad", function() { return /* reexport */ koquestion_signaturepad_QuestionSignaturePad; });
__webpack_require__.d(__webpack_exports__, "QuestionCustom", function() { return /* reexport */ koquestion_custom_QuestionCustom; });
__webpack_require__.d(__webpack_exports__, "QuestionButtonGroup", function() { return /* reexport */ koquestion_buttongroup_QuestionButtonGroup; });
__webpack_require__.d(__webpack_exports__, "TextAreaViewModel", function() { return /* reexport */ TextAreaViewModel; });
__webpack_require__.d(__webpack_exports__, "ActionBarItemViewModel", function() { return /* reexport */ ActionBarItemViewModel; });
__webpack_require__.d(__webpack_exports__, "ActionBarItemDropdownViewModel", function() { return /* reexport */ ActionBarItemDropdownViewModel; });
__webpack_require__.d(__webpack_exports__, "ActionBarSeparatorViewModel", function() { return /* reexport */ ActionBarSeparatorViewModel; });
__webpack_require__.d(__webpack_exports__, "ActionContainerImplementor", function() { return /* reexport */ action_bar_ActionContainerImplementor; });
__webpack_require__.d(__webpack_exports__, "CheckboxViewModel", function() { return /* reexport */ CheckboxViewModel; });
__webpack_require__.d(__webpack_exports__, "BooleanRadioItemViewModel", function() { return /* reexport */ BooleanRadioItemViewModel; });
__webpack_require__.d(__webpack_exports__, "BooleanRadioViewModel", function() { return /* reexport */ BooleanRadioViewModel; });
__webpack_require__.d(__webpack_exports__, "PanelViewModel", function() { return /* reexport */ PanelViewModel; });
__webpack_require__.d(__webpack_exports__, "PopupViewModel", function() { return /* reexport */ popup_PopupViewModel; });
__webpack_require__.d(__webpack_exports__, "showModal", function() { return /* reexport */ showModal; });
__webpack_require__.d(__webpack_exports__, "showDialog", function() { return /* reexport */ showDialog; });
__webpack_require__.d(__webpack_exports__, "ProgressButtonsViewModel", function() { return /* reexport */ buttons_ProgressButtonsViewModel; });
__webpack_require__.d(__webpack_exports__, "ProgressViewModel", function() { return /* reexport */ progress_ProgressViewModel; });
__webpack_require__.d(__webpack_exports__, "ComponentsContainer", function() { return /* reexport */ ComponentsContainer; });
__webpack_require__.d(__webpack_exports__, "TitleElementViewModel", function() { return /* reexport */ TitleElementViewModel; });
__webpack_require__.d(__webpack_exports__, "TitleContentViewModel", function() { return /* reexport */ TitleContentViewModel; });
__webpack_require__.d(__webpack_exports__, "TitleActionViewModel", function() { return /* reexport */ TitleActionViewModel; });
__webpack_require__.d(__webpack_exports__, "StringEditorViewModel", function() { return /* reexport */ StringEditorViewModel; });
__webpack_require__.d(__webpack_exports__, "StringViewerViewModel", function() { return /* reexport */ StringViewerViewModel; });
__webpack_require__.d(__webpack_exports__, "LogoImageViewModel", function() { return /* reexport */ LogoImageViewModel; });
__webpack_require__.d(__webpack_exports__, "Skeleton", function() { return /* reexport */ Skeleton; });
__webpack_require__.d(__webpack_exports__, "CharacterCounterComponent", function() { return /* reexport */ CharacterCounterComponent; });
__webpack_require__.d(__webpack_exports__, "RatingItemViewComponent", function() { return /* reexport */ RatingItemViewComponent; });
__webpack_require__.d(__webpack_exports__, "RatingDropdownViewModel", function() { return /* reexport */ RatingDropdownViewModel; });
__webpack_require__.d(__webpack_exports__, "RatingItemViewModel", function() { return /* reexport */ RatingItemViewModel; });
__webpack_require__.d(__webpack_exports__, "RatingItemStarViewModel", function() { return /* reexport */ RatingItemStarViewModel; });
__webpack_require__.d(__webpack_exports__, "RatingItemSmileyViewModel", function() { return /* reexport */ RatingItemSmileyViewModel; });
__webpack_require__.d(__webpack_exports__, "DropdownViewModel", function() { return /* reexport */ DropdownViewModel; });
__webpack_require__.d(__webpack_exports__, "DropdownSelectViewModel", function() { return /* reexport */ DropdownSelectViewModel; });
__webpack_require__.d(__webpack_exports__, "TagboxViewComponent", function() { return /* reexport */ TagboxViewComponent; });
__webpack_require__.d(__webpack_exports__, "TagboxViewModel", function() { return /* reexport */ TagboxViewModel; });
__webpack_require__.d(__webpack_exports__, "SurveyFilePreview", function() { return /* reexport */ SurveyFilePreview; });
__webpack_require__.d(__webpack_exports__, "SurveyFilePage", function() { return /* reexport */ SurveyFilePage; });
__webpack_require__.d(__webpack_exports__, "SurveyFileItem", function() { return /* reexport */ SurveyFileItem; });
__webpack_require__.d(__webpack_exports__, "ListItemViewComponent", function() { return /* reexport */ ListItemViewComponent; });
__webpack_require__.d(__webpack_exports__, "ListItemContentViewComponent", function() { return /* reexport */ ListItemContentViewComponent; });
__webpack_require__.d(__webpack_exports__, "ListItemGroupViewComponent", function() { return /* reexport */ ListItemGroupViewComponent; });
__webpack_require__.d(__webpack_exports__, "ListViewComponent", function() { return /* reexport */ ListViewComponent; });
__webpack_require__.d(__webpack_exports__, "SvgIconViewModel", function() { return /* reexport */ SvgIconViewModel; });
__webpack_require__.d(__webpack_exports__, "SurveyQuestionMatrixDynamicRemoveButton", function() { return /* reexport */ SurveyQuestionMatrixDynamicRemoveButton; });
__webpack_require__.d(__webpack_exports__, "SurveyQuestionMatrixDetailButton", function() { return /* reexport */ SurveyQuestionMatrixDetailButton; });
__webpack_require__.d(__webpack_exports__, "SurveyQuestionMatrixDynamicDragDropIcon", function() { return /* reexport */ SurveyQuestionMatrixDynamicDragDropIcon; });
__webpack_require__.d(__webpack_exports__, "ButtonGroupItemViewModel", function() { return /* reexport */ ButtonGroupItemViewModel; });
__webpack_require__.d(__webpack_exports__, "SurveyNavigationButton", function() { return /* reexport */ survey_nav_button_SurveyNavigationButton; });
__webpack_require__.d(__webpack_exports__, "SurveyQuestionPaneldynamicActioons", function() { return /* reexport */ SurveyQuestionPaneldynamicActioons; });
__webpack_require__.d(__webpack_exports__, "BrandInfoComponent", function() { return /* reexport */ BrandInfoComponent; });
__webpack_require__.d(__webpack_exports__, "QuestionErrorComponent", function() { return /* reexport */ QuestionErrorComponent; });
__webpack_require__.d(__webpack_exports__, "NotifierViewModel", function() { return /* reexport */ NotifierViewModel; });
__webpack_require__.d(__webpack_exports__, "LoadingIndicatorViewModel", function() { return /* reexport */ LoadingIndicatorViewModel; });
__webpack_require__.d(__webpack_exports__, "SurveyModel", function() { return /* reexport */ external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"]; });
__webpack_require__.d(__webpack_exports__, "SurveyWindowModel", function() { return /* reexport */ external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyWindowModel"]; });
__webpack_require__.d(__webpack_exports__, "settings", function() { return /* reexport */ external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["settings"]; });
__webpack_require__.d(__webpack_exports__, "surveyLocalization", function() { return /* reexport */ external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["surveyLocalization"]; });
__webpack_require__.d(__webpack_exports__, "surveyStrings", function() { return /* reexport */ external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["surveyStrings"]; });

// EXTERNAL MODULE: external {"root":"ko","commonjs2":"knockout","commonjs":"knockout","amd":"knockout"}
var external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_ = __webpack_require__("knockout");

// EXTERNAL MODULE: external {"root":"Survey","commonjs2":"survey-core","commonjs":"survey-core","amd":"survey-core"}
var external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_ = __webpack_require__("survey-core");

// CONCATENATED MODULE: ./src/knockout/templateText.ts
var koTemplate = __webpack_require__(/*! html-loader?interpolate!val-loader!./templates/entry.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/templates/entry.html");
var SurveyTemplateText = /** @class */ (function () {
    function SurveyTemplateText() {
    }
    SurveyTemplateText.prototype.addText = function (newText, id, name) {
        id = this.getId(id, name);
        this.text =
            this.text +
                '<script type="text/html" ' +
                id +
                ">" +
                newText +
                "</script>";
    };
    SurveyTemplateText.prototype.replaceText = function (replaceText, id, questionType) {
        if (questionType === void 0) { questionType = null; }
        var posId = this.getId(id, questionType);
        var pos = this.text.indexOf(posId);
        if (pos < 0) {
            this.addText(replaceText, id, questionType);
            return;
        }
        pos = this.text.indexOf(">", pos);
        if (pos < 0)
            return;
        var startPos = pos + 1;
        var endString = "</script>";
        pos = this.text.indexOf(endString, startPos);
        if (pos < 0)
            return;
        this.text =
            this.text.substring(0, startPos) + replaceText + this.text.substring(pos);
    };
    SurveyTemplateText.prototype.getId = function (id, questionType) {
        var result = 'id="survey-' + id;
        if (questionType) {
            result += "-" + questionType;
        }
        return result + '"';
    };
    Object.defineProperty(SurveyTemplateText.prototype, "text", {
        get: function () {
            return koTemplate;
        },
        set: function (value) {
            koTemplate = value;
        },
        enumerable: false,
        configurable: true
    });
    return SurveyTemplateText;
}());


// CONCATENATED MODULE: ./src/knockout/kobase.ts

var kobase_ImplementorBase = /** @class */ (function () {
    function ImplementorBase(element) {
        this.element = element;
        this.implementedMark = "__surveyImplementedKo";
        if (element[this.implementedMark]) {
            return;
        }
        element.supportOnElementRerenderedEvent = false;
        element.iteratePropertiesHash(function (hash, key) {
            ImplementorBase.doIterateProperties(element, hash, key);
        });
        element.createArrayCoreHandler = function (hash, key) {
            var res = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observableArray"]();
            res()["onArrayChanged"] = function () {
                if (element.isLoadingFromJson || element.isDisposed)
                    return;
                res.notifySubscribers();
            };
            hash[key] = res;
            return res();
        };
        element.getPropertyValueCoreHandler = function (hash, key) {
            if (hash[key] === undefined) {
                hash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]();
            }
            return typeof hash[key] === "function" ? hash[key]() : hash[key];
        };
        element.setPropertyValueCoreHandler = function (hash, key, val) {
            if (hash[key] !== undefined) {
                // if(hash[key]() === val) {
                //   hash[key].notifySubscribers();
                // }
                hash[key](val);
            }
            else {
                hash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](val);
            }
        };
        element[this.implementedMark] = true;
    }
    ImplementorBase.doIterateProperties = function (element, hash, key) {
        var val = hash[key];
        if (val === "function")
            return;
        if (Array.isArray(val)) {
            hash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observableArray"](val);
            val["onArrayChanged"] = function () {
                if (element.isLoadingFromJson || element.isDisposed)
                    return;
                hash[key].notifySubscribers();
            };
        }
        else {
            hash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](val);
        }
    };
    ImplementorBase.prototype.dispose = function () {
        this.element.iteratePropertiesHash(function (hash, key) {
            hash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](hash[key]);
            if (Array.isArray(hash[key])) {
                hash[key]["onArrayChanged"] = undefined;
            }
        });
        this.element.supportOnElementRerenderedEvent = true;
        this.element.createArrayCoreHandler = undefined;
        this.element.getPropertyValueCoreHandler = undefined;
        this.element.setPropertyValueCoreHandler = undefined;
        delete this.element[this.implementedMark];
    };
    return ImplementorBase;
}());


// CONCATENATED MODULE: ./packages/survey-core/src/iconsV1.ts
var path = __webpack_require__("./packages/survey-core/src/images-v1 sync recursive \\.svg$");
var icons = {};
path.keys().forEach(function (key) {
    icons[key.substring(2, key.length - 4).toLowerCase()] = path(key);
});


// CONCATENATED MODULE: ./packages/survey-core/src/iconsV2.ts
var iconsV2_path = __webpack_require__("./packages/survey-core/src/images-v2 sync recursive \\.svg$");
var iconsV2_icons = {};
iconsV2_path.keys().forEach(function (key) {
    iconsV2_icons[key.substring(2, key.length - 4).toLowerCase()] = iconsV2_path(key);
});


// CONCATENATED MODULE: ./src/knockout/kosurvey.ts
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (undefined && undefined.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
/* eslint-disable no-restricted-globals */











Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["addIconsToThemeSet"])("v1", icons);
Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["addIconsToThemeSet"])("v2", iconsV2_icons);
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SvgRegistry"].registerIcons(icons);
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["CustomWidgetCollection"].Instance.onCustomWidgetAdded.add(function (customWidget) {
    if (customWidget.widgetJson.isDefaultRender)
        return;
    if (!customWidget.htmlTemplate)
        customWidget.htmlTemplate =
            "<div>'htmlTemplate' attribute is missed.</div>";
    new SurveyTemplateText().replaceText(customWidget.htmlTemplate, "widget", customWidget.name);
});
var kosurvey_SurveyImplementor = /** @class */ (function (_super) {
    __extends(SurveyImplementor, _super);
    function SurveyImplementor(survey) {
        var _this = _super.call(this, survey) || this;
        _this.survey = survey;
        _this.survey.valueHashGetDataCallback = function (valuesHash, key) {
            if (valuesHash[key] === undefined) {
                valuesHash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]();
            }
            return external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](valuesHash[key]);
        };
        _this.survey.valueHashSetDataCallback = function (valuesHash, key, value) {
            if (external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["isWriteableObservable"](valuesHash[key])) {
                valuesHash[key](value);
            }
            else {
                valuesHash[key] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](value);
            }
        };
        _this.survey.valueHashDeleteDataCallback = function (valuesHash, key) {
            if (external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["isWriteableObservable"](valuesHash[key])) {
                valuesHash[key](undefined);
            }
            else {
                delete valuesHash[key];
            }
        };
        _this.survey["koTitleTemplate"] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("survey-header");
        _this.survey["koAfterRenderPage"] = function (elements, con) {
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
            if (!el)
                return;
            setTimeout(function () {
                !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
                _this.survey.afterRenderPage(el);
            }, 0);
        };
        _this.survey["koAfterRenderHeader"] = function (elements, con) {
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
            if (el)
                _this.survey.afterRenderHeader(el);
        };
        _this.survey["koProcessedCompletedHtml"] = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](_this.survey.processedCompletedHtml);
        _this.survey.locCompletedHtml["koRenderedHtml"].subscribe(function () {
            _this.survey["koProcessedCompletedHtml"](_this.survey.processedCompletedHtml);
        });
        _this.survey.registerPropertyChangedHandlers(["state"], function () { _this.survey["koProcessedCompletedHtml"](_this.survey.processedCompletedHtml); });
        _this.survey.disposeCallback = function () {
            _this.dispose();
        };
        new kobase_ImplementorBase(_this.survey.timerModel);
        return _this;
    }
    SurveyImplementor.prototype.render = function (element) {
        if (element === void 0) { element = null; }
        if (typeof external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_ === "undefined")
            throw new Error("knockoutjs library is not loaded.");
        var page = this.survey.activePage;
        if (!!page) {
            page.updateCustomWidgets();
        }
        this.survey.updateElementCss(false);
        if (element && typeof element === "string") {
            element = Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getElement"])(element);
        }
        if (element) {
            this.renderedElement = element;
        }
        this.survey.startTimerFromUI();
        this.applyBinding();
    };
    SurveyImplementor.prototype.applyBinding = function () {
        if (!this.renderedElement)
            return;
        external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["cleanNode"](this.renderedElement);
        external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["renderTemplate"]("survey-content", this.survey, {}, this.renderedElement);
    };
    SurveyImplementor.prototype.koEventAfterRender = function (element, survey) {
        survey.afterRenderSurvey(element);
    };
    SurveyImplementor.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        if (!!this.renderedElement) {
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["cleanNode"](this.renderedElement);
            this.renderedElement.innerHTML = "";
            this.renderedElement = undefined;
        }
        this.survey["koAfterRenderPage"] = undefined;
        this.survey["koAfterRenderHeader"] = undefined;
        this.survey.iteratePropertiesHash(function (hash, key) {
            delete hash[key];
        });
    };
    return SurveyImplementor;
}(kobase_ImplementorBase));

// SurveyModel.prototype["onCreating"] = function() {
//   this.implementor = new SurveyImplementor(this);
// };
// SurveyModel.prototype["render"] = function(element: any = null) {
//   this.implementor.render(element);
// };
// SurveyModel.prototype["getHtmlTemplate"] = function(): string {
//   return koTemplate;t
// };
var kosurvey_Survey = /** @class */ (function (_super) {
    __extends(Survey, _super);
    function Survey(jsonObj, renderedElement) {
        if (jsonObj === void 0) { jsonObj = null; }
        if (renderedElement === void 0) { renderedElement = null; }
        var _this = _super.call(this, jsonObj, renderedElement) || this;
        _this.implementor = new kosurvey_SurveyImplementor(_this);
        return _this;
    }
    Survey.prototype.render = function (element) {
        if (element === void 0) { element = null; }
        this.implementor.render(element);
    };
    Survey.prototype.fromJSON = function (json, options) {
        if (!json)
            return;
        _super.prototype.fromJSON.call(this, json, options);
        this.locStrsChanged();
    };
    Survey.prototype.getHtmlTemplate = function () {
        return koTemplate;
    };
    Survey.prototype.makeReactive = function (obj) {
        new kobase_ImplementorBase(obj);
    };
    Survey.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        if (this.implementor) {
            this.implementor.dispose();
            this.implementor = undefined;
        }
    };
    return Survey;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"]));

function ensureSurvey(survey) {
    if (!survey.implementor) {
        survey.implementor = new kosurvey_SurveyImplementor(survey);
        survey.render = function (element) {
            if (element === void 0) { element = null; }
            survey.implementor.render(element);
        };
        survey.getHtmlTemplate = function () {
            return koTemplate;
        };
        survey.makeReactive = function (obj) {
            new kobase_ImplementorBase(obj);
        };
    }
}
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["LocalizableString"].prototype["onCreating"] = function () {
    var self = this;
    this.koHasHtml = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](this.hasHtml);
    this.koRenderedHtml = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](this.renderedHtml);
    this.onStringChanged.add(function () {
        var hasHtml = self.hasHtml;
        self.koHasHtml(hasHtml);
        self.koRenderedHtml(hasHtml ? self.getHtmlValue() : self.calculatedText);
    });
};
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ItemValue"].prototype["onCreating"] = function () {
    var _this = this;
    new kobase_ImplementorBase(this);
    this.koText = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () { return _this.locText.koRenderedHtml(); });
    this.locText.strChanged();
};
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("survey", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var survey = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.survey) || external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.model);
            ensureSurvey(survey);
            setTimeout(function () {
                var surveyRoot = document.createElement("div");
                surveyRoot.style.width = "100%";
                surveyRoot.style.height = "100%";
                componentInfo.element.appendChild(surveyRoot);
                survey.render(surveyRoot);
            }, 1);
            // !!ko.tasks && ko.tasks.runEarly();
            return params.survey;
        },
    },
    template: koTemplate,
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["bindingHandlers"]["surveyProp"] = {
    update: function (element, valueAccessor, allBindingsAccessor) {
        var value = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].unwrapObservable(valueAccessor()) || {};
        for (var propName in value) {
            if (typeof propName == "string") {
                var propValue = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].unwrapObservable(value[propName]);
                element[propName] = propValue;
            }
        }
    },
};
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"].platform = "knockout";
var registerTemplateEngine = function (ko, platform) {
    ko.surveyTemplateEngine = function () { };
    ko.surveyTemplateEngine.prototype = new ko.nativeTemplateEngine();
    ko.surveyTemplateEngine.prototype.makeTemplateSource = function (template, templateDocument) {
        if (typeof template === "string") {
            templateDocument = templateDocument || document;
            var templateElementRoot = templateDocument.getElementById("survey-content-" + platform);
            if (!templateElementRoot) {
                var rootElement = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["settings"].environment.rootElement;
                templateElementRoot = document.createElement("div");
                templateElementRoot.id = "survey-content-" + external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"].platform;
                templateElementRoot.style.display = "none";
                templateElementRoot.innerHTML = koTemplate;
                rootElement.appendChild(templateElementRoot);
            }
            var elem;
            for (var i = 0; i < templateElementRoot.children.length; i++) {
                if (templateElementRoot.children[i].id === template) {
                    elem = templateElementRoot.children[i];
                    break;
                }
            }
            if (!elem) {
                elem = templateDocument.getElementById(template);
            }
            if (!elem) {
                return new ko.nativeTemplateEngine().makeTemplateSource(template, templateDocument);
            }
            return new ko.templateSources.domElement(elem);
        }
        else if (template.nodeType === 1 || template.nodeType === 8) {
            return new ko.templateSources.anonymousTemplate(template);
        }
        else {
            throw new Error("Unknown template type: " + template);
        }
    };
    // (<any>ko).surveyTemplateEngine.prototype.renderTemplateSource = function (templateSource: any, bindingContext: any, options: any, templateDocument: any) {
    //   var useNodesIfAvailable = !((<any>ko.utils).ieVersion < 9),
    //     templateNodesFunc = useNodesIfAvailable ? templateSource["nodes"] : null,
    //     templateNodes = templateNodesFunc ? templateSource["nodes"]() : null;
    //   if (templateNodes) {
    //     return (<any>ko.utils).makeArray(templateNodes.cloneNode(true).childNodes);
    //   } else {
    //     var templateText = templateSource["text"]();
    //     return (<any>ko.utils).parseHtmlFragment(templateText, templateDocument);
    //   }
    // };
    var surveyTemplateEngineInstance = new ko.surveyTemplateEngine();
    ko.setTemplateEngine(surveyTemplateEngineInstance);
};
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["bindingHandlers"]["elementStyle"] = {
    update: function (element, valueAccessor, allBindings) {
        if (element && element.style.length) {
            for (var index = element.style.length - 1; index >= 0; index--) {
                var style = element.style[index];
                if (style && style.indexOf("--sjs-") === 0) {
                    element.style.removeProperty(style);
                }
            }
        }
        var value = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].unwrapObservable(valueAccessor()) || {};
        Object.keys(value).forEach(function (key) {
            if (key.indexOf("--") === 0) {
                element.style.setProperty(key, value[key]);
            }
            else {
                element.style[key] = value[key];
            }
        });
    }
};
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["bindingHandlers"]["key2click"] = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var options = __assign({}, valueAccessor()) || {
            processEsc: true,
            disableTabStop: false
        };
        if ((!!viewModel && viewModel.disableTabStop) || (!!options && options.disableTabStop)) {
            element.tabIndex = -1;
            return;
        }
        element.tabIndex = 0;
        element.onkeyup = function (evt) {
            evt.preventDefault();
            evt.stopPropagation();
            Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["doKey2ClickUp"])(evt, options);
            return false;
        };
        element.onkeydown = function (evt) { return Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["doKey2ClickDown"])(evt, options); };
        element.onblur = function (evt) { return Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["doKey2ClickBlur"])(evt); };
    },
};

// CONCATENATED MODULE: ./src/knockout/koPopupSurvey.ts
var koPopupSurvey_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koPopupSurvey_koTemplate = __webpack_require__(/*! html-loader?interpolate!val-loader!./templates/window.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/templates/window.html");
var koPopupSurvey_PopupSurveyImplementor = /** @class */ (function (_super) {
    koPopupSurvey_extends(PopupSurveyImplementor, _super);
    function PopupSurveyImplementor(window) {
        var _this = _super.call(this, window) || this;
        _this.window = window;
        _this.window.showingChangedCallback = function () {
            _this.doShowingChanged();
        };
        _this.window["doExpand"] = function () {
            _this.window.changeExpandCollapse();
        };
        _this.window["doHide"] = function () {
            _this.window.hide();
        };
        _this.window["doToggleFullScreen"] = function () {
            _this.window.toggleFullScreen();
        };
        return _this;
    }
    PopupSurveyImplementor.prototype.doShowingChanged = function () {
        var windowElement = this.window.windowElement;
        var rootElement = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["settings"].environment.rootElement;
        if (this.window.isShowing) {
            windowElement.innerHTML = this.template;
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["cleanNode"](windowElement);
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["applyBindings"](this.window, windowElement);
            rootElement.appendChild(windowElement);
        }
        else {
            rootElement.removeChild(windowElement);
            windowElement.innerHTML = "";
        }
    };
    Object.defineProperty(PopupSurveyImplementor.prototype, "template", {
        get: function () {
            return this.window.templateValue ? this.window.templateValue : koPopupSurvey_koTemplate;
        },
        enumerable: false,
        configurable: true
    });
    return PopupSurveyImplementor;
}(kobase_ImplementorBase));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["PopupSurveyModel"].prototype["onCreating"] = function () {
    this.implementor = new koPopupSurvey_PopupSurveyImplementor(this);
};
var PopupSurvey = /** @class */ (function (_super) {
    koPopupSurvey_extends(PopupSurvey, _super);
    function PopupSurvey(jsonObj, initialModel) {
        if (initialModel === void 0) { initialModel = null; }
        return _super.call(this, jsonObj, initialModel) || this;
    }
    return PopupSurvey;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["PopupSurveyModel"]));

var SurveyWindow = /** @class */ (function (_super) {
    koPopupSurvey_extends(SurveyWindow, _super);
    function SurveyWindow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return SurveyWindow;
}(PopupSurvey));


// CONCATENATED MODULE: ./src/knockout/kopage.ts
var kopage_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();







var kopage_QuestionRow = /** @class */ (function (_super) {
    kopage_extends(QuestionRow, _super);
    function QuestionRow(panel) {
        var _this = _super.call(this, panel) || this;
        _this.panel = panel;
        new kobase_ImplementorBase(_this);
        var self = _this;
        _this.koElementAfterRender = function (el, renderedElement) {
            return self.elementAfterRender(el, renderedElement);
        };
        return _this;
    }
    QuestionRow.prototype.getElementType = function (el) {
        return el.isPanel ? "survey-panel" : "survey-question";
    };
    QuestionRow.prototype.koAfterRender = function (htmlElements, element) {
        for (var i = 0; i < htmlElements.length; i++) {
            var tEl = htmlElements[i];
            var nName = tEl.nodeName;
            if (nName == "#text")
                tEl.data = "";
            else {
                element.setWrapperElement(tEl);
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(tEl, function () {
                    element.setWrapperElement(undefined);
                });
            }
        }
    };
    QuestionRow.prototype.elementAfterRender = function (elements, renderedElement) {
        if (!this.panel || !this.panel.survey)
            return;
        setTimeout(function () {
            !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
            if (!el)
                return;
            var element = renderedElement;
            if (element.isDisposed)
                return;
            if (element.isPanel) {
                element.afterRender(el);
            }
            else {
                element.afterRender(el);
            }
        }, 0);
    };
    QuestionRow.prototype.rowAfterRender = function (elements, model) {
        var rowContainerDiv = elements[0].parentElement;
        model.setRootElement(rowContainerDiv);
        external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(rowContainerDiv, function () {
            model.setRootElement(undefined);
        });
        if (!model.isNeedRender) {
            var timer_1 = setTimeout(function () { return model.startLazyRendering(rowContainerDiv); }, 1);
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(rowContainerDiv, function () {
                clearTimeout(timer_1);
                model.stopLazyRendering();
                if (!model.isDisposed) {
                    model.isNeedRender = !model.isLazyRendering();
                }
            });
        }
    };
    QuestionRow.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        this.koElementAfterRender = undefined;
    };
    return QuestionRow;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionRowModel"]));

var PanelImplementorBase = /** @class */ (function (_super) {
    kopage_extends(PanelImplementorBase, _super);
    function PanelImplementorBase(panel) {
        var _this = _super.call(this, panel) || this;
        _this.panel = panel;
        return _this;
    }
    return PanelImplementorBase;
}(kobase_ImplementorBase));

var kopage_Panel = /** @class */ (function (_super) {
    kopage_extends(Panel, _super);
    function Panel(name) {
        if (name === void 0) { name = ""; }
        var _this = _super.call(this, name) || this;
        _this.onCreating();
        _this.koElementType = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("survey-panel");
        return _this;
    }
    Panel.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new PanelImplementorBase(this);
    };
    Panel.prototype.createRow = function () {
        return new kopage_QuestionRow(this);
    };
    Panel.prototype.onCreating = function () { };
    Panel.prototype.onNumChanged = function (value) {
        this.locTitle.strChanged();
    };
    Panel.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return Panel;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["PanelModel"]));

var kopage_Page = /** @class */ (function (_super) {
    kopage_extends(Page, _super);
    function Page(name) {
        if (name === void 0) { name = ""; }
        var _this = _super.call(this, name) || this;
        _this.onCreating();
        _this.koElementType = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("survey-panel");
        return _this;
    }
    Page.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new kobase_ImplementorBase(this);
    };
    Page.prototype.createRow = function () {
        return new kopage_QuestionRow(this);
    };
    Page.prototype.onCreating = function () { };
    Page.prototype.onNumChanged = function (value) {
        this.locTitle.strChanged();
    };
    Page.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        this._implementor.dispose();
        this._implementor = undefined;
    };
    return Page;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["PageModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("panel", function () {
    return new kopage_Panel();
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("page", function () {
    return new kopage_Page();
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ElementFactory"].Instance.registerElement("panel", function (name) {
    return new kopage_Panel(name);
});

// CONCATENATED MODULE: ./src/knockout/koflowpanel.ts
var koflowpanel_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
/* eslint-disable no-restricted-globals */





var koflowpanel_FlowPanel = /** @class */ (function (_super) {
    koflowpanel_extends(FlowPanel, _super);
    function FlowPanel(name) {
        if (name === void 0) { name = ""; }
        var _this = _super.call(this, name) || this;
        _this.koElementType = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("survey-flowpanel");
        new kobase_ImplementorBase(_this);
        _this.onCreating();
        var self = _this;
        _this.koElementAfterRender = function (el, con) {
            return self.elementAfterRender(el, con);
        };
        return _this;
    }
    FlowPanel.prototype.onCreating = function () { };
    FlowPanel.prototype.getHtmlForQuestion = function (question) {
        return ('<span question="true" contenteditable="false" id="flowpanel_' +
            question.name +
            '"><!-- ko template: { name: "survey-flowpanel-question", data: "' +
            question.name +
            '"} --><!-- /ko --></span>');
    };
    FlowPanel.prototype.elementAfterRender = function (elements, con) {
        if (!this.survey)
            return;
        var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
        if (!!el) {
            this.survey.afterRenderQuestion(con, el);
        }
    };
    return FlowPanel;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["FlowPanelModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("flowpanel", function () {
    return new koflowpanel_FlowPanel();
});
/*
ElementFactory.Instance.registerElement("flowpanel", name => {
  return new FlowPanel(name);
});
*/
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("f-panel", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var self = this;
            var question = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.question);
            self.element = componentInfo.element;
            self.element.innerHTML = question.html;
            self.isOnFocus = false;
            self.wasChanged = false;
            self.isContentUpdating = false;
            question.contentChangedCallback = function () {
                if (self.isContentUpdating)
                    return;
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["cleanNode"](self.element);
                self.element.innerHTML = question.html;
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["applyBindings"]({ question: question }, self.element);
                !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
            };
            self.element.onfocus = function () {
                self.isOnFocus = true;
            };
            self.element.onblur = function () {
                if (self.wasChanged)
                    self.updateContent();
                self.isOnFocus = false;
                self.wasChanged = false;
            };
            self.element.ondragend = function (event) {
                var regEx = /{(.*?(element:)[^$].*?)}/g;
                var str = self.element.innerHTML;
                var res = regEx.exec(str);
                if (res !== null) {
                    var q = question.getQuestionFromText(res[0]);
                    if (!!q) {
                        question.content = self.getContent(q.name);
                    }
                }
            };
            self.updateContent = function () {
                self.isContentUpdating = true;
                question.content = self.getContent();
                self.isContentUpdating = false;
            };
            question.getContent = self.getContent = function (deletedName) {
                var content = document.createElement("div");
                content.innerHTML = self.element.innerHTML;
                var cps = content.querySelectorAll('span[question="true"]');
                for (var i = 0; i < cps.length; i++) {
                    var name = cps[i].id.replace("flowpanel_", "");
                    var html = "";
                    if (name !== deletedName) {
                        var el = question.getQuestionByName(name);
                        html = !!el ? question.getElementContentText(el) : "";
                    }
                    cps[i].outerHTML = html;
                }
                return content.innerHTML;
            };
            var config = {
                characterData: true,
                attributes: true,
                childList: true,
                subtree: true,
            };
            var callback = function (mutationsList, observer) {
                if (!self.isOnFocus)
                    return;
                self.wasChanged = true;
            };
            var observer = new MutationObserver(callback);
            observer.observe(self.element, config);
            return { question: question };
        },
    },
    template: "<div></div>",
});

// CONCATENATED MODULE: ./src/knockout/koquestion.ts
var koquestion_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_QuestionImplementor = /** @class */ (function (_super) {
    koquestion_extends(QuestionImplementor, _super);
    function QuestionImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.question = question;
        _this._koValue = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observableArray"]();
        _this.disposedObjects = [];
        _this.callBackFunctions = [];
        var isSynchronizing = false;
        _this._koValue.subscribe(function (newValue) {
            if (!isSynchronizing) {
                _this.setKoValue(newValue);
            }
        });
        Object.defineProperty(_this.question, "koValue", {
            get: function () {
                if (!external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Helpers"].isTwoValueEquals(_this._koValue(), _this.getKoValue(), false, true, false)) {
                    try {
                        isSynchronizing = true;
                        _this._koValue(_this.getKoValue());
                    }
                    finally {
                        isSynchronizing = false;
                    }
                }
                return _this._koValue;
            },
            enumerable: true,
            configurable: true,
        });
        question.surveyLoadCallback = function () {
            _this.onSurveyLoad();
        };
        _this.setObservaleObj("koTemplateName", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            return _this.getTemplateName();
        }));
        _this.setObservaleObj("koElementType", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("survey-question"));
        _this.koDummy = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.setCallbackFunc("koQuestionAfterRender", function (el, con) {
            _this.koQuestionAfterRender(el, con);
        });
        _this.setCallbackFunc("koMouseDown", function () {
            _this.question.onMouseDown();
            return true;
        });
        return _this;
    }
    QuestionImplementor.prototype.setObservaleObj = function (name, obj, addToQuestion) {
        if (addToQuestion === void 0) { addToQuestion = true; }
        this.disposedObjects.push(name);
        if (addToQuestion) {
            this.question[name] = obj;
        }
        return obj;
    };
    QuestionImplementor.prototype.setCallbackFunc = function (name, func) {
        this.callBackFunctions.push(name);
        this.question[name] = func;
    };
    QuestionImplementor.prototype.getKoValue = function () {
        return this.question.value;
    };
    QuestionImplementor.prototype.setKoValue = function (val) {
        if (this.question.isReadOnlyAttr)
            return;
        this.question.value = val;
    };
    QuestionImplementor.prototype.onSurveyLoad = function () { };
    QuestionImplementor.prototype.getQuestionTemplate = function () {
        return this.question.getTemplate();
    };
    QuestionImplementor.prototype.getTemplateName = function () {
        if (!!this.question &&
            this.question.customWidget &&
            !this.question.customWidget.widgetJson.isDefaultRender)
            return "survey-widget-" + this.question.customWidget.name;
        return "survey-question-" + this.getQuestionTemplate();
    };
    QuestionImplementor.prototype.getNo = function () {
        return this.question.visibleIndex > -1
            ? this.question.visibleIndex + 1 + ". "
            : "";
    };
    QuestionImplementor.prototype.updateKoDummy = function () {
        if (this.question.isDisposed)
            return;
        this.koDummy(this.koDummy() + 1);
        this.question.locTitle.strChanged();
    };
    QuestionImplementor.prototype.koQuestionAfterRender = function (elements, con) {
        var _this = this;
        setTimeout(function () {
            !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements, true);
            if (!!el) {
                _this.question.afterRenderQuestionElement(el);
                if (!!_this.question && !!_this.question.customWidget) {
                    _this.question.customWidget.afterRender(_this.question, el);
                }
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(el, function () {
                    _this.question.beforeDestroyQuestionElement(el);
                    if (!!_this.question && !!_this.question.customWidget) {
                        try {
                            _this.question.customWidget.willUnmount(_this.question, el);
                        }
                        catch (_a) {
                            // eslint-disable-next-line no-console
                            console.warn("Custom widget will unmount failed");
                        }
                    }
                });
            }
        }, 0);
    };
    QuestionImplementor.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        for (var i_1 = 0; i_1 < this.disposedObjects.length; i_1++) {
            var name_1 = this.disposedObjects[i_1];
            var obj = this[name_1] || this.question[name_1];
            if (!obj)
                continue;
            if (this[name_1])
                this[name_1] = undefined;
            if (this.question[name_1])
                this.question[name_1] = undefined;
            if (obj["dispose"])
                obj.dispose();
        }
        this.disposedObjects = [];
        for (var i = 0; i < this.callBackFunctions.length; i++) {
            this.question[this.callBackFunctions[i]] = undefined;
        }
        this.callBackFunctions = [];
        this.question.unregisterPropertyChangedHandlers(["visibleIndex"]);
    };
    return QuestionImplementor;
}(kobase_ImplementorBase));


// CONCATENATED MODULE: ./src/knockout/koquestion_baseselect.ts
var koquestion_baseselect_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();

var QuestionSelectBaseImplementor = /** @class */ (function (_super) {
    koquestion_baseselect_extends(QuestionSelectBaseImplementor, _super);
    function QuestionSelectBaseImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.onCreated();
        return _this;
    }
    QuestionSelectBaseImplementor.prototype.onCreated = function () { };
    Object.defineProperty(QuestionSelectBaseImplementor.prototype, "isOtherSelected", {
        get: function () {
            return this.question.isOtherSelected;
        },
        enumerable: false,
        configurable: true
    });
    return QuestionSelectBaseImplementor;
}(koquestion_QuestionImplementor));

var QuestionCheckboxBaseImplementor = /** @class */ (function (_super) {
    koquestion_baseselect_extends(QuestionCheckboxBaseImplementor, _super);
    function QuestionCheckboxBaseImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.setCallbackFunc("koAfterRender", _this.koAfterRender);
        return _this;
    }
    QuestionCheckboxBaseImplementor.prototype.koAfterRender = function (el, con) {
        var tEl = el[0];
        if (tEl.nodeName == "#text")
            tEl.data = "";
        tEl = el[el.length - 1];
        if (tEl.nodeName == "#text")
            tEl.data = "";
    };
    return QuestionCheckboxBaseImplementor;
}(QuestionSelectBaseImplementor));


// CONCATENATED MODULE: ./src/knockout/koquestion_checkbox.ts
var koquestion_checkbox_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();





var QuestionCheckboxImplementor = /** @class */ (function (_super) {
    koquestion_checkbox_extends(QuestionCheckboxImplementor, _super);
    function QuestionCheckboxImplementor(question) {
        return _super.call(this, question) || this;
    }
    QuestionCheckboxImplementor.prototype.getKoValue = function () {
        return this.question.renderedValue;
    };
    QuestionCheckboxImplementor.prototype.setKoValue = function (val) {
        this.question.renderedValue = val;
    };
    return QuestionCheckboxImplementor;
}(QuestionCheckboxBaseImplementor));

var koquestion_checkbox_QuestionCheckbox = /** @class */ (function (_super) {
    koquestion_checkbox_extends(QuestionCheckbox, _super);
    function QuestionCheckbox(name) {
        var _this = _super.call(this, name) || this;
        _this._selectAllItemImpl = undefined;
        _this._otherItemImpl = undefined;
        _this._selectAllItemImpl = new kobase_ImplementorBase(_this.selectAllItem);
        _this._otherItemImpl = new kobase_ImplementorBase(_this.otherItem);
        return _this;
    }
    QuestionCheckbox.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionCheckboxImplementor(this);
    };
    QuestionCheckbox.prototype.dispose = function () {
        if (this._selectAllItemImpl) {
            this._selectAllItemImpl.dispose();
            this._selectAllItemImpl = undefined;
        }
        if (this._otherItemImpl) {
            this._otherItemImpl.dispose();
            this._otherItemImpl = undefined;
        }
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionCheckbox;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionCheckboxModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("checkbox", function () {
    return new koquestion_checkbox_QuestionCheckbox("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("checkbox", function (name) {
    var q = new koquestion_checkbox_QuestionCheckbox(name);
    q.choices = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_tagbox.ts
var koquestion_tagbox_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();





/*
export class QuestionCheckboxImplementor extends QuestionCheckboxBaseImplementor {
  constructor(question: Question) {
    super(question);
  }
  protected getKoValue() {
    return this.question.renderedValue;
  }
}
 */
var koquestion_tagbox_QuestionTagbox = /** @class */ (function (_super) {
    koquestion_tagbox_extends(QuestionTagbox, _super);
    function QuestionTagbox(name) {
        var _this = _super.call(this, name) || this;
        _this.isAllSelectedUpdating = false;
        _this.koAllSelected = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](_this.isAllSelected);
        _this.koAllSelected.subscribe(function (newValue) {
            if (_this.isAllSelectedUpdating)
                return;
            if (newValue)
                _this.selectAll();
            else
                _this.clearValue(true);
        });
        return _this;
    }
    QuestionTagbox.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionCheckboxBaseImplementor(this);
    };
    QuestionTagbox.prototype.onSurveyValueChanged = function (newValue) {
        _super.prototype.onSurveyValueChanged.call(this, newValue);
        this.updateAllSelected();
    };
    QuestionTagbox.prototype.onVisibleChoicesChanged = function () {
        _super.prototype.onVisibleChoicesChanged.call(this);
        this.updateAllSelected();
    };
    QuestionTagbox.prototype.updateAllSelected = function () {
        this.isAllSelectedUpdating = true;
        this.koAllSelected(this.isAllSelected);
        this.isAllSelectedUpdating = false;
    };
    QuestionTagbox.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        this.koAllSelected = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionTagbox;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionTagboxModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("tagbox", function () {
    return new koquestion_tagbox_QuestionTagbox("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("tagbox", function (name) {
    var q = new koquestion_tagbox_QuestionTagbox(name);
    q.choices = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/components/ranking/item-content.ts

var item_content_template = __webpack_require__(/*! ./item-content.html */ "./src/knockout/components/ranking/item-content.html");
var RankingItemContenViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-ranking-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        },
    },
    template: item_content_template,
});

// CONCATENATED MODULE: ./src/knockout/koquestion_ranking.ts
var koquestion_ranking_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_ranking_QuestionRanking = /** @class */ (function (_super) {
    koquestion_ranking_extends(QuestionRanking, _super);
    function QuestionRanking() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.koHandleKeydown = function (data, event) {
            _this.handleKeydown(event, data);
            return true;
        };
        _this.koHandlePointerDown = function (data, event) {
            if (!_this.survey.isDesignMode)
                event.preventDefault();
            _this.handlePointerDown(event, data, event.currentTarget);
            return true;
        };
        _this.koHandlePointerUp = function (data, event) {
            if (!_this.survey.isDesignMode)
                event.preventDefault();
            _this.handlePointerUp(event, data, event.currentTarget);
            return true;
        };
        return _this;
    }
    QuestionRanking.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionRanking.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionRanking;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionRankingModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("ranking", function () {
    return new koquestion_ranking_QuestionRanking("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("ranking", function (name) {
    var q = new koquestion_ranking_QuestionRanking(name);
    q.choices = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_comment.ts
var koquestion_comment_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();




var koquestion_comment_QuestionComment = /** @class */ (function (_super) {
    koquestion_comment_extends(QuestionComment, _super);
    function QuestionComment(name) {
        return _super.call(this, name) || this;
    }
    QuestionComment.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionComment.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionComment;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionCommentModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("comment", function () {
    return new koquestion_comment_QuestionComment("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("comment", function (name) {
    return new koquestion_comment_QuestionComment(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_dropdown.ts
var koquestion_dropdown_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();





var QuestionDropdownImplementor = /** @class */ (function (_super) {
    koquestion_dropdown_extends(QuestionDropdownImplementor, _super);
    function QuestionDropdownImplementor(question) {
        return _super.call(this, question) || this;
    }
    return QuestionDropdownImplementor;
}(QuestionSelectBaseImplementor));
var koquestion_dropdown_QuestionDropdown = /** @class */ (function (_super) {
    koquestion_dropdown_extends(QuestionDropdown, _super);
    function QuestionDropdown(name) {
        var _this = _super.call(this, name) || this;
        _this.koDisableOption = function (option, item) {
            if (!item)
                return;
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["applyBindingsToNode"](option, { disable: external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () { return !item.isEnabled; }) }, item);
        };
        return _this;
    }
    QuestionDropdown.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionDropdownImplementor(this);
    };
    QuestionDropdown.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionDropdown;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionDropdownModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("dropdown", function () {
    return new koquestion_dropdown_QuestionDropdown("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("dropdown", function (name) {
    var q = new koquestion_dropdown_QuestionDropdown(name);
    q.choices = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_file.ts
var koquestion_file_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_file_QuestionFileImplementor = /** @class */ (function (_super) {
    koquestion_file_extends(QuestionFileImplementor, _super);
    function QuestionFileImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.koRecalc = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.setObservaleObj("koState", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]("empty"));
        _this.setObservaleObj("koHasValue", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () { return _this.question.koState() === "loaded"; }));
        _this.setObservaleObj("koData", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () {
            if (_this.question.koHasValue()) {
                return _this.question.previewValue;
            }
            return [];
        }));
        _this.setObservaleObj("ko", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"]());
        _this.setObservaleObj("koInputTitle", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () {
            _this.koRecalc();
            return _this.question.inputTitle;
        }));
        _this.setObservaleObj("koChooseFileCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            return _this.question.getChooseFileCss();
        }));
        _this.setCallbackFunc("koGetChooseButtonText", function () {
            _this.question.koState();
            return _this.question.chooseButtonText;
        });
        _this.setCallbackFunc("ondrop", function (data, event) {
            _this.question.onDrop(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("ondragover", function (data, event) {
            _this.question.onDragOver(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("ondragenter", function (data, event) {
            _this.question.onDragEnter(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("ondragleave", function (data, event) {
            _this.question.onDragLeave(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("dochange", function (data, event) {
            _this.question.doChange(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("doclean", function (data, event) {
            _this.question.doClean(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
        });
        _this.setCallbackFunc("doremovefile", function (data, event) {
            _this.question.doRemoveFile(data, event);
        });
        _this.setCallbackFunc("dodownload", function (data, event) {
            _this.question.doDownloadFile(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event), data);
            return true;
        });
        _this.setCallbackFunc("dodownloadFromContainer", function (data, event) {
            _this.question.doDownloadFileFromContainer(Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event), data);
            return true;
        });
        return _this;
    }
    return QuestionFileImplementor;
}(koquestion_QuestionImplementor));
var QuestionFile = /** @class */ (function (_super) {
    koquestion_file_extends(QuestionFile, _super);
    function QuestionFile(name) {
        var _this = _super.call(this, name) || this;
        _this.updateState = function (sender, options) {
            _this.koState(options.state);
            _this._implementor.koRecalc(_this._implementor.koRecalc() + 1);
        };
        _this.onUploadStateChanged.add(_this.updateState);
        _this.updateState(_this, { state: _this.currentState });
        return _this;
    }
    QuestionFile.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_file_QuestionFileImplementor(this);
    };
    QuestionFile.prototype.dispose = function () {
        this.onUploadStateChanged.remove(this.updateState);
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionFile;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFileModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("file", function () {
    return new QuestionFile("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("file", function (name) {
    return new QuestionFile(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_html.ts
var koquestion_html_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();




var koquestion_html_QuestionHtml = /** @class */ (function (_super) {
    koquestion_html_extends(QuestionHtml, _super);
    function QuestionHtml(name) {
        return _super.call(this, name) || this;
    }
    QuestionHtml.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionHtml.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionHtml;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionHtmlModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("html", function () {
    return new koquestion_html_QuestionHtml("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("html", function (name) {
    return new koquestion_html_QuestionHtml(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_matrix.ts
var koquestion_matrix_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();






var koquestion_matrix_QuestionMatrix = /** @class */ (function (_super) {
    koquestion_matrix_extends(QuestionMatrix, _super);
    function QuestionMatrix(name) {
        var _this = _super.call(this, name) || this;
        _this.koVisibleRows = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observableArray"]();
        _this.koVisibleColumns = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observableArray"]();
        _this.koVisibleRows(_this.visibleRows);
        _this.koVisibleColumns(_this.visibleColumns);
        return _this;
    }
    QuestionMatrix.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionMatrix.prototype.onColumnsChanged = function () {
        _super.prototype.onColumnsChanged.call(this);
        this.koVisibleColumns(this.visibleColumns);
    };
    QuestionMatrix.prototype.onRowsChanged = function () {
        _super.prototype.onRowsChanged.call(this);
        this.koVisibleRows(this.visibleRows);
    };
    QuestionMatrix.prototype.onSurveyLoad = function () {
        _super.prototype.onSurveyLoad.call(this);
        this.onRowsChanged();
    };
    QuestionMatrix.prototype.onMatrixRowCreated = function (row) {
        new kobase_ImplementorBase(row);
    };
    QuestionMatrix.prototype.getVisibleRows = function () {
        var rows = _super.prototype.getVisibleRows.call(this);
        this.koVisibleRows(rows);
        return rows;
    };
    QuestionMatrix.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        this.koVisibleRows = undefined;
        this.koVisibleColumns = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionMatrix;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("matrix", function () {
    return new koquestion_matrix_QuestionMatrix("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("matrix", function (name) {
    var q = new koquestion_matrix_QuestionMatrix(name);
    q.rows = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultRows;
    q.columns = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultColums;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_matrixdropdown.ts
var koquestion_matrixdropdown_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();








var koquestion_matrixdropdown_QuestionMatrixBaseImplementor = /** @class */ (function (_super) {
    koquestion_matrixdropdown_extends(QuestionMatrixBaseImplementor, _super);
    function QuestionMatrixBaseImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.koRecalc = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.matrix.onRenderedTableCreatedCallback = function (table) {
            if (!!_this._tableImplementor) {
                _this._tableImplementor.dispose();
            }
            _this._tableImplementor = new kobase_ImplementorBase(table);
        };
        _this.matrix.onRenderedTableResetCallback = function () {
            if (_this.question.isDisposed)
                return;
            _this.koRecalc(_this.koRecalc() + 1);
        };
        _this.matrix.onAddColumn = function (column) {
            new kobase_ImplementorBase(column);
        };
        _this.setObservaleObj("koTable", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.matrix.renderedTable;
        }));
        _this.setCallbackFunc("koCellAfterRender", function (el, con) {
            return _this.cellAfterRender(el, con);
        });
        _this.setCallbackFunc("koCellQuestionAfterRender", function (el, con) {
            return _this.cellQuestionAfterRender(el, con);
        });
        _this.setCallbackFunc("koAddRowClick", function () {
            _this.addRow();
        });
        _this.setCallbackFunc("koRemoveRowClick", function (data) {
            _this.removeRow(data.row);
        });
        _this.setCallbackFunc("koPanelAfterRender", function (el, con) {
            _this.panelAfterRender(el, con);
        });
        _this.setCallbackFunc("koRowAfterRender", function (htmlElements, element) {
            for (var i = 0; i < htmlElements.length; i++) {
                var tEl = htmlElements[i];
                var nName = tEl.nodeName;
                if (nName !== "#text" && nName !== "#comment") {
                    element.setRootElement(tEl);
                    external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(tEl, function () {
                        element.setRootElement(undefined);
                    });
                }
            }
        });
        return _this;
    }
    Object.defineProperty(QuestionMatrixBaseImplementor.prototype, "matrix", {
        get: function () { return this.question; },
        enumerable: false,
        configurable: true
    });
    QuestionMatrixBaseImplementor.prototype.cellAfterRender = function (elements, con) {
        var _this = this;
        if (!this.question.survey)
            return;
        setTimeout(function () {
            !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
            if (!el)
                return;
            var cell = con;
            if (!cell || !_this.question || !_this.question.survey || _this.question.isDisposed)
                return;
            var options = {
                cell: cell.cell,
                cellQuestion: cell.question,
                htmlElement: el,
                row: cell.row,
                column: !!cell.cell ? cell.cell.column : null,
            };
            _this.question.survey.matrixAfterCellRender(_this.question, options);
            if (cell.question) {
                cell.question.afterRenderCore(el);
            }
        }, 0);
    };
    QuestionMatrixBaseImplementor.prototype.cellQuestionAfterRender = function (elements, con) {
        if (!this.question || !this.question.survey)
            return;
        setTimeout(function () {
            !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
            var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
            if (!el)
                return;
            var cell = con;
            if (!cell)
                return;
            var question = cell.question;
            if (!question || !question.survey || question.isDisposed)
                return;
            if (question.customWidget) {
                question.customWidget.afterRender(cell.question, el);
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(el, function () {
                    question.customWidget.willUnmount(cell.question, el);
                });
            }
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["utils"].domNodeDisposal.addDisposeCallback(el, function () {
                question.beforeDestroyQuestionElement(el);
            });
            question.afterRenderQuestionElement(el);
        }, 0);
    };
    QuestionMatrixBaseImplementor.prototype.isAddRowTop = function () {
        return false;
    };
    QuestionMatrixBaseImplementor.prototype.isAddRowBottom = function () {
        return false;
    };
    QuestionMatrixBaseImplementor.prototype.addRow = function () { };
    QuestionMatrixBaseImplementor.prototype.removeRow = function (row) { };
    QuestionMatrixBaseImplementor.prototype.panelAfterRender = function (elements, con) {
        if (!this.question || !this.question.survey)
            return;
        var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
        this.question.survey.afterRenderPanel(con, el);
    };
    QuestionMatrixBaseImplementor.prototype.dispose = function () {
        if (!!this._tableImplementor) {
            this._tableImplementor.dispose();
        }
        this.matrix.onRenderedTableCreatedCallback = undefined;
        this.matrix.onRenderedTableResetCallback = undefined;
        this.matrix.onAddColumn = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionMatrixBaseImplementor;
}(koquestion_QuestionImplementor));

var QuestionMatrixDropdown = /** @class */ (function (_super) {
    koquestion_matrixdropdown_extends(QuestionMatrixDropdown, _super);
    function QuestionMatrixDropdown(name) {
        return _super.call(this, name) || this;
    }
    QuestionMatrixDropdown.prototype.createRenderedTable = function () {
        return new koquestion_matrixdropdown_KoQuestionMatrixDropdownRenderedTable(this);
    };
    QuestionMatrixDropdown.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_matrixdropdown_QuestionMatrixBaseImplementor(this);
    };
    QuestionMatrixDropdown.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        this._implementor.dispose();
        this._implementor = undefined;
    };
    return QuestionMatrixDropdown;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDropdownModel"]));

var koquestion_matrixdropdown_KoQuestionMatrixDropdownRenderedTable = /** @class */ (function (_super) {
    koquestion_matrixdropdown_extends(KoQuestionMatrixDropdownRenderedTable, _super);
    function KoQuestionMatrixDropdownRenderedTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    KoQuestionMatrixDropdownRenderedTable.prototype.createRenderedRow = function (cssClasses, isDetailRow) {
        if (isDetailRow === void 0) { isDetailRow = false; }
        var renderedRow = new external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDropdownRenderedRow"](cssClasses, isDetailRow);
        new kobase_ImplementorBase(renderedRow);
        return renderedRow;
    };
    KoQuestionMatrixDropdownRenderedTable.prototype.createErrorRenderedRow = function (cssClasses) {
        var res = _super.prototype.createErrorRenderedRow.call(this, cssClasses);
        new kobase_ImplementorBase(res);
        return res;
    };
    return KoQuestionMatrixDropdownRenderedTable;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDropdownRenderedTable"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("matrixdropdown", function () {
    return new QuestionMatrixDropdown("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("matrixdropdown", function (name) {
    var q = new QuestionMatrixDropdown(name);
    q.choices = [1, 2, 3, 4, 5];
    q.rows = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultRows;
    external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDropdownModelBase"].addDefaultColumns(q);
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_matrixdynamic.ts
var koquestion_matrixdynamic_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();






var koquestion_matrixdynamic_QuestionMatrixDynamicImplementor = /** @class */ (function (_super) {
    koquestion_matrixdynamic_extends(QuestionMatrixDynamicImplementor, _super);
    function QuestionMatrixDynamicImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.question["getKoPopupIsVisible"] = _this.getKoPopupIsVisible;
        return _this;
    }
    QuestionMatrixDynamicImplementor.prototype.addRow = function () {
        this.question.addRowUI();
    };
    QuestionMatrixDynamicImplementor.prototype.removeRow = function (row) {
        this.question.removeRowUI(row);
    };
    QuestionMatrixDynamicImplementor.prototype.getKoPopupIsVisible = function (row) {
        return external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](row.isDetailPanelShowing);
    };
    QuestionMatrixDynamicImplementor.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        this.question["getKoPopupIsVisible"] = undefined;
    };
    return QuestionMatrixDynamicImplementor;
}(koquestion_matrixdropdown_QuestionMatrixBaseImplementor));

var koquestion_matrixdynamic_QuestionMatrixDynamic = /** @class */ (function (_super) {
    koquestion_matrixdynamic_extends(QuestionMatrixDynamic, _super);
    function QuestionMatrixDynamic(name) {
        return _super.call(this, name) || this;
    }
    QuestionMatrixDynamic.prototype.createRenderedTable = function () {
        return new koquestion_matrixdropdown_KoQuestionMatrixDropdownRenderedTable(this);
    };
    QuestionMatrixDynamic.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_matrixdynamic_QuestionMatrixDynamicImplementor(this);
    };
    QuestionMatrixDynamic.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionMatrixDynamic;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDynamicModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("matrixdynamic", function () {
    return new koquestion_matrixdynamic_QuestionMatrixDynamic("");
});
// QuestionMatrixDropdownRenderedRow.prototype["onCreating"] = function() {
//   new ImplementorBase(this);
// };
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("matrixdynamic", function (name) {
    var q = new koquestion_matrixdynamic_QuestionMatrixDynamic(name);
    q.choices = [1, 2, 3, 4, 5];
    q.rowCount = 2;
    external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMatrixDropdownModelBase"].addDefaultColumns(q);
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_paneldynamic.ts
var koquestion_paneldynamic_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_paneldynamic_QuestionPanelDynamicImplementor = /** @class */ (function (_super) {
    koquestion_paneldynamic_extends(QuestionPanelDynamicImplementor, _super);
    function QuestionPanelDynamicImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.koRecalc = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.setCallbackFunc("koAddPanelClick", function () {
            _this.addPanel();
        });
        _this.setCallbackFunc("koRemovePanelClick", function (data) {
            _this.removePanel(data);
        });
        _this.setCallbackFunc("koPrevPanelClick", function () {
            _this.question.goToPrevPanel();
        });
        _this.setCallbackFunc("koNextPanelClick", function () {
            _this.question.goToNextPanel();
        });
        _this.setObservaleObj("koCanAddPanel", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.canAddPanel;
        }));
        _this.setObservaleObj("koCanRemovePanel", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.canRemovePanel;
        }));
        _this.setObservaleObj("koIsPrevButton", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isPrevButtonVisible;
        }));
        _this.setObservaleObj("koIsNextButton", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isNextButtonVisible;
        }));
        _this.setObservaleObj("koIsRange", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isRangeShowing;
        }));
        _this.setObservaleObj("koPanel", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.currentPanel;
        }));
        _this.setObservaleObj("koIsList", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isRenderModeList;
        }));
        _this.setObservaleObj("koIsProgressTop", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isProgressTopShowing;
        }));
        _this.setObservaleObj("koIsProgressBottom", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.isProgressBottomShowing;
        }));
        var koRangeValue = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](_this.question.currentIndex);
        koRangeValue.subscribe(function (newValue) {
            _this.question.currentIndex = newValue;
        });
        _this.setObservaleObj("koRangeValue", koRangeValue);
        _this.setObservaleObj("koRangeMax", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.visiblePanelCount - 1;
        }));
        _this.setObservaleObj("koAddButtonCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.getAddButtonCss();
        }));
        _this.setObservaleObj("koPrevButtonCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.getPrevButtonCss();
        }));
        _this.setObservaleObj("koNextButtonCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.getNextButtonCss();
        }));
        _this.setObservaleObj("koProgressText", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.progressText;
        }));
        _this.setObservaleObj("koProgress", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.progress;
        }));
        _this.setCallbackFunc("koPanelAfterRender", function (el, con) {
            _this.panelAfterRender(el, con);
        });
        _this.question.panelCountChangedCallback = function () {
            _this.onPanelCountChanged();
        };
        _this.question.renderModeChangedCallback = function () {
            _this.onRenderModeChanged();
        };
        _this.question.currentIndexChangedCallback = function () {
            _this.onCurrentIndexChanged();
        };
        return _this;
    }
    QuestionPanelDynamicImplementor.prototype.onPanelCountChanged = function () {
        this.onCurrentIndexChanged();
    };
    QuestionPanelDynamicImplementor.prototype.onRenderModeChanged = function () {
        this.onCurrentIndexChanged();
    };
    QuestionPanelDynamicImplementor.prototype.onCurrentIndexChanged = function () {
        if (this.question.isDisposed)
            return;
        this.koRecalc(this.koRecalc() + 1);
        this.question.koRangeValue(this.question.currentIndex);
    };
    QuestionPanelDynamicImplementor.prototype.addPanel = function () {
        this.question.addPanelUI();
    };
    QuestionPanelDynamicImplementor.prototype.removePanel = function (val) {
        if (!this.question.isRenderModeList) {
            val = this.question.currentPanel;
        }
        this.question.removePanelUI(val);
    };
    QuestionPanelDynamicImplementor.prototype.panelAfterRender = function (elements, con) {
        if (!this.question || !this.question.survey)
            return;
        var el = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyElement"].GetFirstNonTextElement(elements);
        this.question.survey.afterRenderPanel(con, el);
    };
    QuestionPanelDynamicImplementor.prototype.dispose = function () {
        this.question.panelCountChangedCallback = undefined;
        this.question.renderModeChangedCallback = undefined;
        this.question.currentIndexChangedCallback = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionPanelDynamicImplementor;
}(koquestion_QuestionImplementor));

var QuestionPanelDynamic = /** @class */ (function (_super) {
    koquestion_paneldynamic_extends(QuestionPanelDynamic, _super);
    function QuestionPanelDynamic(name) {
        return _super.call(this, name) || this;
    }
    QuestionPanelDynamic.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_paneldynamic_QuestionPanelDynamicImplementor(this);
    };
    QuestionPanelDynamic.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionPanelDynamic;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionPanelDynamicModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("paneldynamic", function () {
    return new QuestionPanelDynamic("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("paneldynamic", function (name) {
    return new QuestionPanelDynamic(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_text.ts
var koquestion_text_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();





var koquestion_text_QuestionTextImplementor = /** @class */ (function (_super) {
    koquestion_text_extends(QuestionTextImplementor, _super);
    function QuestionTextImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.setCallbackFunc("koOnFocus", function (_, event) {
            _this.question.onFocus(event);
            return true;
        });
        _this.setCallbackFunc("koOnBlur", function (_, event) {
            _this.question.onBlur(event);
            return true;
        });
        _this.setCallbackFunc("koOnKeyDown", function (_, event) {
            _this.question.onKeyDown(event);
            return true;
        });
        _this.setCallbackFunc("koOnKeyUp", function (_, event) {
            _this.question.onKeyUp(event);
            return true;
        });
        _this.setCallbackFunc("koOnChange", function (_, event) {
            _this.question.onChange(event);
            return true;
        });
        _this.setCallbackFunc("koOnCompositeUpdate", function (_, event) {
            _this.question.onCompositionUpdate(event);
            return true;
        });
        _this.setObservaleObj("koReadOnlyValue", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () { return _this.question.inputValue; }));
        return _this;
    }
    return QuestionTextImplementor;
}(koquestion_QuestionImplementor));

var QuestionText = /** @class */ (function (_super) {
    koquestion_text_extends(QuestionText, _super);
    function QuestionText(name) {
        return _super.call(this, name) || this;
    }
    QuestionText.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_text_QuestionTextImplementor(this);
    };
    QuestionText.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionText;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionTextModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("text", function () {
    return new QuestionText("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("text", function (name) {
    return new QuestionText(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_multipletext.ts
var koquestion_multipletext_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();








var koquestion_multipletext_koMultipleTextEditorModel = /** @class */ (function (_super) {
    koquestion_multipletext_extends(koMultipleTextEditorModel, _super);
    function koMultipleTextEditorModel(name) {
        return _super.call(this, name) || this;
    }
    koMultipleTextEditorModel.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_text_QuestionTextImplementor(this);
    };
    koMultipleTextEditorModel.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return koMultipleTextEditorModel;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["MultipleTextEditorModel"]));

var MultipleTextItem = /** @class */ (function (_super) {
    koquestion_multipletext_extends(MultipleTextItem, _super);
    function MultipleTextItem(name, title) {
        if (name === void 0) { name = null; }
        if (title === void 0) { title = null; }
        return _super.call(this, name, title) || this;
    }
    MultipleTextItem.prototype.createEditor = function (name) {
        return new koquestion_multipletext_koMultipleTextEditorModel(name);
    };
    return MultipleTextItem;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["MultipleTextItemModel"]));

var koquestion_multipletext_QuestionMultipleTextImplementor = /** @class */ (function (_super) {
    koquestion_multipletext_extends(QuestionMultipleTextImplementor, _super);
    function QuestionMultipleTextImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.koRecalc = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.setObservaleObj("koItemCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.getItemCss();
        }));
        _this.setObservaleObj("koItemTitleCss", external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["pureComputed"](function () {
            _this.koRecalc();
            return _this.question.getItemTitleCss();
        }));
        return _this;
    }
    return QuestionMultipleTextImplementor;
}(koquestion_QuestionImplementor));

var koquestion_multipletext_QuestionMultipleText = /** @class */ (function (_super) {
    koquestion_multipletext_extends(QuestionMultipleText, _super);
    function QuestionMultipleText(name) {
        return _super.call(this, name) || this;
    }
    QuestionMultipleText.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_multipletext_QuestionMultipleTextImplementor(this);
    };
    QuestionMultipleText.prototype.onRowCreated = function (row) {
        new kobase_ImplementorBase(row);
        return row;
    };
    QuestionMultipleText.prototype.createTextItem = function (name, title) {
        return new MultipleTextItem(name, title);
    };
    QuestionMultipleText.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        this.koRows = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionMultipleText;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMultipleTextModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("multipletextitem", function () {
    return new MultipleTextItem("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("multipletext", function () {
    return new koquestion_multipletext_QuestionMultipleText("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("multipletext", function (name) {
    var q = new koquestion_multipletext_QuestionMultipleText(name);
    external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionMultipleTextModel"].addDefaultItems(q);
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_radiogroup.ts
var koquestion_radiogroup_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();




var koquestion_radiogroup_QuestionRadiogroup = /** @class */ (function (_super) {
    koquestion_radiogroup_extends(QuestionRadiogroup, _super);
    function QuestionRadiogroup(name) {
        return _super.call(this, name) || this;
    }
    QuestionRadiogroup.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionCheckboxBaseImplementor(this);
    };
    QuestionRadiogroup.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionRadiogroup;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionRadiogroupModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("radiogroup", function () {
    return new koquestion_radiogroup_QuestionRadiogroup("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("radiogroup", function (name) {
    var q = new koquestion_radiogroup_QuestionRadiogroup(name);
    q.choices = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_rating.ts
var koquestion_rating_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();


var QuestionRatingImplementor = /** @class */ (function (_super) {
    koquestion_rating_extends(QuestionRatingImplementor, _super);
    function QuestionRatingImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.onCreated();
        return _this;
    }
    QuestionRatingImplementor.prototype.onCreated = function () { };
    return QuestionRatingImplementor;
}(koquestion_QuestionImplementor));

var QuestionRating = /** @class */ (function (_super) {
    koquestion_rating_extends(QuestionRating, _super);
    function QuestionRating(name) {
        return _super.call(this, name) || this;
    }
    QuestionRating.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionRatingImplementor(this);
    };
    QuestionRating.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionRating;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionRatingModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("rating", function () {
    return new QuestionRating("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("rating", function (name) {
    return new QuestionRating(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_boolean.ts
var koquestion_boolean_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();


var koquestion_boolean_QuestionBoolean = /** @class */ (function (_super) {
    koquestion_boolean_extends(QuestionBoolean, _super);
    function QuestionBoolean(name) {
        return _super.call(this, name) || this;
    }
    QuestionBoolean.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionBoolean.prototype.onSwitchClick = function (data, event) {
        return _super.prototype.onSwitchClickModel.call(this, Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["getOriginalEvent"])(event));
    };
    QuestionBoolean.prototype.onTrueLabelClick = function (data, event) {
        return this.onLabelClick(event, !this.swapOrder);
    };
    QuestionBoolean.prototype.onFalseLabelClick = function (data, event) {
        return this.onLabelClick(event, this.swapOrder);
    };
    QuestionBoolean.prototype.onKeyDown = function (data, event) {
        return this.onKeyDownCore(event);
    };
    QuestionBoolean.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionBoolean;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionBooleanModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("boolean", function () {
    return new koquestion_boolean_QuestionBoolean("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("boolean", function (name) {
    return new koquestion_boolean_QuestionBoolean(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_empty.ts
var koquestion_empty_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_empty_QuestionEmpty = /** @class */ (function (_super) {
    koquestion_empty_extends(QuestionEmpty, _super);
    function QuestionEmpty(name) {
        return _super.call(this, name) || this;
    }
    QuestionEmpty.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionEmpty.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionEmpty;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionEmptyModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("empty", function () {
    return new koquestion_empty_QuestionEmpty("");
});

// CONCATENATED MODULE: ./src/knockout/koquestion_expression.ts
var koquestion_expression_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();




var koquestion_expression_QuestionExpression = /** @class */ (function (_super) {
    koquestion_expression_extends(QuestionExpression, _super);
    function QuestionExpression(name) {
        return _super.call(this, name) || this;
    }
    QuestionExpression.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionExpression.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionExpression;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionExpressionModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("expression", function () {
    return new koquestion_expression_QuestionExpression("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("expression", function (name) {
    return new koquestion_expression_QuestionExpression(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_imagepicker.ts
var koquestion_imagepicker_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();





var koquestion_imagepicker_QuestionImagePickerImplementor = /** @class */ (function (_super) {
    koquestion_imagepicker_extends(QuestionImagePickerImplementor, _super);
    function QuestionImagePickerImplementor(question) {
        var _this = _super.call(this, question) || this;
        _this.question = question;
        _this.koRecalc = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](0);
        _this.setCallbackFunc("koGetItemClass", function (item) {
            _this.koRecalc();
            return question.getItemClass(item);
        });
        _this.question.registerFunctionOnPropertyValueChanged("value", function () {
            if (_this.question.multiSelect && _this.question.isDesignMode) {
                _this.koRecalc(_this.koRecalc() + 1);
            }
        }, "__koOnValueChangeTrigger");
        return _this;
    }
    QuestionImagePickerImplementor.prototype.getKoValue = function () {
        return this.question.renderedValue;
    };
    QuestionImagePickerImplementor.prototype.dispose = function () {
        this.question.unRegisterFunctionOnPropertyValueChanged("value", "__koOnValueChangeTrigger");
        _super.prototype.dispose.call(this);
    };
    return QuestionImagePickerImplementor;
}(QuestionCheckboxBaseImplementor));
var QuestionImagePicker = /** @class */ (function (_super) {
    koquestion_imagepicker_extends(QuestionImagePicker, _super);
    function QuestionImagePicker(name) {
        return _super.call(this, name) || this;
    }
    QuestionImagePicker.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_imagepicker_QuestionImagePickerImplementor(this);
    };
    QuestionImagePicker.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionImagePicker;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionImagePickerModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("imagepicker", function () {
    return new QuestionImagePicker("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("imagepicker", function (name) {
    var q = new QuestionImagePicker(name);
    //q.choices = QuestionFactory.DefaultChoices;
    return q;
});

// CONCATENATED MODULE: ./src/knockout/koquestion_image.ts
var koquestion_image_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();




var koquestion_image_QuestionImage = /** @class */ (function (_super) {
    koquestion_image_extends(QuestionImage, _super);
    function QuestionImage(name) {
        return _super.call(this, name) || this;
    }
    QuestionImage.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionImage.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionImage;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionImageModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("image", function () {
    return new koquestion_image_QuestionImage("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("image", function (name) {
    return new koquestion_image_QuestionImage(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_signaturepad.ts
var koquestion_signaturepad_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();



var koquestion_signaturepad_QuestionSignaturePad = /** @class */ (function (_super) {
    koquestion_signaturepad_extends(QuestionSignaturePad, _super);
    function QuestionSignaturePad(name) {
        return _super.call(this, name) || this;
    }
    QuestionSignaturePad.prototype.koOnBlur = function (data, event) {
        return this.onBlur(event);
    };
    QuestionSignaturePad.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionSignaturePad.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionSignaturePad;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionSignaturePadModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["Serializer"].overrideClassCreator("signaturepad", function () {
    return new koquestion_signaturepad_QuestionSignaturePad("");
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionFactory"].Instance.registerQuestion("signaturepad", function (name) {
    return new koquestion_signaturepad_QuestionSignaturePad(name);
});

// CONCATENATED MODULE: ./src/knockout/koquestion_custom.ts
var koquestion_custom_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();


var koquestion_custom_QuestionCustom = /** @class */ (function (_super) {
    koquestion_custom_extends(QuestionCustom, _super);
    function QuestionCustom(name, questionJSON) {
        return _super.call(this, name, questionJSON) || this;
    }
    QuestionCustom.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionCustom.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionCustom;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionCustomModel"]));

var koquestion_custom_QuestionComposite = /** @class */ (function (_super) {
    koquestion_custom_extends(QuestionComposite, _super);
    function QuestionComposite(name, questionJSON) {
        return _super.call(this, name, questionJSON) || this;
    }
    QuestionComposite.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new koquestion_QuestionImplementor(this);
    };
    QuestionComposite.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionComposite;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionCompositeModel"]));

external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ComponentCollection"].Instance.onCreateCustom = function (name, questionJSON) {
    return new koquestion_custom_QuestionCustom(name, questionJSON);
};
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ComponentCollection"].Instance.onCreateComposite = function (name, questionJSON) {
    return new koquestion_custom_QuestionComposite(name, questionJSON);
};

// CONCATENATED MODULE: ./src/knockout/koquestion_buttongroup.ts
var koquestion_buttongroup_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();


var koquestion_buttongroup_QuestionButtonGroup = /** @class */ (function (_super) {
    koquestion_buttongroup_extends(QuestionButtonGroup, _super);
    function QuestionButtonGroup(name) {
        return _super.call(this, name) || this;
    }
    QuestionButtonGroup.prototype.onBaseCreating = function () {
        _super.prototype.onBaseCreating.call(this);
        this._implementor = new QuestionCheckboxBaseImplementor(this);
    };
    QuestionButtonGroup.prototype.dispose = function () {
        this._implementor.dispose();
        this._implementor = undefined;
        _super.prototype.dispose.call(this);
    };
    return QuestionButtonGroup;
}(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["QuestionButtonGroupModel"]));

// Serializer.overrideClassCreator("buttongroup", function() {
//   return new QuestionButtonGroup("");
// });
// QuestionFactory.Instance.registerQuestion("buttongroup", name => {
//   var q = new QuestionButtonGroup(name);
//   q.choices = QuestionFactory.DefaultChoices;
//   return q;
// });

// CONCATENATED MODULE: ./src/knockout/components/text-area/text-area.ts

var text_area_template = __webpack_require__(/*! ./text-area.html */ "./src/knockout/components/text-area/text-area.html");
var TextAreaViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-text-area", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var element = componentInfo.element.querySelector && componentInfo.element.querySelector("textarea") || componentInfo.element.nextElementSibling;
            params.setElement(element);
            return {
                model: params,
                value: external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](params.getTextValue() || ""),
            };
        },
    },
    template: text_area_template,
});

// CONCATENATED MODULE: ./src/knockout/components/action-bar/action.ts


var action_template = __webpack_require__(/*! ./action.html */ "./src/knockout/components/action-bar/action.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-action", {
    viewModel: {
        createViewModel: function (params) {
            var item = params.item;
            new kobase_ImplementorBase(item);
            return params;
        },
    },
    template: action_template
});

// CONCATENATED MODULE: ./src/knockout/components/action-bar/action-bar-item.ts

var action_bar_item_template = __webpack_require__(/*! ./action-bar-item.html */ "./src/knockout/components/action-bar/action-bar-item.html");
var ActionBarItemViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-action-bar-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var el = componentInfo.element;
            el = !!el.nextElementSibling ? el.nextElementSibling : el.parentElement.firstElementChild;
            if (!!el) {
                var item_1 = params.item;
                el.onfocus = function (args) { item_1.doFocus(args); };
                el.onmousedown = function (args) { item_1.doMouseDown(args); };
            }
            return params;
        },
    },
    template: action_bar_item_template
});

// CONCATENATED MODULE: ./src/knockout/components/action-bar/action-bar-item-dropdown.ts


var action_bar_item_dropdown_template = __webpack_require__(/*! ./action-bar-item-dropdown.html */ "./src/knockout/components/action-bar/action-bar-item-dropdown.html");
var ActionBarItemDropdownViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-action-bar-item-dropdown", {
    viewModel: {
        createViewModel: function (params) {
            return {
                model: new external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ActionDropdownViewModel"](params.item)
            };
        }
    },
    template: action_bar_item_dropdown_template
});

// CONCATENATED MODULE: ./src/knockout/components/action-bar/action-bar-separator.ts

var action_bar_separator_template = __webpack_require__(/*! ./action-bar-separator.html */ "./src/knockout/components/action-bar/action-bar-separator.html");
var ActionBarSeparatorViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-action-bar-separator", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var item = params.item;
            if (!!item) {
                return {
                    css: item.innerCss,
                };
            }
            return {};
        },
    },
    template: action_bar_separator_template,
});

// CONCATENATED MODULE: ./src/knockout/components/action-bar/action-bar.ts
var action_bar_extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();


var action_bar_template = __webpack_require__(/*! ./action-bar.html */ "./src/knockout/components/action-bar/action-bar.html");




var action_bar_ActionContainerImplementor = /** @class */ (function (_super) {
    action_bar_extends(ActionContainerImplementor, _super);
    function ActionContainerImplementor(model, handleClick) {
        if (handleClick === void 0) { handleClick = true; }
        var _this = _super.call(this, model) || this;
        _this.model = model;
        _this.handleClick = handleClick;
        _this.itemsSubscription = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () {
            (model.renderedActions || model.items || model.actions).forEach(function (item) {
                if (!!item.stateItem) {
                    new kobase_ImplementorBase(item.stateItem);
                }
                else {
                    new kobase_ImplementorBase(item);
                }
            });
        });
        return _this;
    }
    ActionContainerImplementor.prototype.dispose = function () {
        _super.prototype.dispose.call(this);
        this.itemsSubscription.dispose();
        this.model.resetResponsivityManager();
    };
    return ActionContainerImplementor;
}(kobase_ImplementorBase));

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-action-bar", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var handleClick = params.handleClick !== undefined ? params.handleClick : true;
            var model = params.model;
            var container = componentInfo.element.nextElementSibling;
            params.model.initResponsivityManager(container);
            return new action_bar_ActionContainerImplementor(model, handleClick);
        },
    },
    template: action_bar_template,
});

// CONCATENATED MODULE: ./src/knockout/components/boolean-checkbox/boolean-checkbox.ts


var boolean_checkbox_template = __webpack_require__(/*! ./boolean-checkbox.html */ "./src/knockout/components/boolean-checkbox/boolean-checkbox.html");
var CheckboxViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-boolean-checkbox", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return { question: params.question };
        },
    },
    template: boolean_checkbox_template,
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["RendererFactory"].Instance.registerRenderer("boolean", "checkbox", "sv-boolean-checkbox");

// CONCATENATED MODULE: ./src/knockout/components/boolean-radio/boolean-radio-item.ts

var boolean_radio_item_template = __webpack_require__(/*! ./boolean-radio-item.html */ "./src/knockout/components/boolean-radio/boolean-radio-item.html");
var BooleanRadioItemViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-boolean-radio-item", {
    viewModel: {
        createViewModel: function (params) {
            params.handleChange = function () {
                params.question.booleanValue = params.value;
            };
            return params;
        },
    },
    template: boolean_radio_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/boolean-radio/boolean-radio.ts



var boolean_radio_template = __webpack_require__(/*! ./boolean-radio.html */ "./src/knockout/components/boolean-radio/boolean-radio.html");
var BooleanRadioViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-boolean-radio", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return { question: params.question };
        },
    },
    template: boolean_radio_template,
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["RendererFactory"].Instance.registerRenderer("boolean", "radio", "sv-boolean-radio");

// CONCATENATED MODULE: ./src/knockout/components/panel/panel.ts

var panel_template = __webpack_require__(/*! html-loader?interpolate!val-loader!./panel.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/panel/panel.html");
var PanelViewModel = /** @class */ (function () {
    function PanelViewModel(question, targetElement) {
        this.question = question;
        this.targetElement = targetElement;
    }
    return PanelViewModel;
}());

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-panel", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var viewModel = new PanelViewModel(params.question, componentInfo.element.parentElement);
            return viewModel;
        },
    },
    template: panel_template,
});

// CONCATENATED MODULE: ./src/knockout/components/popup/popup.ts



var popup_template = __webpack_require__(/*! html-loader?interpolate!val-loader!./popup.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/popup/popup.html");
var popup_PopupViewModel = /** @class */ (function () {
    function PopupViewModel(popupViewModel) {
        var _this = this;
        this.popupViewModel = popupViewModel;
        this.visibilityChangedHandler = function (s, option) {
            if (option.isVisible) {
                external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
                _this.popupViewModel.updateOnShowing();
            }
        };
        this._popupModelImplementor = new kobase_ImplementorBase(popupViewModel.model);
        this._popupImplementor = new kobase_ImplementorBase(popupViewModel);
        popupViewModel.onVisibilityChanged.add(this.visibilityChangedHandler);
    }
    PopupViewModel.prototype.dispose = function () {
        this._popupModelImplementor.dispose();
        this._popupModelImplementor = undefined;
        this._popupImplementor.dispose();
        this._popupImplementor = undefined;
        this.popupViewModel.resetComponentElement();
        this.popupViewModel.onVisibilityChanged.remove(this.visibilityChangedHandler);
        this.popupViewModel.dispose();
        this.visibilityChangedHandler = undefined;
    };
    return PopupViewModel;
}());

// replace to showDialog then delete
function showModal(componentName, data, onApply, onCancel, cssClass, title, displayMode, container) {
    if (displayMode === void 0) { displayMode = "popup"; }
    var options = Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["createDialogOptions"])(componentName, data, onApply, onCancel, undefined, undefined, cssClass, title, displayMode);
    return showDialog(options, container);
}
function showDialog(dialogOptions, rootElement) {
    var popupViewModel = Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["createPopupModalViewModel"])(dialogOptions, rootElement);
    var onVisibilityChangedCallback = function (_, options) {
        if (!options.isVisible) {
            popupViewModel.onVisibilityChanged.remove(onVisibilityChangedCallback);
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["cleanNode"](popupViewModel.container);
            popupViewModel.container.remove();
            popupViewModel.dispose();
            viewModel.dispose();
        }
    };
    popupViewModel.onVisibilityChanged.add(onVisibilityChangedCallback);
    var viewModel = new popup_PopupViewModel(popupViewModel);
    popupViewModel.container.innerHTML = popup_template;
    external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["applyBindings"](viewModel, popupViewModel.container);
    popupViewModel.model.isVisible = true;
    return popupViewModel;
}
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["settings"].showModal = showModal;
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["settings"].showDialog = showDialog;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-popup", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var container = componentInfo.element.nodeType === Node.COMMENT_NODE ? componentInfo.element.nextElementSibling : componentInfo.element;
            var viewModel = Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["createPopupViewModel"])(external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.model));
            viewModel.setComponentElement(container);
            return new popup_PopupViewModel(viewModel);
        },
    },
    template: popup_template
});

// CONCATENATED MODULE: ./src/knockout/components/progress/buttons.ts


var buttons_template = __webpack_require__(/*! html-loader?interpolate!val-loader!./buttons.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/buttons.html");
var buttons_ProgressButtonsViewModel = /** @class */ (function () {
    function ProgressButtonsViewModel(model, element, container, survey) {
        if (container === void 0) { container = "center"; }
        this.model = model;
        this.element = element;
        this.container = container;
        this.survey = survey;
        this.hasScroller = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](false);
        this.canShowHeader = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](false);
        this.canShowFooter = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](false);
        this.canShowItemTitles = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["observable"](true);
        this.respManager = new external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ProgressButtonsResponsivityManager"](model, element, this);
    }
    ProgressButtonsViewModel.prototype.onResize = function (canShowItemTitles) {
        this.canShowItemTitles(canShowItemTitles);
        this.canShowHeader(!this.canShowItemTitles());
    };
    ProgressButtonsViewModel.prototype.onUpdateScroller = function (hasScroller) {
        this.hasScroller(hasScroller);
    };
    ProgressButtonsViewModel.prototype.onUpdateSettings = function () {
        this.canShowItemTitles(this.model.showItemTitles);
        this.canShowFooter(!this.model.showItemTitles);
    };
    ProgressButtonsViewModel.prototype.getScrollButtonCss = function (isLeftScroll) {
        return this.model.getScrollButtonCss(this.hasScroller(), isLeftScroll);
    };
    ProgressButtonsViewModel.prototype.clickScrollButton = function (listContainerElement, isLeftScroll) {
        listContainerElement.scrollLeft += (isLeftScroll ? -1 : 1) * 70;
    };
    ProgressButtonsViewModel.prototype.dispose = function () {
        this.respManager.dispose();
    };
    return ProgressButtonsViewModel;
}());

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-buttons", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var viewModel = new buttons_ProgressButtonsViewModel(params.model, componentInfo.element.nextElementSibling, params.container, params.survey);
            setTimeout(function () { var _a; return (_a = params.model) === null || _a === void 0 ? void 0 : _a.processResponsiveness(0); }, 10);
            return viewModel;
        },
    },
    template: buttons_template
});

// CONCATENATED MODULE: ./src/knockout/components/progress/progress.ts


var progress_template = __webpack_require__(/*! html-loader?interpolate!val-loader!./progress.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/progress.html");
var progress_ProgressViewModel = /** @class */ (function () {
    function ProgressViewModel(model, container) {
        if (container === void 0) { container = "header"; }
        this.model = model;
        this.container = container;
    }
    ProgressViewModel.prototype.getProgressTextInBarCss = function (css) {
        return external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyProgressModel"].getProgressTextInBarCss(css);
    };
    ProgressViewModel.prototype.getProgressTextUnderBarCss = function (css) {
        return external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyProgressModel"].getProgressTextUnderBarCss(css);
    };
    ProgressViewModel.prototype.getProgressCssClasses = function () {
        return this.model.getProgressCssClasses(this.container);
    };
    return ProgressViewModel;
}());

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-progress", {
    viewModel: {
        createViewModel: function (params) {
            return new progress_ProgressViewModel(params.model, params.container);
        }
    },
    template: progress_template
});
var templateBridge = "<!-- ko component: { name: 'sv-progress-progress', params: $data } --><!-- /ko -->";
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-pages", {
    viewModel: {
        createViewModel: function (params) {
            return new progress_ProgressViewModel(params.model, params.container);
        }
    },
    template: templateBridge
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-questions", {
    viewModel: {
        createViewModel: function (params) {
            return new progress_ProgressViewModel(params.model, params.container);
        }
    },
    template: templateBridge
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-correctquestions", {
    viewModel: {
        createViewModel: function (params) {
            return new progress_ProgressViewModel(params.model, params.container);
        }
    },
    template: templateBridge
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-progress-requiredquestions", {
    viewModel: {
        createViewModel: function (params) {
            return new progress_ProgressViewModel(params.model, params.container);
        }
    },
    template: templateBridge
});

// CONCATENATED MODULE: ./src/knockout/components/progress/toc.ts

var toc_template = __webpack_require__(/*! html-loader?interpolate!val-loader!./toc.html */ "./node_modules/html-loader/index.js?interpolate!./node_modules/val-loader/index.js!./src/knockout/components/progress/toc.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-navigation-toc", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return {
                tocModel: params.model
            };
        },
    },
    template: toc_template
});

// CONCATENATED MODULE: ./src/knockout/components/components-container/components-container.ts

var components_container_template = __webpack_require__(/*! ./components-container.html */ "./src/knockout/components/components-container/components-container.html");
var ComponentsContainer = /** @class */ (function () {
    function ComponentsContainer(survey, container, needRenderWrapper) {
        if (needRenderWrapper === void 0) { needRenderWrapper = true; }
        this.survey = survey;
        this.container = container;
        this.needRenderWrapper = needRenderWrapper;
        this.css = "sv-components-column";
        this.css += " sv-components-container-" + container;
    }
    Object.defineProperty(ComponentsContainer.prototype, "components", {
        get: function () {
            return this.survey.getContainerContent(this.container);
        },
        enumerable: false,
        configurable: true
    });
    return ComponentsContainer;
}());

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-components-container", {
    viewModel: {
        createViewModel: function (params) {
            var survey = params.survey;
            return new ComponentsContainer(survey, params.container, params.needRenderWrapper);
        },
    },
    template: components_container_template
});

// CONCATENATED MODULE: ./src/knockout/components/template-renderer/template-renderer.ts


var template_renderer_template = __webpack_require__(/*! ./template-renderer.html */ "./src/knockout/components/template-renderer/template-renderer.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"].TemplateRendererComponentName, {
    viewModel: {
        createViewModel: function (params) {
            return params;
        },
    },
    template: template_renderer_template,
});

// CONCATENATED MODULE: ./src/knockout/components/title/title-element.ts
/* eslint-disable no-restricted-globals */

var TitleElementViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("survey-element-title", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var element = params.element;
            var rootEl = componentInfo.element;
            var titleEl = document.createElement(element.titleTagName);
            var ariaLabelAttr = !element.titleAriaLabel ? "" : "'aria-label': element.titleAriaLabel,";
            var bindings = "css: element.cssTitle, attr: { " + ariaLabelAttr + " id: element.ariaTitleId, tabindex: element.titleTabIndex, 'aria-expanded': element.titleAriaExpanded, role: element.titleAriaRole }";
            if (element.hasTitleEvents) {
                bindings += ", key2click";
            }
            titleEl.setAttribute("data-bind", bindings);
            var innerHTML = "<!-- ko component: { name: 'sv-title-actions', params: {element: element } } --><!-- /ko -->";
            var iconExpandSvg, iconCollapseSvg;
            if (element.getCssTitleExpandableSvg()) {
                var getSvgComponentString = function (iconName) { return "<!-- ko component: { name: 'sv-svg-icon', params: { css: element.getCssTitleExpandableSvg(), iconName: '" + iconName + "', size: 'auto' } } --><!-- /ko -->"; };
                iconExpandSvg = "<!-- ko ifnot: element.isExpanded -->" + getSvgComponentString("icon-expand-16x16") + "<!-- /ko -->";
                iconCollapseSvg = "<!-- ko if: element.isExpanded -->" + getSvgComponentString("icon-collapse-16x16") + "<!-- /ko -->";
                innerHTML = iconExpandSvg + iconCollapseSvg + innerHTML;
            }
            titleEl.innerHTML = innerHTML;
            var dummyNode = rootEl.nextSibling;
            rootEl.parentNode.insertBefore(document.createComment(" ko if: element.hasTitle "), dummyNode);
            rootEl.parentNode.insertBefore(titleEl, dummyNode);
            rootEl.parentNode.insertBefore(document.createComment(" /ko "), dummyNode);
            rootEl.parentNode.removeChild(dummyNode);
            return { element: element };
        },
    },
    template: "<span></span>",
});

// CONCATENATED MODULE: ./src/knockout/components/title/title-content.ts

var title_content_template = __webpack_require__(/*! ./title-content.html */ "./src/knockout/components/title/title-content.html");
var TitleContentViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("survey-element-title-content", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var element = params.element;
            return { element: element };
        },
    },
    template: title_content_template,
});

// CONCATENATED MODULE: ./src/knockout/components/title/title-actions.ts


var title_actions_template = __webpack_require__(/*! ./title-actions.html */ "./src/knockout/components/title/title-actions.html");
var TitleActionViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-title-actions", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var element = params.element;
            return {
                element: element,
                toolbar: element.getTitleToolbar(),
            };
        },
    },
    template: title_actions_template,
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["RendererFactory"].Instance.registerRenderer("element", "title-actions", "sv-title-actions");

// CONCATENATED MODULE: ./src/knockout/components/string-editor/string-editor.ts
/* eslint-disable no-restricted-globals */


var string_editor_template = __webpack_require__(/*! ./string-editor.html */ "./src/knockout/components/string-editor/string-editor.html");
var StringEditorViewModel = /** @class */ (function () {
    function StringEditorViewModel(locString) {
        this.locString = locString;
    }
    Object.defineProperty(StringEditorViewModel.prototype, "koHasHtml", {
        get: function () {
            return this.locString.koHasHtml();
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StringEditorViewModel.prototype, "editValue", {
        get: function () {
            return this.locString.koRenderedHtml();
        },
        set: function (value) {
            this.locString.searchElement = undefined;
            this.locString.text = value;
        },
        enumerable: false,
        configurable: true
    });
    StringEditorViewModel.prototype.onInput = function (sender, event) {
        sender.editValue = event.target.innerText;
    };
    StringEditorViewModel.prototype.onClick = function (sender, event) {
        event.stopPropagation();
    };
    StringEditorViewModel.prototype.dispose = function () {
        this.locString.onSearchChanged = undefined;
    };
    return StringEditorViewModel;
}());

function getSearchElement(element) {
    while (!!element && element.nodeName !== "SPAN") {
        var elements = element.parentElement.getElementsByClassName("sv-string-editor");
        element = elements.length > 0 ? elements[0] : undefined;
    }
    if (!!element && element.childNodes.length > 0)
        return element;
    return null;
}
function resetLocalizationSpan(element, locStr) {
    while (element.childNodes.length > 1) {
        element.removeChild(element.childNodes[1]);
    }
    element.childNodes[0].textContent = locStr.renderedHtml;
}
function applyLocStrOnSearchChanged(element, locStr) {
    locStr.onSearchChanged = function () {
        if (locStr.searchElement == undefined) {
            locStr.searchElement = getSearchElement(element);
        }
        if (locStr.searchElement == null)
            return;
        var el = locStr.searchElement;
        if (!locStr.highlightDiv) {
            locStr.highlightDiv = document.createElement("span");
            locStr.highlightDiv.style.backgroundColor = "lightgray";
        }
        if (locStr.searchIndex != undefined) {
            resetLocalizationSpan(el, locStr);
            var rng = document.createRange();
            rng.setStart(el.childNodes[0], locStr.searchIndex);
            rng.setEnd(el.childNodes[0], locStr.searchIndex + locStr.searchText.length);
            rng.surroundContents(locStr.highlightDiv);
        }
        else {
            resetLocalizationSpan(el, locStr);
            locStr.searchElement = undefined;
        }
    };
}
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["LocalizableString"].editableRenderer, {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var locStr = params.locString;
            applyLocStrOnSearchChanged(componentInfo.element, locStr);
            return new StringEditorViewModel(locStr);
        },
    },
    template: string_editor_template
});

// CONCATENATED MODULE: ./src/knockout/components/string-viewer/string-viewer.ts

var string_viewer_template = __webpack_require__(/*! ./string-viewer.html */ "./src/knockout/components/string-viewer/string-viewer.html");
var StringViewerViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-string-viewer", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return {
                locString: params.locString
            };
        },
    },
    template: string_viewer_template
});

// CONCATENATED MODULE: ./src/knockout/components/logo-image/logo-image.ts

var logo_image_template = __webpack_require__(/*! ./logo-image.html */ "./src/knockout/components/logo-image/logo-image.html");
var LogoImageViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-logo-image", {
    viewModel: {
        createViewModel: function (params) {
            return { survey: params };
        },
    },
    template: logo_image_template
});

// CONCATENATED MODULE: ./src/knockout/components/skeleton/skeleton.ts

var skeleton_template = __webpack_require__(/*! ./skeleton.html */ "./src/knockout/components/skeleton/skeleton.html");
var Skeleton;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-skeleton", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return { element: params.element };
        },
    },
    template: skeleton_template,
});

// CONCATENATED MODULE: ./src/knockout/components/character-counter/character-counter.ts


var character_counter_template = __webpack_require__(/*! ./character-counter.html */ "./src/knockout/components/character-counter/character-counter.html");
var CharacterCounterComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-character-counter", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var counter = params.counter;
            var remainingCharacterCounter = params.remainingCharacterCounter;
            new kobase_ImplementorBase(counter);
            return { counter: counter, remainingCharacterCounter: remainingCharacterCounter };
        },
    },
    template: character_counter_template,
});

// CONCATENATED MODULE: ./src/knockout/components/rating-dropdown/rating-dropdown-item.ts


var rating_dropdown_item_template = __webpack_require__(/*! ./rating-dropdown-item.html */ "./src/knockout/components/rating-dropdown/rating-dropdown-item.html");
var RatingItemViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-rating-dropdown-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return {
                item: params.item,
                description: params.item.description
            };
        },
    },
    template: rating_dropdown_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/rating-dropdown/rating-dropdown.ts


var rating_dropdown_template = __webpack_require__(/*! ./rating-dropdown.html */ "./src/knockout/components/rating-dropdown/rating-dropdown.html");

var RatingDropdownViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-rating-dropdown", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return { question: params.question };
        },
    },
    template: rating_dropdown_template,
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["RendererFactory"].Instance.registerRenderer("rating", "dropdown", "sv-rating-dropdown");

// CONCATENATED MODULE: ./src/knockout/components/rating/rating-item.ts


var rating_item_template = __webpack_require__(/*! ./rating-item.html */ "./src/knockout/components/rating/rating-item.html");
var RatingItemViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-rating-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return { question: params.question, item: params.item, index: params.index };
        },
    },
    template: rating_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/rating/rating-item-star.ts


var rating_item_star_template = __webpack_require__(/*! ./rating-item-star.html */ "./src/knockout/components/rating/rating-item-star.html");
var RatingItemStarViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-rating-item-star", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return { question: params.question, item: params.item, index: params.index };
        },
    },
    template: rating_item_star_template,
});

// CONCATENATED MODULE: ./src/knockout/components/rating/rating-item-smiley.ts


var rating_item_smiley_template = __webpack_require__(/*! ./rating-item-smiley.html */ "./src/knockout/components/rating/rating-item-smiley.html");
var RatingItemSmileyViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-rating-item-smiley", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return { question: params.question, item: params.item, index: params.index };
        },
    },
    template: rating_item_smiley_template,
});

// CONCATENATED MODULE: ./src/knockout/components/dropdown/dropdown.ts


var dropdown_template = __webpack_require__(/*! ./dropdown.html */ "./src/knockout/components/dropdown/dropdown.html");
var DropdownViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-dropdown", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var q = params.question;
            var click = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.onClick(e);
            };
            var chevronPointerDown = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.chevronPointerDown(e);
            };
            var clear = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.onClear(e);
            };
            var keyhandler = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.keyHandler(e);
                return true;
            };
            var blur = function (_, e) {
                q.onBlur(e);
            };
            var focus = function (_, e) {
                q.onFocus(e);
            };
            new kobase_ImplementorBase(q.dropdownListModel);
            return { question: q, model: q.dropdownListModel, click: click, clear: clear, keyhandler: keyhandler, blur: blur, focus: focus, chevronPointerDown: chevronPointerDown };
        },
    },
    template: dropdown_template,
});

// CONCATENATED MODULE: ./src/knockout/components/dropdown-select/dropdown-select.ts



var dropdown_select_template = __webpack_require__(/*! ./dropdown-select.html */ "./src/knockout/components/dropdown-select/dropdown-select.html");
var DropdownSelectViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-dropdown-select", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            params.question.choices.forEach(function (choice) {
                new kobase_ImplementorBase(choice);
            });
            var keyup = function (_, e) {
                params.question.onKeyUp(e);
            };
            var click = function (_, e) {
                params.question.onClick(e);
            };
            return { question: params.question, click: click, keyup: keyup };
        },
    },
    template: dropdown_select_template,
});
external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["RendererFactory"].Instance.registerRenderer("dropdown", "select", "sv-dropdown-select");

// CONCATENATED MODULE: ./src/knockout/components/tagbox/tagbox-item.ts


var tagbox_item_template = __webpack_require__(/*! ./tagbox-item.html */ "./src/knockout/components/tagbox/tagbox-item.html");
var TagboxViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-tagbox-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var item = params.item;
            new kobase_ImplementorBase(item);
            return {
                item: item,
                question: params.question,
                removeItem: function (data, event) {
                    data.question.dropdownListModel.deselectItem(data.item.value);
                    event.stopPropagation();
                }
            };
        },
    },
    template: tagbox_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/tagbox/tagbox.ts



var tagbox_template = __webpack_require__(/*! ./tagbox.html */ "./src/knockout/components/tagbox/tagbox.html");
var TagboxViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-tagbox", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var q = params.question;
            var click = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.onClick(e);
            };
            var chevronPointerDown = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.chevronPointerDown(e);
            };
            var clear = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.onClear(e);
            };
            var keyhandler = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.keyHandler(e);
                return true;
            };
            var blur = function (_, e) {
                q.onBlur(e);
            };
            var focus = function (_, e) {
                q.onFocus(e);
            };
            var inputKeyHandler = function (_, e) {
                var _a;
                (_a = q.dropdownListModel) === null || _a === void 0 ? void 0 : _a.inputKeyHandler(e);
                return true;
            };
            if (!q.dropdownListModel) {
                q.dropdownListModel = new external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["DropdownMultiSelectListModel"](q);
            }
            new kobase_ImplementorBase(q.dropdownListModel);
            return { question: q, model: q.dropdownListModel, click: click, clear: clear, keyhandler: keyhandler, blur: blur, focus: focus, inputKeyHandler: inputKeyHandler, chevronPointerDown: chevronPointerDown };
        },
    },
    template: tagbox_template,
});

// CONCATENATED MODULE: ./src/knockout/components/header/cell.ts

var cell_template = __webpack_require__(/*! ./cell.html */ "./src/knockout/components/header/cell.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-header-cell", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            // new ImplementorBase(params.model);
            return params.model;
        },
    },
    template: cell_template,
});

// CONCATENATED MODULE: ./src/knockout/components/header/mobile.ts

var mobile_template = __webpack_require__(/*! ./mobile.html */ "./src/knockout/components/header/mobile.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-header-mobile", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            // new ImplementorBase(params.model);
            return params.model;
        },
    },
    template: mobile_template,
});

// CONCATENATED MODULE: ./src/knockout/components/header/index.ts




var header_template = __webpack_require__(/*! ./index.html */ "./src/knockout/components/header/index.html");
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-header", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            params.model.survey = params.survey;
            new kobase_ImplementorBase(params.model);
            return params;
        },
    },
    template: header_template,
});

// CONCATENATED MODULE: ./src/knockout/components/file/choose-file.ts

var choose_file_template = __webpack_require__(/*! ./choose-file.html */ "./src/knockout/components/file/choose-file.html");
var SurveyNavigationButton;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-file-choose-btn", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        },
    },
    template: choose_file_template,
});

// CONCATENATED MODULE: ./src/knockout/components/file/file-preview.ts

var file_preview_template = __webpack_require__(/*! ./file-preview.html */ "./src/knockout/components/file/file-preview.html");
var SurveyFilePreview;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-file-preview", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        },
    },
    template: file_preview_template,
});

// CONCATENATED MODULE: ./src/knockout/components/file/file-page.ts


var file_page_template = __webpack_require__(/*! ./file-page.html */ "./src/knockout/components/file/file-page.html");
var SurveyFilePage;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-file-page", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var _implementor = new kobase_ImplementorBase(params.model);
            return {
                dispose: function () {
                    _implementor.dispose();
                },
                model: params.model
            };
        }
    },
    template: file_page_template,
});

// CONCATENATED MODULE: ./src/knockout/components/file/file-item.ts

var file_item_template = __webpack_require__(/*! ./file-item.html */ "./src/knockout/components/file/file-item.html");
var SurveyFileItem;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-file-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        }
    },
    template: file_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/list/list-item.ts


var list_item_template = __webpack_require__(/*! ./list-item.html */ "./src/knockout/components/list/list-item.html");
var ListItemViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-list-item", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return {
                item: params.item,
                model: params.model,
                disableTabStop: params.item.disableTabStop,
                itemClick: function (data, event) {
                    data.model.onItemClick(data.item);
                    event.stopPropagation();
                },
                hover: function (event, data) {
                    if (event.type === "mouseover") {
                        data.model.onItemHover(data.item);
                    }
                },
                leave: function (event, data) {
                    data.model.onItemLeave(data.item);
                },
                itemComponent: params.item.component || params.model.itemComponent
            };
        },
    },
    template: list_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/list/list-item-content.ts


var list_item_content_template = __webpack_require__(/*! ./list-item-content.html */ "./src/knockout/components/list/list-item-content.html");
var ListItemContentViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-list-item-content", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.item);
            return {
                item: params.item,
                model: params.model
            };
        },
    },
    template: list_item_content_template,
});

// CONCATENATED MODULE: ./src/knockout/components/list/list-item-group.ts


var list_item_group_template = __webpack_require__(/*! ./list-item-group.html */ "./src/knockout/components/list/list-item-group.html");
var ListItemGroupViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-list-item-group", {
    viewModel: {
        createViewModel: function (params) {
            new kobase_ImplementorBase(params.item);
            return {
                item: params.item,
                model: params.model,
                disableTabStop: params.item.disableTabStop,
                itemClick: function (data, event) {
                    data.model.onItemClick(data.item);
                    event.stopPropagation();
                },
            };
        },
    },
    template: list_item_group_template,
});

// CONCATENATED MODULE: ./src/knockout/components/list/list.ts


var list_template = __webpack_require__(/*! ./list.html */ "./src/knockout/components/list/list.html");



var ListViewComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-list", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var model = params.model;
            var _implementor = new action_bar_ActionContainerImplementor(model);
            model.initListContainerHtmlElement(componentInfo.element);
            return {
                model: model,
                dispose: function () {
                    _implementor.dispose();
                    model.initListContainerHtmlElement(undefined);
                },
                afterItemRender: function (_, action) {
                    !!external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"] && external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["tasks"].runEarly();
                    model.onLastItemRended(action);
                }
            };
        },
    },
    template: list_template,
});

// CONCATENATED MODULE: ./src/knockout/components/svg-icon/svg-icon.ts


var svg_icon_template = __webpack_require__(/*! ./svg-icon.html */ "./src/knockout/components/svg-icon/svg-icon.html");
var SvgIconViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-svg-icon", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["computed"](function () {
                var iconName = external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.iconName);
                var element = componentInfo.element.querySelector && componentInfo.element.querySelector("svg") || componentInfo.element.nextElementSibling;
                if (iconName) {
                    Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["createSvg"])(external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.size), external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.width), external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.height), iconName, element, external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["unwrap"](params.title));
                }
            });
            return {
                hasIcon: params.iconName,
                css: params.css,
                title: params.title
            };
        },
    },
    template: svg_icon_template,
});

// CONCATENATED MODULE: ./src/knockout/components/matrix-actions/remove-button/remove-button.ts

var remove_button_template = __webpack_require__(/*! ./remove-button.html */ "./src/knockout/components/matrix-actions/remove-button/remove-button.html");
var SurveyQuestionMatrixDynamicRemoveButton;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-matrix-remove-button", {
    viewModel: {
        createViewModel: function (params) {
            return params.item.data;
        },
    },
    template: remove_button_template
});

// CONCATENATED MODULE: ./src/knockout/components/matrix-actions/detail-button/detail-button.ts

var detail_button_template = __webpack_require__(/*! ./detail-button.html */ "./src/knockout/components/matrix-actions/detail-button/detail-button.html");
var SurveyQuestionMatrixDetailButton;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-matrix-detail-button", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params.item.data;
        },
    },
    template: detail_button_template,
});

// CONCATENATED MODULE: ./src/knockout/components/matrix-actions/drag-drop-icon/drag-drop-icon.ts

var drag_drop_icon_template = __webpack_require__(/*! ./drag-drop-icon.html */ "./src/knockout/components/matrix-actions/drag-drop-icon/drag-drop-icon.html");
var SurveyQuestionMatrixDynamicDragDropIcon;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-matrix-drag-drop-icon", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params.item.data;
        },
    },
    template: drag_drop_icon_template,
});

// CONCATENATED MODULE: ./src/knockout/components/button-group/button-group-item.ts


var button_group_item_template = __webpack_require__(/*! ./button-group-item.html */ "./src/knockout/components/button-group/button-group-item.html");
var ButtonGroupItemViewModel = /** @class */ (function () {
    function ButtonGroupItemViewModel(model) {
        this.model = model;
    }
    return ButtonGroupItemViewModel;
}());

external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-button-group-item", {
    viewModel: {
        createViewModel: function (params) {
            var model = new external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["ButtonGroupItemModel"](params.question, params.item, params.index());
            var viewModel = new ButtonGroupItemViewModel(model);
            return viewModel;
        },
    },
    template: button_group_item_template,
});

// CONCATENATED MODULE: ./src/knockout/components/survey-actions/survey-nav-button.ts

var survey_nav_button_template = __webpack_require__(/*! ./survey-nav-button.html */ "./src/knockout/components/survey-actions/survey-nav-button.html");
var survey_nav_button_SurveyNavigationButton;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-nav-btn", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        },
    },
    template: survey_nav_button_template,
});

// CONCATENATED MODULE: ./src/knockout/components/paneldynamic-actions/paneldynamic-actions.ts

var addBtnTemplate = __webpack_require__(/*! ./paneldynamic-add-btn.html */ "./src/knockout/components/paneldynamic-actions/paneldynamic-add-btn.html");
var nextBtnTemplate = __webpack_require__(/*! ./paneldynamic-next-btn.html */ "./src/knockout/components/paneldynamic-actions/paneldynamic-next-btn.html");
var prevBtnTemplate = __webpack_require__(/*! ./paneldynamic-prev-btn.html */ "./src/knockout/components/paneldynamic-actions/paneldynamic-prev-btn.html");
var progressTextTemplate = __webpack_require__(/*! ./paneldynamic-progress-text.html */ "./src/knockout/components/paneldynamic-actions/paneldynamic-progress-text.html");
var removeBtnTemplate = __webpack_require__(/*! ./paneldynamic-remove-btn.html */ "./src/knockout/components/paneldynamic-actions/paneldynamic-remove-btn.html");
var SurveyQuestionPaneldynamicActioons;
function getPaneldynamicActionViewModel() {
    return {
        createViewModel: function (params, componentInfo) {
            return (!!params.item && params.item.data) || params;
        },
    };
}
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-paneldynamic-add-btn", {
    viewModel: getPaneldynamicActionViewModel(),
    template: addBtnTemplate,
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-paneldynamic-next-btn", {
    viewModel: getPaneldynamicActionViewModel(),
    template: nextBtnTemplate,
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-paneldynamic-prev-btn", {
    viewModel: getPaneldynamicActionViewModel(),
    template: prevBtnTemplate,
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-paneldynamic-progress-text", {
    viewModel: getPaneldynamicActionViewModel(),
    template: progressTextTemplate,
});
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-paneldynamic-remove-btn", {
    viewModel: getPaneldynamicActionViewModel(),
    template: removeBtnTemplate,
});

// CONCATENATED MODULE: ./src/knockout/components/brand-info/brand-info.ts

var brand_info_template = __webpack_require__(/*! ./brand-info.html */ "./src/knockout/components/brand-info/brand-info.html");
var BrandInfoComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-brand-info", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return {};
        }
    },
    template: brand_info_template,
});

// CONCATENATED MODULE: ./src/knockout/components/question-error/question-error.ts

var question_error_template = __webpack_require__(/*! ./question-error.html */ "./src/knockout/components/question-error/question-error.html");
var QuestionErrorComponent;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-question-error", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            return params;
        }
    },
    template: question_error_template,
});

// CONCATENATED MODULE: ./src/knockout/components/notifier/notifier.ts


var notifier_template = __webpack_require__(/*! ./notifier.html */ "./src/knockout/components/notifier/notifier.html");
var NotifierViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-notifier", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            new kobase_ImplementorBase(params.notifier);
            return params;
        },
    },
    template: notifier_template,
});

// CONCATENATED MODULE: ./src/knockout/components/loading-indicator/loading-indicator.ts

var loading_indicator_template = __webpack_require__(/*! ./loading-indicator.html */ "./src/knockout/components/loading-indicator/loading-indicator.html");
var LoadingIndicatorViewModel;
external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-loading-indicator", {
    viewModel: {
        createViewModel: function (params, componentInfo) { }
    },
    template: loading_indicator_template
});

// CONCATENATED MODULE: ./src/knockout/svg-bundle.ts


external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_["components"].register("sv-svg-bundle", {
    viewModel: {
        createViewModel: function (params, componentInfo) {
            var element = componentInfo.element.querySelector && componentInfo.element.querySelector("svg") || componentInfo.element.nextElementSibling;
            element.innerHTML = external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SvgRegistry"].iconsRenderedHtml();
            return params;
        }
    },
    template: "<svg id='sv-icon-holder-global-container' style=\"display:none\"></svg>"
});

// CONCATENATED MODULE: ./src/entries/knockout-ui-model.ts

















































































registerTemplateEngine(external_root_ko_commonjs2_knockout_commonjs_knockout_amd_knockout_, external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["SurveyModel"].platform);

// CONCATENATED MODULE: ./src/entries/core-export.ts




// CONCATENATED MODULE: ./src/entries/knockout-ui.ts



Object(external_root_Survey_commonjs2_survey_core_commonjs_survey_core_amd_survey_core_["checkLibraryVersion"])("" + "1.12.47", "survey-knockout-ui");


/***/ }),

/***/ "./src/knockout/components/action-bar/action-bar-item-dropdown.html":
/*!**************************************************************************!*\
  !*** ./src/knockout/components/action-bar/action-bar-item-dropdown.html ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: $data.model.item -->\n<button type=\"button\"\n  data-bind=\"click: function(s, args) { $data.action($data, getIsTrusted(args)); }, key2click: { processEsc: false }, css: getActionBarItemCss(), attr: { disabled: $data.enabled !== undefined && !ko.unwrap($data.enabled), title: $data.tooltip || $data.title, 'role': $data.ariaRole }\">\n  <!-- ko if: $data.iconName -->\n  <!-- ko component: { name: 'sv-svg-icon', params: { iconName: iconName, size: iconSize, title: $data.tooltip || $data.title, css: $data.cssClasses.itemIcon } } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: $data.hasTitle -->\n  <span data-bind=\"text: title, css: getActionBarItemTitleCss()\"></span>\n  <!-- /ko -->\n</button>\n<sv-popup params=\"{ model: popupModel }\"></sv-popup>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/action-bar/action-bar-item.html":
/*!*****************************************************************!*\
  !*** ./src/knockout/components/action-bar/action-bar-item.html ***!
  \*****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: $data.item -->\n<button\n  type=\"button\"\n  data-bind=\"click: function(s, args) { $data.doAction(args); }, key2click: { processEsc: false }, disable: $data.disabled, css: getActionBarItemCss(), attr: { title: $data.tooltip || $data.title, 'aria-checked': $data.ariaChecked, 'role': $data.ariaRole, 'aria-expanded': typeof $data.ariaExpanded === 'undefined' ? null : ($data.ariaExpanded ? 'true': 'false') }\"\n>\n  <!-- ko if: $data.iconName -->\n  <!-- ko component: { name: 'sv-svg-icon', params: { css: $data.cssClasses.itemIcon, iconName: iconName, size: iconSize, title: $data.tooltip || $data.title } } --><!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: $data.hasTitle -->\n  <span\n    data-bind=\"text: title, css: getActionBarItemTitleCss()\"\n  ></span>\n  <!-- /ko -->\n</button>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/action-bar/action-bar-separator.html":
/*!**********************************************************************!*\
  !*** ./src/knockout/components/action-bar/action-bar-separator.html ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sv-action-bar-separator\" data-bind=\"css: $data.css\"></div>";

/***/ }),

/***/ "./src/knockout/components/action-bar/action-bar.html":
/*!************************************************************!*\
  !*** ./src/knockout/components/action-bar/action-bar.html ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: model.hasActions -->\n<div\n  data-bind=\"css: model.getRootCss(), click: handleClick ? function() { return true; } : undefined, clickBubble: handleClick ? false : undefined\"\n>\n  <!-- ko foreach: model.renderedActions -->\n  <!-- ko component: { name: 'sv-action', params: { item: $data } } -->\n  <!-- /ko -->\n  <!--/ko-->\n</div>\n<!--/ko-->\n";

/***/ }),

/***/ "./src/knockout/components/action-bar/action.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/action-bar/action.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: $data.item -->\r\n<div data-bind=\"class: $data.getActionRootCss(), attr: { id: $data.id }\">\r\n    <!-- ko ifnot: $data.isEmpty -->\r\n    <div class=\"sv-action__content\">\r\n        <!-- ko if: $data.needSeparator -->\r\n        <sv-action-bar-separator></sv-action-bar-separator>\r\n        <!-- /ko -->\r\n        <!-- ko ifnot: $data.template-->\r\n        <!-- ko component: { name: $data.component || 'sv-action-bar-item', params: { item: $data } } -->\r\n        <!-- /ko -->\r\n        <!-- /ko -->\r\n        <!-- ko if: $data.template  -->\r\n        <!-- ko template: { name: $data.template, data: $data.data || $data } -->\r\n        <!-- /ko -->\r\n        <!-- /ko -->\r\n    </div>\r\n    <!-- /ko -->\r\n</div>\r\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/boolean-checkbox/boolean-checkbox.html":
/*!************************************************************************!*\
  !*** ./src/knockout/components/boolean-checkbox/boolean-checkbox.html ***!
  \************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.cssClasses.rootCheckbox\">\n  <div data-bind=\"css: question.getCheckboxItemCss()\">\n    <label data-bind=\"css: question.cssClasses.checkboxLabel\">\n      <input\n        type=\"checkbox\"\n        data-bind=\"value: question.booleanValue, css: question.cssClasses.controlCheckbox, attr: {name: question.name, id: question.inputId, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage, readonly: question.isReadOnlyAttr}, checked: question.booleanValue, surveyProp: {indeterminate: question.isIndeterminate}, enable: !question.isDisabledAttr\"\n      />\n      <span data-bind=\"css: question.cssClasses.checkboxMaterialDecorator\">\n        <!-- ko if: question.svgIcon -->\n        <svg data-bind=\"css:question.cssClasses.checkboxItemDecorator\">\n          <use data-bind=\"attr:{'xlink:href':question.svgIcon}\" xlink:href=''></use>\n        </svg>\n        <!-- /ko -->\n        <span class=\"check\"></span>\n      </span>\n      <span\n        data-bind=\"if: question.isLabelRendered, css: question.cssClasses.checkboxControlLabel, attr: {id: question.labelRenderedAriaID}\"\n      >\n        <!-- ko component: { name: 'sv-title-actions', params: {element: question } } --><!-- /ko -->\n      </span>\n    </label>\n    <!-- ko if: question.canRenderLabelDescription -->\n    <div data-bind=\"css: question.cssDescription, attr: {'id': question.ariaDescriptionId}\">\n      <!-- ko template: { name: 'survey-string', data: question.locDescription } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/boolean-radio/boolean-radio-item.html":
/*!***********************************************************************!*\
  !*** ./src/knockout/components/boolean-radio/boolean-radio-item.html ***!
  \***********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "  <div role=\"presentation\" data-bind=\"class: question.getRadioItemClass(question.cssClasses, $data.value)\">\n    <label data-bind=\"css: question.cssClasses.radioLabel\">\n      <input\n        type=\"radio\"\n        data-bind=\"event: { change: handleChange }, attr: { name: question.name, 'aria-errormessage': question.ariaErrormessage, value: ''+$data.value, checked: $data.value === question.booleanValue, readonly: question.isReadOnlyAttr }, enable: !question.isDisabledAttr, css: question.cssClasses.itemRadioControl\"\n      />\n      <!-- ko if: question.cssClasses.materialRadioDecorator -->\n      <span data-bind=\"css: question.cssClasses.materialRadioDecorator\">\n        <!-- ko if: question.itemSvgIcon -->\n        <svg data-bind=\"css:question.cssClasses.itemRadioDecorator\">\n          <use data-bind=\"attr:{'xlink:href':question.itemSvgIcon}\" xlink:href=''></use>\n        </svg>\n        <!-- /ko -->\n      </span>\n      <!-- /ko -->\n      <span data-bind=\"css: question.cssClasses.radioControlLabel\">\n        <!-- ko template: { name: 'survey-string', data: $data.locText } -->\n        <!-- /ko -->\n      </span>\n    </label>\n  </div>\n\n";

/***/ }),

/***/ "./src/knockout/components/boolean-radio/boolean-radio.html":
/*!******************************************************************!*\
  !*** ./src/knockout/components/boolean-radio/boolean-radio.html ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.cssClasses.rootRadio\">\n  <fieldset role=\"presentation\" data-bind=\"css: question.cssClasses.radioFieldset\">\n    <!-- ko ifnot: question.swapOrder -->\n    <!-- ko component: { name: 'sv-boolean-radio-item', params: { value: false, locText: question.locLabelFalse, question: question } } --><!-- /ko -->\n    <!-- ko component: { name: 'sv-boolean-radio-item', params: { value: true, locText: question.locLabelTrue, question: question } } --><!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: question.swapOrder -->\n    <!-- ko component: { name: 'sv-boolean-radio-item', params: { value: true, locText: question.locLabelTrue, question: question } } --><!-- /ko -->\n    <!-- ko component: { name: 'sv-boolean-radio-item', params: { value: false, locText: question.locLabelFalse, question: question } } --><!-- /ko -->\n    <!-- /ko -->\n  </fieldset>\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/brand-info/brand-info.html":
/*!************************************************************!*\
  !*** ./src/knockout/components/brand-info/brand-info.html ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sv-brand-info\">\n  <a class=\"sv-brand-info__logo\" href=\"https://surveyjs.io/?utm_source=built-in_links&utm_medium=online_survey_tool&utm_campaign=landing_page\"><img src=\"https://surveyjs.io/Content/Images/poweredby.svg\"/></a>\n  <div class=\"sv-brand-info__text\">Try and see how easy it is to <a href=\"https://surveyjs.io/create-survey?utm_source=built-in_links&utm_medium=online_survey_tool&utm_campaign=create_survey\">create a survey</a></div>\n  <div class=\"sv-brand-info__terms\"><a href=\"https://surveyjs.io/TermsOfUse\">Terms of Use & Privacy Statement</a></div>\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/button-group/button-group-item.html":
/*!*********************************************************************!*\
  !*** ./src/knockout/components/button-group/button-group-item.html ***!
  \*********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<label role=\"radio\" data-bind=\"css: model.css.label, attr: { title: model.caption.koRenderedHtml }\">\r\n  <input type=\"radio\"\r\n    data-bind=\"attr: { name: model.name, id: model.id, 'aria-required': model.isRequired, 'aria-label': model.caption.koRenderedHtml, role: 'radio', 'aria-invalid': model.hasErrors, 'aria-errormessage': model.describeBy}, checkedValue: model.value, checked: model.question.renderedValue, disable: model.readOnly, css: model.css.control\" />\r\n  <div data-bind=\"css: model.css.decorator\">\r\n    <!-- ko if: !!model.iconName-->\r\n    <sv-svg-icon data-bind=\"css: model.css.icon\" params=\"iconName: model.iconName, size: model.iconSize\"></sv-svg-icon>\r\n    <!-- /ko -->\r\n    <!-- ko if: model.showCaption -->\r\n    <span data-bind=\"css: model.css.caption, attr: { title: model.caption.koRenderedHtml }\">\r\n      <!-- ko template: { name: 'survey-string', data: model.caption } -->\r\n      <!-- /ko -->\r\n    </span>\r\n    <!-- /ko -->\r\n  </div>\r\n</label>";

/***/ }),

/***/ "./src/knockout/components/character-counter/character-counter.html":
/*!**************************************************************************!*\
  !*** ./src/knockout/components/character-counter/character-counter.html ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"text: counter.remainingCharacterCounter, css: remainingCharacterCounter\"></div>";

/***/ }),

/***/ "./src/knockout/components/components-container/components-container.html":
/*!********************************************************************************!*\
  !*** ./src/knockout/components/components-container/components-container.html ***!
  \********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: components.length > 0 -->\n<!-- ko if: $data.needRenderWrapper -->\n<div data-bind=\"css: css\">\n  <!-- ko foreach: components -->\n  <!-- ko if: $data.component && !$data.template -->\n  <!-- ko component: { name: component, params: { survey: $parent.survey, model: $data.data, container: $parent.container } } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: $data.template -->\n  <!-- ko template: { name: template, data: $data.data } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- /ko -->\n</div>\n<!-- /ko -->\n<!-- ko ifnot: $data.needRenderWrapper -->\n  <!-- ko foreach: components -->\n  <!-- ko if: $data.component && !$data.template -->\n  <!-- ko component: { name: component, params: { survey: $parent.survey, model: $data.data, container: $parent.container } } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: $data.template -->\n  <!-- ko template: { name: template, data: $data.data } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- /ko -->\n<!-- /ko -->\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/dropdown-select/dropdown-select.html":
/*!**********************************************************************!*\
  !*** ./src/knockout/components/dropdown-select/dropdown-select.html ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.renderCssRoot\">\n  <div data-bind=\"css: question.cssClasses.selectWrapper\">\n    <!-- ko ifnot: question.isReadOnly -->\n    <select data-bind=\"options: question.visibleChoices, \n    optionsValue: 'value', \n    optionsText: 'koText', \n    optionsCaption: question.allowClear ? question.locPlaceholder.koRenderedHtml : undefined, \n    optionsAfterRender: question.koDisableOption, \n    attr: {id: question.inputId, autocomplete: question.autocomplete, required: question.isRequired, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage},\n    click: click,\n    event: { keyup: keyup },\n    disable: question.isInputReadOnly, \n    value: question.renderedValue, \n    valueAllowUnset: true, \n    css: question.getControlClass()\">\n    </select>\n    <!-- /ko -->\n    <!-- ko if: question.isReadOnly -->\n    <div disabled\n      data-bind=\"attr: {id: question.inputId}, text: question.readOnlyText, css: question.getControlClass()\">\n    </div>\n    <!-- /ko -->\n    <!-- ko if: question.cssClasses.chevronButtonIconId -->\n    <div data-bind=\"css: question.cssClasses.chevronButton\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.chevronButtonSvg, iconName: question.cssClasses.chevronButtonIconId, size: 'auto' } } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n  <!-- ko if: question.isOtherSelected -->\n  <div data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': question.isOtherSelected } }, style: {display: question.isFlowLayout ? 'inline': ''}\">\n  </div>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/dropdown/dropdown.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/dropdown/dropdown.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.cssClasses.selectWrapper, click: click\">\n  <!-- ko ifnot: question.isReadOnly -->\n  <div data-bind=\"css: question.getControlClass(),\n    event: { keydown: keyhandler, blur: blur },\n    attr: { \n      id: question.inputId, \n      required: question.isRequired, \n      tabindex: model.noTabIndex ? undefined : 0,\n      disabled: question.isDisabledAttr,\n      role: question.ariaRole,\n      'aria-required': question.ariaRequired, \n      'aria-label': question.ariaLabel, \n      'aria-invalid': question.ariaInvalid, \n      'aria-errormessage': question.ariaErrormessage,\n      'aria-expanded': question.ariaExpanded,\n      'aria-controls': model.listElementId,\n      'aria-activedescendant': model.ariaActivedescendant,\n    },\">\n    <!-- ko if: model.showHintPrefix -->\n    <div data-bind=\"css: question.cssClasses.hintPrefix\">\n      <span data-bind=\"text: model.hintStringPrefix\"></span>\n    </div>\n    <!-- /ko -->\n    <div data-bind=\"css: question.cssClasses.controlValue\">\n      <!-- ko if: model.showHintString -->\n      <div data-bind=\"css: question.cssClasses.hintSuffix\">\n      <span style=\"visibility: hidden\" data-bind=\"text: model.inputStringRendered\"></span>\n      <span data-bind=\"text: model.hintStringSuffix\"></span>\n      </div>\n      <!-- /ko -->\n      <!-- ko if: question.showInputFieldComponent -->\n      <!-- ko component: { name: question.inputFieldComponentName, params: { item: model.getSelectedAction(), question: question } } -->\n      <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.showSelectedItemLocText -->\n      <!-- ko template: { name: 'survey-string', data: question.selectedItemLocText } -->\n      <!-- /ko -->\n      <!-- /ko -->\n      <input type=\"text\" autocomplete=\"off\" data-bind=\"\n      textInput: model.inputStringRendered, \n      css: question.cssClasses.filterStringInput, \n      attr: {\n        'aria-expanded': question.ariaExpanded,\n        'aria-controls': model.listElementId,\n        'aria-activedescendant': model.ariaActivedescendant,\n        'aria-label': question.a11y_input_ariaLabel,\n        'aria-labelledby': question.a11y_input_ariaLabelledBy,\n        'aria-describedby': question.a11y_input_ariaDescribedBy,\n        placeholder: model.placeholderRendered, \n        readonly: model.filterReadOnly || undefined, \n        role: model.filterStringEnabled ? question.ariaRole : undefined,\n        tabindex: model.noTabIndex ? undefined : -1,\n        disabled: question.isDisabledAttr,\n        id: question.getInputId(), \n        inputmode: model.inputMode\n      },\n      event: { blur: blur, focus: focus }\"></input>\n    </div>\n    <!-- ko if: (question.allowClear && question.cssClasses.cleanButtonIconId) -->\n    <div data-bind=\"css: question.cssClasses.cleanButton, click: clear, visible: question.showClearButton\" aria-hidden=\"true\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.cleanButtonSvg, iconName: question.cssClasses.cleanButtonIconId, size: 'auto', title: question.clearCaption } } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n  <!-- ko component: { name: \"sv-popup\", params: { model: model.popupModel }} -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.isReadOnly -->\n  <div data-bind=\"css: question.getControlClass(), attr: { \n      id: question.inputId,\n      'aria-label': question.a11y_input_ariaLabel,\n      'aria-labelledby': question.a11y_input_ariaLabelledBy,\n      'aria-describedby': question.a11y_input_ariaDescribedBy,\n      tabindex: model.isDisabledAttr ? undefined : 0,\n      disabled: model.isDisabledAttr\n    } \">\n    <!-- ko if: question.locReadOnlyText -->\n    <!-- ko template: { name: 'survey-string', data: question.locReadOnlyText } -->\n    <!-- /ko -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <!-- ko if: question.cssClasses.chevronButtonIconId -->\n  <div data-bind=\"css: question.cssClasses.chevronButton, event: {pointerdown: chevronPointerDown}\" aria-hidden=\"true\">\n    <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.chevronButtonSvg, iconName: question.cssClasses.chevronButtonIconId, size: 'auto' } } -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/file/choose-file.html":
/*!*******************************************************!*\
  !*** ./src/knockout/components/file/choose-file.html ***!
  \*******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<label tabindex=\"0\" data-bind=\"css: question.koChooseFileCss, key2click, click: function(d, e) { question.chooseFile(e); }, attr: { for: question.inputId, 'aria-label': question.koGetChooseButtonText() }\">\n  <!-- ko if: question.cssClasses.chooseFileIconId -->\n    <!-- ko component: { name: 'sv-svg-icon', params: { title: question.koGetChooseButtonText(), iconName: question.cssClasses.chooseFileIconId, size: 'auto' } } --><!-- /ko -->\n  <!-- /ko -->\n  <span data-bind=\"text: question.koGetChooseButtonText()\"></span>\n</label>";

/***/ }),

/***/ "./src/knockout/components/file/file-item.html":
/*!*****************************************************!*\
  !*** ./src/knockout/components/file/file-item.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<span data-bind=\"css: question.cssClasses.previewItem, click: question.dodownloadFromContainer\">\n  <!-- ko template: { name: 'survey-question-file-sign', data: {question: question, item: item, fileSignCss: question.cssClasses.fileSign} } --><!-- /ko -->\n  <div data-bind=\"css: question.getImageWrapperCss(item)\">\n    <!-- ko if: question.canPreviewImage(item) -->\n    <img data-bind=\"attr: { src: item.content }, style : { height: question.imageHeight, width: question.imageWidth }\" alt=\"File preview\">\n    <!-- /ko -->\n    <!-- ko if: question.defaultImage(item) -->\n    <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.defaultImage, iconName: question.cssClasses.defaultImageIconId, size: 'auto' } } --><!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: item.name -->\n    <!-- ko ifnot: question.isReadOnly -->\n    <div data-bind=\"click: () => question.doremovefile(item), css: question.getRemoveButtonCss()\">\n        <span data-bind=\"css: question.cssClasses.removeFile, text: question.removeFileCaption\"></span>\n        <!-- ko if: question.cssClasses.removeFileSvgIconId -->\n          <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.removeFileSvg, title: question.removeFileCaption, iconName: question.cssClasses.removeFileSvgIconId, size: 'auto' } } --><!-- /ko -->\n        <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- /ko -->\n  </div>\n  <!-- ko template: { name: 'survey-question-file-sign', data: {question: question, item: item, fileSignCss: question.cssClasses.fileSignBottom} } --><!-- /ko -->\n</span>";

/***/ }),

/***/ "./src/knockout/components/file/file-page.html":
/*!*****************************************************!*\
  !*** ./src/knockout/components/file/file-page.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: model -->\n<div data-bind=\"css: css, attr: { id: id }\">\n  <!-- ko foreach: $data.items -->\n      <!-- ko component: { name: 'sv-file-item', params: { item: $data, question: question } } -->\n      <!-- /ko -->\n  <!-- /ko -->\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/file/file-preview.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/file/file-preview.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: question.koHasValue && question.showPreviewContainer -->\n<div data-bind=\"css: question.cssClasses.fileList, visible: question.koHasValue\">\n  <!-- ko if: question.supportFileNavigator -->\n  <!-- ko foreach: question.renderedPages -->\n  <!-- ko component: { name: 'sv-file-page', params: { model: $data } } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: !question.supportFileNavigator -->\n    <!-- ko foreach: question.koData -->\n      <!-- ko component: { name: 'sv-file-item', params: { item: $data, question: question } } -->\n      <!-- /ko -->\n    <!-- /ko -->\n  <!-- /ko -->\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/header/cell.html":
/*!**************************************************!*\
  !*** ./src/knockout/components/header/cell.html ***!
  \**************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: css, style: style\">\n  <div class=\"sv-header__cell-content\" data-bind=\"style: contentStyle\">\n    <!-- ko if: showLogo -->\n    <div class=\"sv-header__logo\">\n    <!-- ko component: { name: survey.getElementWrapperComponentName(survey, 'logo-image'), params: survey.getElementWrapperComponentData(survey, 'logo-image') } -->\n    <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko if: showTitle -->\n    <div class=\"sv-header__title\" data-bind=\"style: { maxWidth: textAreaWidth }\">\n    <!-- ko component: { name: 'survey-element-title', params: { element: survey } } -->\n    <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko if: showDescription -->\n    <div class=\"sv-header__description\" data-bind=\"style: { maxWidth: textAreaWidth }\">\n      <div data-bind=\"css: survey.css.description\">\n        <!-- ko template: { name: 'survey-string', data: survey.locDescription } -->\n        <!-- /ko -->\n      </div>\n    </div>\n    <!-- /ko -->\n  </div>\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/header/index.html":
/*!***************************************************!*\
  !*** ./src/knockout/components/header/index.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: (survey.headerView === 'advanced') -->\n<div data-bind=\"css: model.headerClasses, style: { height: model.renderedHeight }\">\n  <!-- ko if: !!model.backgroundImage -->\n  <div data-bind=\"style: model.backgroundImageStyle, css: model.backgroundImageClasses\"></div>\n  <!-- /ko -->\n  <!-- ko ifnot: survey.isMobile -->\n  <div data-bind=\"css: model.contentClasses, style: { maxWidth: model.maxWidth }\">\n  <!-- ko foreach: model.cells -->\n    <!-- ko component: { name: 'sv-header-cell', params: { model: $data } } -->\n    <!-- /ko -->\n  <!--/ko-->\n  </div>\n  <!--/ko-->\n  <!-- ko if: survey.isMobile -->\n    <!-- ko component: { name: 'sv-header-mobile', params: { model: model } } -->\n    <!-- /ko -->\n  <!--/ko-->\n  </div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/header/mobile.html":
/*!****************************************************!*\
  !*** ./src/knockout/components/header/mobile.html ***!
  \****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sv-header--mobile\">\n  <!-- ko if: survey.hasLogo -->\n  <div class=\"sv-header__logo\">\n  <!-- ko component: { name: survey.getElementWrapperComponentName(survey, 'logo-image'), params: survey.getElementWrapperComponentData(survey, 'logo-image') } -->\n  <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <!-- ko if: survey.hasTitle -->\n  <div class=\"sv-header__title\" data-bind=\"style: { maxWidth: textAreaWidth }\">\n  <!-- ko component: { name: 'survey-element-title', params: { element: survey } } -->\n  <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <!-- ko if: survey.renderedHasDescription -->\n  <div class=\"sv-header__description\" data-bind=\"style: { maxWidth: textAreaWidth }\">\n    <div data-bind=\"css: survey.css.description\">\n      <!-- ko template: { name: 'survey-string', data: survey.locDescription } -->\n      <!-- /ko -->\n    </div>\n  </div>\n  <!-- /ko -->\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/list/list-item-content.html":
/*!*************************************************************!*\
  !*** ./src/knockout/components/list/list-item-content.html ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: $data.item.iconName -->\n<!-- ko component: { name: \"sv-svg-icon\", params: { iconName: $data.item.iconName, size: $data.item.iconSize, css: $data.model.cssClasses.itemIcon } }-->\n<!-- /ko -->\n<!-- /ko -->\n<!-- ko template: { name: 'survey-string', data: $data.item.locTitle } -->\n<!-- /ko -->\n<!-- ko if: $data.item.markerIconName -->\n<!-- ko component: { name: 'sv-svg-icon', params: { css: $data.item.cssClasses.itemMarkerIcon, iconName: $data.item.markerIconName, size: 'auto' } } -->\n<!-- /ko -->\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/list/list-item-group.html":
/*!***********************************************************!*\
  !*** ./src/knockout/components/list/list-item-group.html ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko component: { name: \"sv-list-item-content\", params: { item: $data.item, model: $data.model } } -->\n<!-- /ko -->\n<sv-popup params=\"{ model: $data.item.popupModel }\"></sv-popup>";

/***/ }),

/***/ "./src/knockout/components/list/list-item.html":
/*!*****************************************************!*\
  !*** ./src/knockout/components/list/list-item.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "\r\n<li role=\"option\"\r\ndata-bind=\"css: $data.model.getItemClass($data.item), attr: { id: $data.item.elementId, 'aria-selected': $data.model.isItemSelected($data.item) ? 'true' : 'false' }, click: itemClick, key2click, visible: $data.model.isItemVisible($data.item), event: { pointerdown: function (model, event) { $data.model.onPointerDown(event, $data.item); } }\">\r\n  <!-- ko if: $data.item.needSeparator -->\r\n  <div data-bind=\"css: $data.model.cssClasses.itemSeparator\"></div>\r\n  <!-- /ko -->\r\n  <div data-bind=\"style: $data.model.getItemStyle($data.item), css: $data.model.cssClasses.itemBody, attr: { title: $data.item.locTitle.calculatedText }, event: { mouseover: function(m, e) { $data.hover(e, $data); return true; }, mouseleave: function(m, e) { $data.leave(e, $data); return true; } }\">\r\n  <!-- ko component: { name: $data.itemComponent, params: { item: $data.item, model: $data.model } } -->\r\n  <!-- /ko -->\r\n  </div>\r\n</li>";

/***/ }),

/***/ "./src/knockout/components/list/list.html":
/*!************************************************!*\
  !*** ./src/knockout/components/list/list.html ***!
  \************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: model.cssClasses.root\">\n  <!-- ko if: $data.model.showFilter -->\n  <div data-bind=\"css: model.cssClasses.filter\">\n    <div data-bind=\"css: model.cssClasses.filterIcon\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-search', size: 'auto' }  } -->\n      <!-- /ko -->\n    </div>\n    <input type=\"text\" \n      data-bind=\"css: model.cssClasses.filterInput, textInput: model.filterString, attr: { placeholder: model.filterStringPlaceholder, 'aria-label': model.filterStringPlaceholder }, event: { keyup: function (model, event) { $data.model.goToItems(event); } }\"></input>\n    <!-- ko if: $data.model.showSearchClearButton && !!$data.model.filterString -->\n    <button data-bind=\"event: { click: (_, event) => { model.onClickSearchClearButton(event); } }, css: model.cssClasses.searchClearButtonIcon\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { iconName: 'icon-searchclear', size: 'auto' }  } -->\n      <!-- /ko -->\n    </button>\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <div data-bind=\"css: model.cssClasses.emptyContainer, visible: $data.model.isEmpty\">\n    <div data-bind=\"css: model.cssClasses.emptyText, text: model.emptyMessage, attr: { 'aria-label': model.emptyMessage }\"></div>\n  </div>\n  <!-- ko if: $data.model.renderElements -->\n  <ul role=\"listbox\"\n    data-bind=\"css: model.getListClass(), visible: !$data.model.isEmpty, attr: { id: model.elementId },\n    event: { mousedown: function (data, e) { e.preventDefault(); }, keydown: function(data, e) { $data.model.onKeyDown(event); return true; }, mousemove: function(data, e) { $data.model.onMouseMove(event); return true; } }\">\n    <!-- ko template: { foreach: model.renderedActions, afterRender: $data.afterItemRender } -->\n    <!-- ko component: { name: 'sv-list-item', params: { item: $data, model: $parent.model } } -->\n    <!-- /ko -->\n    <!-- /ko -->\n  </ul>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/loading-indicator/loading-indicator.html":
/*!**************************************************************************!*\
  !*** ./src/knockout/components/loading-indicator/loading-indicator.html ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sd-loading-indicator\">\n  <!-- ko component: { name: \"sv-svg-icon\", params: { iconName: 'icon-loading', size: 'auto' }  } -->\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/logo-image/logo-image.html":
/*!************************************************************!*\
  !*** ./src/knockout/components/logo-image/logo-image.html ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: survey -->\n<div data-bind=\"css: logoClassNames\">\n  <img data-bind=\"css: css.logoImage, attr: { src: locLogo.koRenderedHtml, width: renderedLogoWidth, height: renderedLogoHeight, alt: locTitle.renderedHtml }, style: { objectFit: logoFit, width: renderedStyleLogoWidth, height: renderedStyleLogoHeight }\">\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/matrix-actions/detail-button/detail-button.html":
/*!*********************************************************************************!*\
  !*** ./src/knockout/components/matrix-actions/detail-button/detail-button.html ***!
  \*********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<button\ntype=\"button\"\ndata-bind=\"css:question.getDetailPanelButtonCss(row), click:row.showHideDetailPanelClick, attr:{ 'aria-expanded': question.getIsDetailPanelShowing($data.row) ? 'true': 'false', 'aria-controls': question.getIsDetailPanelShowing($data.row) ? row.detailPanelId: false}\"\n>\n<!-- ko component: { name: 'sv-svg-icon', params: { css: question.getDetailPanelIconCss(row), iconName: question.getDetailPanelIconId(row), size: 'auto' } } -->\n<!-- /ko -->\n</button>\n<!-- ko if: question.detailPanelMode === \"popup\" && question.getKoPopupIsVisible(row) -->\n<sv-popup\nparams=\"contentComponentName: 'sv-panel', contentComponentData: { question: row.detailPanel, onItemSelect: function(){} }, isVisible: question.getKoPopupIsVisible(row), isModal: true, onHide: function() { row.hideDetailPanel() }, verticalPosition: 'top', horizontalPosition: 'right'\"\n></sv-popup>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/matrix-actions/drag-drop-icon/drag-drop-icon.html":
/*!***********************************************************************************!*\
  !*** ./src/knockout/components/matrix-actions/drag-drop-icon/drag-drop-icon.html ***!
  \***********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div>\n  <!-- ko if: question.iconDragElement -->\n  <svg data-bind=\"css: question.cssClasses.dragElementDecorator\">\n    <use data-bind=\"attr: { 'xlink:href': question.iconDragElement }\" xlink:href=''></use>\n  </svg>\n  <!-- /ko -->\n  <!-- ko ifnot: question.iconDragElement -->\n  <span data-bind=\"css: question.cssClasses.iconDrag\"></span>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/matrix-actions/remove-button/remove-button.html":
/*!*********************************************************************************!*\
  !*** ./src/knockout/components/matrix-actions/remove-button/remove-button.html ***!
  \*********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<button\n  type=\"button\"\n  data-bind=\"click: question.koRemoveRowClick, disable: question.isInputReadOnly, css: question.getRemoveRowButtonCss()\"\n>\n  <!-- ko template: { name: 'survey-string', data: question.locRemoveRowText } --><!-- /ko -->\n  <span data-bind=\"css: question.cssClasses.iconRemove\"></span>\n</button>\n";

/***/ }),

/***/ "./src/knockout/components/notifier/notifier.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/notifier/notifier.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: notifier.isDisplayed -->\n<div data-bind=\"css: notifier.css, style: { visibility: notifier.active ? 'visible' : 'hidden' }\" role=\"alert\" aria-live=\"polite\">\n  <span data-bind=\"text: notifier.message\"></span>\n  <!-- ko component: { name: \"sv-action-bar\", params: { model: notifier.actionBar } } -->\n  <!-- /ko -->\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/paneldynamic-actions/paneldynamic-add-btn.html":
/*!********************************************************************************!*\
  !*** ./src/knockout/components/paneldynamic-actions/paneldynamic-add-btn.html ***!
  \********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: question.koCanAddPanel -->\n<button type=\"button\" data-bind=\"click: question.koAddPanelClick, css: question.koAddButtonCss, visible: question.koCanAddPanel, attr: { id: question.addButtonId }\">\n  <span data-bind=\"css: question.cssClasses.buttonAddText\"><!-- ko template: { name: 'survey-string', data: question.locPanelAddText } --><!-- /ko --></span>\n</button>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/paneldynamic-actions/paneldynamic-next-btn.html":
/*!*********************************************************************************!*\
  !*** ./src/knockout/components/paneldynamic-actions/paneldynamic-next-btn.html ***!
  \*********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"attr: { title: question.panelNextText }, click: question.koNextPanelClick, css: question.koNextButtonCss\">\n    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: question.cssClasses.progressBtnIcon, size: 'auto' } } --><!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/paneldynamic-actions/paneldynamic-prev-btn.html":
/*!*********************************************************************************!*\
  !*** ./src/knockout/components/paneldynamic-actions/paneldynamic-prev-btn.html ***!
  \*********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"attr: { title: question.panelPrevText }, click: question.koPrevPanelClick, css: question.koPrevButtonCss\">\n    <!-- ko component: { name: 'sv-svg-icon', params: { iconName: question.cssClasses.progressBtnIcon, size: 'auto' } } --><!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/paneldynamic-actions/paneldynamic-progress-text.html":
/*!**************************************************************************************!*\
  !*** ./src/knockout/components/paneldynamic-actions/paneldynamic-progress-text.html ***!
  \**************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"text: question.koProgressText, css: question.cssClasses.progressText\"></div>";

/***/ }),

/***/ "./src/knockout/components/paneldynamic-actions/paneldynamic-remove-btn.html":
/*!***********************************************************************************!*\
  !*** ./src/knockout/components/paneldynamic-actions/paneldynamic-remove-btn.html ***!
  \***********************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<button type=\"button\" data-bind=\"click: function() { question.koRemovePanelClick(panel); }, css: question.getPanelRemoveButtonCss(), attr: { id: question.getPanelRemoveButtonId(panel) }\">\n  <span data-bind=\"css: question.cssClasses.buttonRemoveText\"><!-- ko template: { name: 'survey-string', data: question.locPanelRemoveText } --><!-- /ko --></span>\n  <span data-bind=\"css: question.cssClasses.iconRemove\"></span>\n</button>";

/***/ }),

/***/ "./src/knockout/components/question-error/question-error.html":
/*!********************************************************************!*\
  !*** ./src/knockout/components/question-error/question-error.html ***!
  \********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div>\n  <span aria-hidden=\"true\" data-bind=\"css: cssClasses.error.icon\"></span>\n  <span data-bind=\"css: cssClasses.error.item\">\n      <!-- ko template: { name: 'survey-string', data: error.locText } --><!-- /ko -->\n  </span>\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/ranking/item-content.html":
/*!***********************************************************!*\
  !*** ./src/knockout/components/ranking/item-content.html ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: cssClasses.controlLabel\">\n  <!-- ko template: { name: 'survey-string', data: item.locText } -->\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/rating-dropdown/rating-dropdown-item.html":
/*!***************************************************************************!*\
  !*** ./src/knockout/components/rating-dropdown/rating-dropdown-item.html ***!
  \***************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sd-rating-dropdown-item\">\n  <span class=\"sd-rating-dropdown-item_text\" data-bind=\"text: item.title\"></span>\n  <!-- ko if: !!item.description -->\n  <div class=\"sd-rating-dropdown-item_description\">\n    <!-- ko template: { name: 'survey-string', data: item.description } -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/rating-dropdown/rating-dropdown.html":
/*!**********************************************************************!*\
  !*** ./src/knockout/components/rating-dropdown/rating-dropdown.html ***!
  \**********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.cssClasses.rootDropdown\">\n  <!-- ko component: { name: 'sv-dropdown', params: { question: question } } -->\n  <!-- /ko -->\n</div>\n";

/***/ }),

/***/ "./src/knockout/components/rating/rating-item-smiley.html":
/*!****************************************************************!*\
  !*** ./src/knockout/components/rating/rating-item-smiley.html ***!
  \****************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<label data-bind=\"style: question.getItemStyle(item.itemValue, item.highlight), css: question.getItemClass(item.itemValue, item.highlight), event: { mouseover: function () { question.onItemMouseIn(item); }, mouseleave: function () { question.onItemMouseOut(item);}, mousedown: question.koMouseDown }\">\n  <input\n  type=\"radio\"\n  class=\"sv-visuallyhidden\"\n  data-bind=\"attr: { name: question.questionName, id: question.getInputId(index), value: item.value, readonly: question.isReadOnlyAttr, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage }, checkedValue: item.value, enable: !question.isDisabledAttr, event: { click: function(data, event) { question.setValueFromClick(event.target.value); return true; } }\"\n  />\n  <!-- ko component: { name: 'sv-svg-icon', params: { iconName: question.getItemSmileyIconName(item.itemValue), size: 'auto', title: item.text } } --><!-- /ko -->\n</label>";

/***/ }),

/***/ "./src/knockout/components/rating/rating-item-star.html":
/*!**************************************************************!*\
  !*** ./src/knockout/components/rating/rating-item-star.html ***!
  \**************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<label data-bind=\"css: question.getItemClass(item.itemValue, item.highlight), event: { mouseover: function () { question.onItemMouseIn(item); }, mouseleave: function () { question.onItemMouseOut(item);}, mousedown: question.koMouseDown }\">\n  <input\n  type=\"radio\"\n  class=\"sv-visuallyhidden\"\n  data-bind=\"attr: { name: question.questionName, id: question.getInputId(index), value: item.value, readonly: question.isReadOnlyAttr, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage }, checkedValue: item.value, enable: !question.isDisabledAttr, event: { click: function(data, event) { question.setValueFromClick(event.target.value); return true; } }\"\n  />\n  <!-- ko component: { name: 'sv-svg-icon', params: { css: 'sv-star', iconName: question.itemStarIcon, size: 'auto', title: item.text } } --><!-- /ko -->\n  <!-- ko component: { name: 'sv-svg-icon', params: { css: 'sv-star-2', iconName: question.itemStarIconAlt, size: 'auto', title: item.text } } --><!-- /ko -->\n</label>";

/***/ }),

/***/ "./src/knockout/components/rating/rating-item.html":
/*!*********************************************************!*\
  !*** ./src/knockout/components/rating/rating-item.html ***!
  \*********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<label data-bind=\"css: question.getItemClassByText(item.itemValue, item.text),  event: { mousedown: question.koMouseDown }\">\n  <input\n  type=\"radio\"\n  class=\"sv-visuallyhidden\"\n  data-bind=\"attr: { name: question.questionName, id: question.getInputId(index), value: item.value, readonly: question.isReadOnlyAttr, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage }, checkedValue: item.value, enable: !question.isDisabledAttr, event: { click: function(data, event) { question.setValueFromClick(event.target.value); return true; } }\"\n  />\n  <span data-bind=\"css: question.cssClasses.itemText, attr: {'data-text': item.text }\">\n  <!-- ko template: { name: 'survey-string', data: item.locText } -->\n  <!-- /ko -->\n  </span>\n</label>\n";

/***/ }),

/***/ "./src/knockout/components/skeleton/skeleton.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/skeleton/skeleton.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sv-skeleton-element\" data-bind=\"attr: { id: element.id }, style: { height: element.skeletonHeight }\">\n</div>";

/***/ }),

/***/ "./src/knockout/components/string-editor/string-editor.html":
/*!******************************************************************!*\
  !*** ./src/knockout/components/string-editor/string-editor.html ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- <input class=\"sv-string-editor\" data-bind=\"value: editValue\" /> -->\n\n<!-- ko ifnot: koHasHtml -->\n<span class=\"sv-string-editor\" data-bind=\"text: editValue, event: { blur: onInput, click: onClick, clickBubble: false }\" contenteditable=\"true\"></span>\n<!-- /ko -->\n<!-- ko if: koHasHtml -->\n<span class=\"sv-string-editor\" data-bind=\"html: editValue, event: { blur: onInput, click: onClick, clickBubble: false }\" contenteditable=\"true\"></span>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/string-viewer/string-viewer.html":
/*!******************************************************************!*\
  !*** ./src/knockout/components/string-viewer/string-viewer.html ***!
  \******************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko ifnot: locString.koHasHtml -->\n<span class=\"sv-string-viewer\" data-bind=\"text: locString.koRenderedHtml, css: {'sv-string-viewer--multiline': locString.allowLineBreaks}\"></span>\n<!-- /ko -->\n<!-- ko if: locString.koHasHtml -->\n<span class=\"sv-string-viewer\" data-bind=\"html: locString.koRenderedHtml, css: {'sv-string-viewer--multiline': locString.allowLineBreaks}\"></span>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/survey-actions/survey-nav-button.html":
/*!***********************************************************************!*\
  !*** ./src/knockout/components/survey-actions/survey-nav-button.html ***!
  \***********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko with: $data.item  -->\n  <input type=\"button\" data-bind=\"event: { mousedown: $data.data && $data.data.mouseDown }, value: $data.title, click: $data.action, visible: $data.visible, css: $data.innerCss, disable: $data.disabled, attr: { title: $data.getTooltip() }\"/>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/svg-icon/svg-icon.html":
/*!********************************************************!*\
  !*** ./src/knockout/components/svg-icon/svg-icon.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: hasIcon -->\n<svg class=\"sv-svg-icon\" data-bind=\"css: css\" role=\"img\"><use></use></svg>\n<!-- /ko -->\n";

/***/ }),

/***/ "./src/knockout/components/tagbox/tagbox-item.html":
/*!*********************************************************!*\
  !*** ./src/knockout/components/tagbox/tagbox-item.html ***!
  \*********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div class=\"sv-tagbox__item\">\n  <div class=\"sv-tagbox__item-text\">\n    <!-- ko template: { name: 'survey-string', data: item.locText } -->\n    <!-- /ko -->\n  </div>\n  <div data-bind=\"css: question.cssClasses.cleanItemButton, click: removeItem\">\n    <sv-svg-icon params=\"iconName: question.cssClasses.cleanItemButtonIconId, css: question.cssClasses.cleanItemButtonSvg, size:'auto' \"></sv-svg-icon>\n  </div>\n</div>";

/***/ }),

/***/ "./src/knockout/components/tagbox/tagbox.html":
/*!****************************************************!*\
  !*** ./src/knockout/components/tagbox/tagbox.html ***!
  \****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<div data-bind=\"css: question.cssClasses.selectWrapper, click: click\">\n  <!-- ko ifnot: question.isReadOnly -->\n  <div data-bind=\"css: question.getControlClass(),\n    event: { keydown: keyhandler, blur: blur },\n    attr: { \n      id: question.inputId, \n      required: question.isRequired, \n      tabindex: model.noTabIndex ? undefined : 0,\n      disabled: question.isDisabledAttr,\n      role: question.ariaRole,\n      'aria-required': question.ariaRequired, \n      'aria-label': question.ariaLabel, \n      'aria-invalid': question.ariaInvalid, \n      'aria-errormessage': question.ariaErrormessage,\n      'aria-expanded': question.ariaExpanded,\n      'aria-controls': model.listElementId,\n      'aria-activedescendant': model.ariaActivedescendant, \n    },\">\n    <div data-bind=\"css: question.cssClasses.controlValue\">\n      <!-- ko foreach: question.selectedChoices -->\n      <!-- ko component: { name: 'sv-tagbox-item', params: { item: $data, question: question } } -->\n      <!-- /ko -->\n      <!-- /ko -->\n      <div data-bind=\"css: question.cssClasses.hint\">\n        <!-- ko if: model.showHintPrefix -->\n        <div data-bind=\"css: question.cssClasses.hintPrefix\">\n          <span data-bind=\"text: model.hintStringPrefix\"></span>\n        </div>\n        <!-- /ko -->\n        <div data-bind=\"css: question.cssClasses.hintSuffixWrapper\">\n          <!-- ko if: model.showHintString -->\n          <div data-bind=\"css: question.cssClasses.hintSuffix\">\n            <span style=\"visibility: hidden\" data-bind=\"text: model.inputStringRendered\"></span>\n            <span data-bind=\"text: model.hintStringSuffix\"></span>\n            </div>\n          <!-- /ko -->\n          <input type=\"text\" autocomplete=\"off\" data-bind=\"textInput: model.inputStringRendered, \n          css: question.cssClasses.filterStringInput, \n          attr: { \n            inputmode: model.inputMode,\n            size: !model.inputStringRendered ? 1 : null, \n            id: question.getInputId(), \n            role: model.filterStringEnabled ? question.ariaRole : undefined,\n            'aria-expanded': question.ariaExpanded,\n            'aria-controls': model.listElementId,\n            'aria-activedescendant': model.ariaActivedescendant,\n            'aria-label': question.a11y_input_ariaLabel,\n            'aria-labelledby': question.a11y_input_ariaLabelledBy,\n            'aria-describedby': question.a11y_input_ariaDescribedBy,\n            placeholder: model.filterStringPlaceholder, \n            disabled: question.isDisabledAttr,\n            readonly: model.filterReadOnly\n          },\n          event: { keydown: inputKeyHandler, blur: blur, focus: focus }\"></input>\n        </div>\n      </div>\n    </div>\n    <!-- ko if: (question.allowClear && question.cssClasses.cleanButtonIconId) -->\n    <div data-bind=\"css: question.cssClasses.cleanButton, click: clear, visible: question.showClearButton\" aria-hidden=\"true\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.cleanButtonSvg, iconName: question.cssClasses.cleanButtonIconId, size: 'auto', title: question.clearCaption } } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n  <!-- ko component: { name: \"sv-popup\", params: { model: model.popupModel }} -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.isReadOnly -->\n  <div disabled data-bind=\"css: question.getControlClass(), attr: {\n    id: question.inputId,\n    'aria-label': question.a11y_input_ariaLabel,\n    'aria-labelledby': question.a11y_input_ariaLabelledBy,\n    'aria-describedby': question.a11y_input_ariaDescribedBy,\n    tabindex: model.isDisabledAttr ? undefined : 0,\n    disabled: model.isDisabledAttr } \">\n    <!-- ko if: question.locReadOnlyText -->\n    <!-- ko template: { name: 'survey-string', data: question.locReadOnlyText } -->\n    <!-- /ko -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <!-- ko if: question.cssClasses.chevronButtonIconId -->\n  <div data-bind=\"css: question.cssClasses.chevronButton, event: {pointerdown: chevronPointerDown}\" aria-hidden=\"true\">\n    <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.chevronButtonSvg, iconName: question.cssClasses.chevronButtonIconId, size: 'auto' } } -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n</div>";

/***/ }),

/***/ "./src/knockout/components/template-renderer/template-renderer.html":
/*!**************************************************************************!*\
  !*** ./src/knockout/components/template-renderer/template-renderer.html ***!
  \**************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: templateData.name -->\n  <!-- ko template: { name: templateData.name, data: templateData.data, afterRender: templateData.afterRender } -->\n  <!-- /ko -->\n<!-- /ko -->\n<!-- ko ifnot: templateData.name -->\n  <!-- ko template: { nodes: templateData.nodes || $componentTemplateNodes, data: templateData.data, afterRender: templateData.afterRender } -->\n  <!-- /ko -->\n<!-- /ko -->\n";

/***/ }),

/***/ "./src/knockout/components/text-area/text-area.html":
/*!**********************************************************!*\
  !*** ./src/knockout/components/text-area/text-area.html ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<textarea data-bind=\"\n  attr: { \n    id: $data.model.id, \n    'readonly': $data.model.isReadOnlyAttr, \n    'disabled': $data.model.isDisabledAttr, \n    maxLength: $data.model.maxLength, \n    cols: $data.model.cols, \n    rows: $data.model.rows, \n    placeholder: $data.model.placeholder, \n    'aria-required': $data.model.ariaRequired,\n    'aria-label': $data.model.ariaLabel,\n    'aria-labelledby': $data.model.ariaLabelledBy, \n    'aria-describedby': $data.model.ariaDescribedBy, \n    'aria-invalid': $data.model.ariaInvalid, \n    'aria-errormessage': $data.model.ariaErrormessage\n  }, \n  event: { \n    focus: function(s, e) { $data.model.onTextAreaFocus(e); return true; }, \n    blur: function(s, e) { $data.model.onTextAreaBlur(e); return true; },\n    input: function(s, e) { $data.model.onTextAreaInput(e); },\n    keydown: function(s, e) { $data.model.onTextAreaKeyDown(e); return true; }\n  }, \n  value: $data.value, \n  css: $data.model.className,\n  style: { resize: $data.model.question.resizeStyle },\n\"></textarea>\n";

/***/ }),

/***/ "./src/knockout/components/title/title-actions.html":
/*!**********************************************************!*\
  !*** ./src/knockout/components/title/title-actions.html ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko ifnot: element.hasTitleActions -->\n  <!-- ko component: { name: 'survey-element-title-content', params: {element: element } } --><!-- /ko -->\n<!-- /ko -->\n<!-- ko if: element.hasTitleActions -->\n<div class=\"sv-title-actions\">\n  <span class=\"sv-title-actions__title\">\n    <!-- ko component: { name: 'survey-element-title-content', params: {element: element } } --><!-- /ko -->\n  </span>\n  <!-- ko component: { name: 'sv-action-bar', params: { model: toolbar } } -->\n  <!-- /ko -->\n</div>\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/components/title/title-content.html":
/*!**********************************************************!*\
  !*** ./src/knockout/components/title/title-content.html ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<!-- ko if: element.isTitleRenderedAsString -->\n  <!-- ko template: { name: 'survey-string', data: element.locTitle } --><!-- /ko -->\n<!-- /ko -->\n<!-- ko ifnot: element.isTitleRenderedAsString -->\n  <!-- ko if: element.isRequireTextOnStart -->\n  <span\n    data-bind=\"css: element.cssRequiredText, text: element.requiredText, attr: { 'aria-hidden': true }\"\n  ></span>\n  <!-- /ko -->\n  <!-- ko if: element.no -->\n  <span\n    style=\"position: static;\"\n    data-bind=\"css: element.cssTitleNumber, text: element.no, attr: { 'aria-hidden': true }\"\n  ></span>\n  <span>&nbsp</span>\n  <!-- /ko -->\n  <!-- ko if: element.isRequireTextBeforeTitle -->\n  <span\n    data-bind=\"css: element.cssRequiredText, text: element.requiredText, attr: { 'aria-hidden': true }\"\n  ></span>\n  <span>&nbsp</span>\n  <!-- /ko -->\n  <!-- ko template: { name: 'survey-string', data: element.locTitle } --><!-- /ko -->\n  <!-- ko if: element.isRequireTextAfterTitle -->\n  <span>&nbsp</span>\n  <span\n    data-bind=\"css: element.cssRequiredText, text: element.requiredText, attr: { 'aria-hidden': true }\"\n  ></span>\n  <!-- /ko -->\n<!-- /ko -->";

/***/ }),

/***/ "./src/knockout/templates/comment.html":
/*!*********************************************!*\
  !*** ./src/knockout/templates/comment.html ***!
  \*********************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-comment\">\n<!-- ko if: !question.isReadOnlyRenderDiv() -->\n<!-- ko component: { name: 'sv-text-area', params: question.commentTextAreaModel } -->\n<!-- /ko -->\n<!-- /ko-->\n<!-- ko if: question.isReadOnlyRenderDiv() -->\n<div data-bind=\"text: question.comment\"></div>\n<!--/ko-->\n</script>\n<script type=\"text/html\" id=\"survey-other\">\n<!-- ko if: !question.isReadOnlyRenderDiv() -->\n<!-- ko component: { name: 'sv-text-area', params: question.otherTextAreaModel } -->\n<!-- /ko -->\n<!-- /ko-->\n<!-- ko if: question.isReadOnlyRenderDiv() -->\n<div data-bind=\"text: question.otherValue\"></div>\n<!-- /ko-->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/flowpanel.html":
/*!***********************************************!*\
  !*** ./src/knockout/templates/flowpanel.html ***!
  \***********************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-flowpanel\">\n  <div data-bind=\"style: { flexBasis: renderWidth, flexGrow: 1, flexShrink: 1, width: renderWidth, minWidth: $data.minWidth, maxWidth: $data.maxWidth }, attr: { id: id }, css: cssClasses.panel.container\">\n      <h4 data-bind=\"visible: (processedTitle.length > 0), css: question.cssTitle\">\n          <!-- ko template: { name: 'survey-string', data: locTitle } -->\n          <!-- /ko -->\n      </h4>\n      <div data-bind=\"css: cssClasses.panel.description\">\n          <!-- ko template: { name: 'survey-string', data: locDescription } -->\n          <!-- /ko -->\n      </div>\n      <div data-bind=\"style: { paddingLeft: innerPaddingLeft }\"></div>\n      <f-panel params=\"question: question\" data-bind=\"attr: { contenteditable : question.isDesignMode, placeHolder: question.placeHolder }\"></f-panel>\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-flowpanel-question\">\n  <!-- ko with: $parent.question.getQuestionByName($data) -->\n    <!-- ko template: { name: koElementType(), data: $data, as: 'question', afterRender: parent.koElementAfterRender } --><!-- /ko -->\n  <!-- /ko -->\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/header.html":
/*!********************************************!*\
  !*** ./src/knockout/templates/header.html ***!
  \********************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-header\">\n  <!-- ko if: renderedHasHeader -->\n<div data-bind=\"css: css.header\">\n  <!-- ko if: isLogoBefore -->\n  <!-- ko component: { name: getElementWrapperComponentName($data, 'logo-image'), params: getElementWrapperComponentData($data, 'logo-image') } -->\n  <!-- /ko -->\n  <!-- /ko -->\n\n  <!-- ko if: renderedHasTitle -->\n  <div data-bind=\"css: css.headerText, style: { maxWidth: titleMaxWidth }\">\n    <!-- ko component: { name: 'survey-element-title', params: {element: $data } } -->\n    <!-- /ko -->\n    <!-- ko if: renderedHasDescription -->\n    <div data-bind=\"css: css.description\">\n      <!-- ko template: { name: 'survey-string', data: locDescription } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n\n  <!-- ko if: isLogoAfter -->\n  <!-- ko component: { name: getElementWrapperComponentName($data, 'logo-image'), params: getElementWrapperComponentData($data, 'logo-image') } -->\n  <!-- /ko -->\n  <!-- /ko -->\n  <div data-bind=\"css: css.headerClose\"></div>\n</div>\n<!-- /ko -->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/index.html":
/*!*******************************************!*\
  !*** ./src/knockout/templates/index.html ***!
  \*******************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-content\">\n    <!-- ko template: { name: \"survey-content-template\", afterRender: $data.implementor.koEventAfterRender } -->\n    <!-- /ko -->\n</script>\n\n<script type=\"text/html\" id=\"survey-content-template\">\n  <div data-bind=\"css: rootCss, elementStyle: themeVariables, attr: { lang: locale || 'en', dir: localeDir }\">\n    <!-- ko if: needRenderIcons -->\n      <!-- ko component: { name: 'sv-svg-bundle'} -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <div data-bind=\"css: wrapperFormCss\">\n      <!-- ko if: !!renderBackgroundImage -->\n      <div data-bind=\"css: css.rootBackgroundImage, elementStyle: backgroundImageStyle\"></div>\n      <!-- /ko -->\n      <form onsubmit=\"return false;\">\n          <div class=\"sv_custom_header\" data-bind=\"visible: !hasLogo\"></div>\n          <div data-bind=\"css: containerCss\">\n              <!-- ko if: headerView === 'basic' -->\n              <!-- ko template: { name: koTitleTemplate, afterRender: koAfterRenderHeader } -->\n              <!-- /ko -->\n              <!-- /ko -->\n              <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"header\", needRenderWrapper: false } } --><!-- /ko -->\n              <!-- ko if: isShowingPage -->\n              <div data-bind=\"css: $data.bodyContainerCss\">\n                  <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"left\" } } --><!-- /ko -->\n                  <div class=\"sv-components-column sv-components-column--expandable\">\n                    <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"center\" } } --><!-- /ko -->\n                    <div data-bind=\"css: bodyCss, style:{maxWidth: renderedWidth}, attr: { id: activePage ? activePage.id : '' }\">\n                          <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"contentTop\" } } --><!-- /ko -->\n                          <!-- ko if: activePage -->\n                          <!-- ko template: { name: 'survey-page', data: activePage, afterRender: koAfterRenderPage } -->\n                          <!-- /ko -->\n                          <!-- ko if: activePage.rows.length == 0 && $data.emptyPageTemplate -->\n                          <!-- ko template: { name: emptyPageTemplate, data: $data.emptyPageTemplateData || $data } -->\n                          <!-- /ko -->\n                          <!-- /ko -->\n                          <!-- /ko -->\n                          <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"contentBottom\" } } --><!-- /ko -->\n                          <!-- ko if: showBrandInfo -->\n                            <sv-brand-info></sv-brand-info>\n                          <!-- /ko -->\n                    </div>\n                  </div>\n                  <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"right\" } } --><!-- /ko -->\n              </div>\n              <!-- /ko -->\n              <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"footer\", needRenderWrapper: false } } --><!-- /ko -->\n              <!-- ko if: state == \"completed\" && showCompletedPage -->\n              <div data-bind=\"html: koProcessedCompletedHtml, css: completedCss\"></div>\n              <!-- ko component: { name: \"sv-components-container\", params: { survey: $data, container: \"completePage\", needRenderWrapper: false } } --><!-- /ko -->\n              <!-- /ko -->\n              <!-- ko if: state == \"completedbefore\" -->\n              <div data-bind=\"html: locCompletedBeforeHtml.koRenderedHtml, css: completedBeforeCss\"></div>\n              <!-- /ko -->\n              <!-- ko if: state == \"loading\" -->\n              <div data-bind=\"html: locLoadingHtml.koRenderedHtml, css: loadingBodyCss\"></div>\n              <!-- /ko -->\n              <!-- ko if: state == \"empty\" -->\n              <div data-bind=\"text:emptySurveyText, css: css.bodyEmpty\"></div>\n              <!-- /ko -->\n          </div>\n      </form>\n      <!-- ko component: { name: 'sv-notifier', params: { notifier: notifier } } -->\n      <!-- /ko -->\n    </div>\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/page.html":
/*!******************************************!*\
  !*** ./src/knockout/templates/page.html ***!
  \******************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-page\">\n  <div data-bind=\"css: cssRoot\">\n    <!-- ko component: { name: 'survey-element-title', params: {element: $data } } --><!-- /ko -->\n    <!-- ko if: _showDescription-->\n    <div\n      data-bind=\"visible: data.showPageTitles, css: cssClasses.page?.description\"\n    >\n      <!-- ko template: { name: 'survey-string', data: locDescription } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko template: { name: 'survey-question-errors', data: $data, as: 'question' } -->\n    <!-- /ko -->\n    <!-- ko template: { name: 'survey-rows', data: $data} -->\n    <!-- /ko -->\n  </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/panel.html":
/*!*******************************************!*\
  !*** ./src/knockout/templates/panel.html ***!
  \*******************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-panel\">\n  <!-- ko if: $data.getIsContentVisible() -->\n  <div\n    data-bind=\"attr: { id: id }, css: $data.getContainerCss(), event: {focusin: focusIn}\"\n  >\n    <!-- ko if: showErrorsAbovePanel-->\n      <!-- ko template: { name: 'survey-question-errors', data: $data } -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: hasDescription || hasTitle  -->\n        <!--ko template: { name: 'survey-question-title', data: $data  } --><!-- /ko -->\n    <!-- /ko -->\n    <!-- ko ifnot: showErrorsAbovePanel-->\n      <!-- ko template: { name: 'survey-question-errors', data: $data } -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: renderedIsExpanded -->\n    <div\n      data-bind=\"style: { paddingLeft: innerPaddingLeft }, css: cssClasses.panel.content, attr: {id:contentId}\"\n    >\n      <!-- ko template: { name: 'survey-rows', data: $data} -->\n      <!-- /ko -->\n      <!-- ko component: { name: 'sv-action-bar', params: { model: getFooterToolbar() } } -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/popup-pointer.html":
/*!***************************************************!*\
  !*** ./src/knockout/templates/popup-pointer.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"popup-pointer\">\n  <span class=\"sv-popup__pointer\" data-bind=\"style: { left: pointerTarget.left, top: pointerTarget.top }\"></span>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-boolean.html":
/*!******************************************************!*\
  !*** ./src/knockout/templates/question-boolean.html ***!
  \******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-boolean\">\n  <div data-bind=\"css: question.cssClasses.root, event: { keydown: question.onKeyDown}\">\n    <label data-bind=\"css: question.getItemCss()\">\n      <input\n        type=\"checkbox\"\n        data-bind=\"value: question.booleanValue, css: question.cssClasses.control, attr: {name: question.name, id: question.inputId, 'role': question.a11y_input_ariaRole, 'aria-required': question.a11y_input_ariaRequired, 'aria-labelledby': question.a11y_input_ariaLabelledBy, 'aria-describedby': question.a11y_input_ariaDescribedBy, 'aria-invalid': question.a11y_input_ariaInvalid, 'aria-errormessage': question.a11y_input_ariaErrormessage, 'aria-label': question.a11y_input_ariaLabel, readonly: question.isReadOnlyAttr}, checked: question.booleanValue, surveyProp: {indeterminate: question.isIndeterminate}, enable: !question.isDisabledAttr\"\n      />\n      <div data-bind=\"css: question.cssClasses.sliderGhost, click: onFalseLabelClick\">\n        <span data-bind=\"css: question.getLabelCss(swapOrder)\">\n          <!-- ko template: { name: 'survey-string', data: locLabelLeft } --><!-- /ko -->\n        </span>\n      </div>\n      <div data-bind=\"css: question.cssClasses.switch, click: onSwitchClick\">\n        <span data-bind=\"css: question.cssClasses.slider\">\n            <!-- ko if: question.cssClasses.sliderText && question.isDeterminated -->\n            <span data-bind=\"css: question.cssClasses.sliderText\">\n              <!-- ko template: { name: 'survey-string', data: question.getCheckedLabel() } --><!-- /ko -->\n            </span>\n            <!-- /ko -->\n        </span>\n      </div>\n      <div data-bind=\"css: question.cssClasses.sliderGhost, click: onTrueLabelClick\">\n        <span data-bind=\"css: question.getLabelCss(!swapOrder)\">\n          <!-- ko template: { name: 'survey-string', data: locLabelRight } --><!-- /ko -->\n        </span>\n      </div>\n    </label>\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-buttongroup.html":
/*!**********************************************************!*\
  !*** ./src/knockout/templates/question-buttongroup.html ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-buttongroup\">\n  <div role=\"group\" data-bind=\"css: question.cssClasses.root\">\n      <!-- ko foreach: question.visibleChoices -->\n        <!-- ko component: { name: 'sv-button-group-item', params: { question: question, item: $data, index: $index } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n    </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-checkbox.html":
/*!*******************************************************!*\
  !*** ./src/knockout/templates/question-checkbox.html ***!
  \*******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-checkbox\">\n  <fieldset data-bind=\"css: question.getSelectBaseRootCss(), attr: { 'role': question.a11y_input_ariaRole, 'aria-required': question.a11y_input_ariaRequired, 'aria-labelledby': question.a11y_input_ariaLabelledBy, 'aria-describedby': question.a11y_input_ariaDescribedBy, 'aria-invalid': question.a11y_input_ariaInvalid, 'aria-errormessage': question.a11y_input_ariaErrormessage, 'aria-label': question.a11y_input_ariaLabel }\">\n      <legend data-bind=\"text: question.locTitle.renderedHtml\" class=\"sv-hidden\"></legend>\n      <!-- ko if: question.hasHeadItems  -->\n        <!-- ko foreach: { data: question.headItems, as: 'item', afterRender: question.koAfterRender }  -->\n          <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n          <!-- /ko -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko ifnot: question.hasColumns  -->\n        <!-- ko if: question.blockedRow -->\n        <div data-bind=\"css: question.cssClasses.rootRow\">\n          <!-- ko foreach: { data: question.dataChoices, as: 'item', afterRender: question.koAfterRender }  -->\n          <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n          <!-- /ko -->\n          <!-- /ko -->\n        </div>\n        <!-- /ko -->\n        <!-- ko ifnot: question.blockedRow -->\n        <!-- ko foreach: { data: question.bodyItems, as: 'item', afterRender: question.koAfterRender }  -->\n          <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n          <!-- /ko -->\n        <!-- /ko -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.hasColumns  -->\n        <div data-bind=\"css: question.cssClasses.rootMultiColumn\">\n        <!-- ko foreach: question.columns -->\n            <div data-bind=\"css: question.getColumnClass()\" role=\"presentation\">\n            <!-- ko foreach: { data: $data, as: 'item', afterRender: question.koAfterRender }  -->\n              <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n              <!-- /ko -->\n            <!-- /ko -->\n            </div>\n        <!-- /ko -->\n        </div>\n      <!-- /ko -->\n      <!-- ko if: question.hasFootItems  -->\n        <!-- ko foreach: { data: question.footItems, as: 'item', afterRender: question.koAfterRender }  -->\n          <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n          <!-- /ko -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.hasOther && question.isOtherSelected -->\n      <div data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': question.isOtherSelected } }\"></div>\n      <!-- /ko -->\n    </fieldset>\n</script>\n\n<script type=\"text/html\" id=\"survey-checkbox-item\">\n  <div role=\"presentation\" data-bind=\"css: question.getItemClass($data)\">\n      <label data-bind=\"css: question.getLabelClass($data)\">\n          <input type=\"checkbox\" data-bind=\"attr: {name: question.name + id, id: question.getItemId($data), readonly: question.isReadOnlyAttr, required: question.hasRequiredError()}, value: $data.value, checked: question.isItemSelected($data), event: { change: (i, e) => { question.clickItemHandler($data, e.target.checked); } }, enable: question.getItemEnabled($data), css: question.cssClasses.itemControl\"/>\n          <!-- ko if: question.cssClasses.materialDecorator -->\n          <span data-bind=\"css: question.cssClasses.materialDecorator\">\n            <!-- ko if: question.itemSvgIcon -->\n            <svg data-bind=\"css:question.cssClasses.itemDecorator\">\n              <use data-bind=\"attr:{'xlink:href':question.itemSvgIcon}\" xlink:href=''></use>\n            </svg>\n            <!-- /ko -->\n          </span>\n          <!-- /ko -->\n          <!-- ko if: !$data.hideCaption -->\n          <span data-bind=\"css: question.cssClasses.controlLabel\">\n          <!-- ko template: { name: 'survey-string', data: $data.locText } -->\n          <!-- /ko -->\n          </span>\n          <!-- /ko -->\n      </label>\n  </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-comment.html":
/*!******************************************************!*\
  !*** ./src/knockout/templates/question-comment.html ***!
  \******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-comment\">\n<!-- ko if: !question.isReadOnlyRenderDiv() -->\n  <!-- ko component: { name: 'sv-text-area', params: question.textAreaModel } -->\n  <!-- /ko -->\n  <!-- ko if: question.getMaxLength() -->\n  <!-- ko component: { name: 'sv-character-counter', params: { counter: question.characterCounter, remainingCharacterCounter: question.cssClasses.remainingCharacterCounter } } -->\n  <!-- /ko -->\n  <!-- /ko-->\n<!--/ko-->\n\n<!-- ko if: question.isReadOnlyRenderDiv() -->\n<div data-bind=\"text: question.value\"></div>\n<!-- /ko-->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-composite.html":
/*!********************************************************!*\
  !*** ./src/knockout/templates/question-composite.html ***!
  \********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-composite\">\n  <!-- ko template: { name: 'survey-panel', data: question.contentPanel, as: 'question', afterRender: question.contentPanel.koPanelAfterRender } -->\n  <!-- /ko -->\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-custom.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/question-custom.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-custom\">\n    <!-- ko if: question.contentQuestion.isDefaultRendering() -->\n      <!-- ko template: { name: question.contentQuestion.koTemplateName(), data: question.contentQuestion, as: 'question', afterRender: question.contentQuestion.koQuestionAfterRender } -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko ifnot: question.contentQuestion.isDefaultRendering() -->\n      <!-- ko component: { name: question.contentQuestion.getComponentName(), params: { question: question.contentQuestion } } -->\n      <!-- /ko -->\n    <!-- /ko -->\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-dropdown.html":
/*!*******************************************************!*\
  !*** ./src/knockout/templates/question-dropdown.html ***!
  \*******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-dropdown\">\n  <div data-bind=\"css: question.renderCssRoot\">\n    <!-- ko component: { name: 'sv-dropdown', params: { question: question } } -->\n    <!-- /ko -->\n  <!-- ko if: question.isOtherSelected -->\n  <div data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': question.isOtherSelected } }, style: {display: question.isFlowLayout ? 'inline': ''}\">\n  </div>\n  <!-- /ko -->\n  </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-empty.html":
/*!****************************************************!*\
  !*** ./src/knockout/templates/question-empty.html ***!
  \****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-empty\">\n    <div></div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-errors.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/question-errors.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-errors\">\n        <!-- ko if: hasVisibleErrors -->\n            <div role=\"alert\" aria-live=\"polite\" data-bind=\"visible: hasVisibleErrors, foreach: { data: errors, as: 'error' }, css: cssError, attr: { id: question.id + '_errors' }\">\n            <!-- ko if: error.visible -->\n            <!-- ko component: { name: question.survey.questionErrorComponent, params: { error: error, cssClasses: question.cssClasses, element: question } } -->\n            <!-- /ko -->\n            <!-- /ko -->\n        </div>\n        <!-- /ko -->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-expression.html":
/*!*********************************************************!*\
  !*** ./src/knockout/templates/question-expression.html ***!
  \*********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-expression\">\n  <div data-bind=\"text:question.formatedValue, css: question.cssClasses.root\"></div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-file.html":
/*!***************************************************!*\
  !*** ./src/knockout/templates/question-file.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-file\">\n  <div data-bind=\"css: question.fileRootCss\">\n        <!-- ko ifnot: question.isInputReadOnly -->\n          <!-- ko if: question.hasFileUI -->\n          <input type=\"file\" tabindex=\"-1\" data-bind=\"css: question.cssClasses.fileInput, attr: { id: question.inputId, 'aria-required': question.ariaRequired, 'aria-label': question.ariaLabel, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage, multiple: question.allowMultiple ? 'multiple' : undefined, title: koInputTitle, accept: question.acceptedTypes, capture: question.renderCapture }\">\n          <!-- /ko -->\n        <!-- /ko -->\n        <!-- ko if: question.isReadOnlyAttr -->\n        <input type=\"file\" readonly data-bind=\"css: question.getReadOnlyFileCss(), attr: { id: question.inputId, placeholder: question.title, multiple: question.allowMultiple ? 'multiple' : undefined }\" style=\"color: transparent;\"/>\n        <!-- /ko -->\n        <!-- ko if: question.isDisabledAttr -->\n        <input type=\"file\" disabled data-bind=\"css: question.getReadOnlyFileCss(), attr: { id: question.inputId, placeholder: question.title, multiple: question.allowMultiple ? 'multiple' : undefined }\" style=\"color: transparent;\"/>\n        <!-- /ko -->\n        <div data-bind=\"css: question.cssClasses.dragArea, event: { dragenter: question.ondragenter, dragover: question.ondragover, drop: question.ondrop, dragleave: question.ondragleave }\">     \n          <!-- ko if: question.showFileDecorator -->\n          <div data-bind=\"css: question.getFileDecoratorCss()\">\n            <!-- ko if: question.showDragAreaPlaceholder -->\n            <span data-bind=\"css: question.cssClasses.dragAreaPlaceholder\">\n              <!-- ko template: { name: 'survey-string', data: question.locRenderedPlaceholder } -->\n              <!-- /ko -->\n            </span>\n            <!-- /ko -->\n            <div data-bind=\"css: question.cssClasses.wrapper\">\n              <!-- ko if: question.showChooseButton -->\n                <!-- ko component: { name: 'sv-file-choose-btn' } -->\n                <!-- /ko -->\n              <!-- /ko -->\n              <!-- ko if: question.actionsContainerVisible -->\n              <!-- ko component: { name: 'sv-action-bar', params: { model: question.actionsContainer } } -->\n              <!-- /ko -->\n              <!-- /ko -->\n              <!-- ko if: !question.koHasValue() -->\n              <span data-bind=\"css: question.cssClasses.noFileChosen, text: question.noFileChosenCaption\"></span>\n              <!-- /ko -->\n            </div>\n          </div>\n          <!-- /ko -->\n          <!-- ko if: question.showLoadingIndicator -->\n          <div data-bind=\"css: question.cssClasses.loadingIndicator\">\n            <!-- ko component: { name: \"sv-loading-indicator\" } -->\n            <!-- /ko -->\n          </div>\n          <!-- /ko -->\n          <!-- ko if: question.isPlayingVideo -->\n          <!-- ko template: { name: 'survey-question-file-video', data: { question: question } } --><!-- /ko -->          \n          <!-- /ko -->\n          <!-- ko template: { name: 'survey-question-file-clean-button', data: {question: question, showRemoveButton: question.showRemoveButton} } --><!-- /ko -->\n          <!-- ko if: question.allowShowPreview -->\n          <!-- ko component: { name: 'sv-file-preview', data: { question: question } } --><!-- /ko -->          \n          <!-- /ko -->\n          <!-- ko template: { name: 'survey-question-file-clean-button', data: {question: question, showRemoveButton: question.showRemoveButtonBottom} } --><!-- /ko -->\n          <!-- ko if: question.fileNavigatorVisible -->\n          <!-- ko component: { name: 'sv-action-bar', params: { model: question.fileNavigator } } -->\n          <!-- /ko -->\n          <!-- /ko -->\n        </div>\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-question-file-clean-button\">\n  <!-- ko if: question.koHasValue() && !question.isReadOnly && $data.showRemoveButton-->\n  <button type=\"button\" data-bind=\"css: showRemoveButton, enabled: !question.isInputReadOnly, click: question.doclean\">\n      <span data-bind=\"text: question.clearButtonCaption\"></span>\n  </button>\n  <!-- /ko -->\n</script>\n<script type=\"text/html\" id=\"survey-question-file-video\">\n  <div data-bind=\"css: question.cssClasses.videoContainer\">\n    <!-- ko component: { name: 'sv-action', params: { item: question.changeCameraAction } } --><!-- /ko -->\n    <!-- ko component: { name: 'sv-action', params: { item: question.closeCameraAction } } --><!-- /ko -->\n    <video autoplay playsinline data-bind=\"attr: { id: question.videoId },  css: question.cssClasses.video\"></video>\n    <!-- ko component: { name: 'sv-action', params: { item: question.takePictureAction } } --><!-- /ko -->\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-question-file-sign\">\n  <!-- ko if: item.name && fileSignCss -->\n  <div data-bind=\"css: fileSignCss\">\n    <a data-bind=\"style: { width: question.imageWidth }, click: question.dodownload, text: item.name, attr: { href: item.content, title: item.name, download: item.name }\"></a>\n  </div>\n  <!-- /ko -->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-html.html":
/*!***************************************************!*\
  !*** ./src/knockout/templates/question-html.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-html\">\n  <div data-bind=\"html: question.locHtml.koRenderedHtml, css: question.renderCssRoot\"></div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-image.html":
/*!****************************************************!*\
  !*** ./src/knockout/templates/question-image.html ***!
  \****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-image\">\n  <div data-bind=\"css: question.cssClasses.root\">\n    <!-- ko if: question.renderedMode === \"image\" -->\n    <img data-bind=\"event: { load: question.onLoadHandler, error: question.onErrorHandler }, css: question.getImageCss(), attr: { src: $data.locImageLink.koRenderedHtml() || null, width: question.renderedWidth, height: question.renderedHeight, alt: question.altText || question.title }, style: { objectFit: question.imageFit,  width: question.renderedStyleWidth, height: question.renderedStyleHeight }, visible: $data.locImageLink.koRenderedHtml() && !question.contentNotLoaded\"/>\n    <!-- /ko -->\n    <!-- ko if: question.renderedMode === \"video\" -->\n    <video controls data-bind=\"event: { load: question.onLoadHandler, error: question.onErrorHandler }, css: question.getImageCss(), attr: { src: $data.locImageLink.koRenderedHtml(), width: question.renderedWidth, height: question.renderedHeight }, style: { objectFit: question.imageFit,  width: question.renderedStyleWidth, height: question.renderedStyleHeight }, visible: $data.locImageLink.koRenderedHtml() && !question.contentNotLoaded\"></video>\n    <!-- /ko -->\n    <!-- ko if: question.renderedMode === \"youtube\" -->\n    <iframe data-bind=\" css: question.getImageCss(), attr: { src: $data.locImageLink.koRenderedHtml(), width: question.renderedWidth, height: question.renderedHeight }, style: { objectFit: question.imageFit,  width: question.renderedStyleWidth, height: question.renderedStyleHeight }\"></iframe>\n    <!-- /ko -->\n    <!-- ko if: !$data.locImageLink.koRenderedHtml() || question.contentNotLoaded  -->\n    <div data-bind=\"css: question.cssClasses.noImage\">\n      <!-- ko component: { name: 'sv-svg-icon', params: { iconName: question.cssClasses.noImageSvgIconId, size: 48 } } --><!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-imagepicker.html":
/*!**********************************************************!*\
  !*** ./src/knockout/templates/question-imagepicker.html ***!
  \**********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-imagepicker\">\n    <fieldset data-bind=\"css: question.getSelectBaseRootCss(), style: question.getContainerStyle()\">\n        <legend class=\"sv-hidden\" data-bind=\"text: question.locTitle.renderedHtml\"></legend>\n        <!-- ko ifnot: question.hasColumns -->\n        <!-- ko foreach: { data: question.visibleChoices, as: 'item', afterRender: question.koAfterRender}  -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: 'survey-imagepicker-item', data: item } } } -->\n        <!-- /ko -->\n        <!-- /ko -->\n        <!-- /ko -->\n        <!-- ko if: question.hasColumns -->\n        <!-- ko foreach: question.columns -->\n        <div data-bind=\"css: question.getColumnClass()\" role=\"presentation\">\n            <!-- ko foreach: { data: $data, as: 'item', afterRender: question.koAfterRender }  -->\n            <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: 'survey-imagepicker-item', data: item } } } -->\n            <!-- /ko -->\n            <!-- /ko -->\n        </div>\n        <!-- /ko -->\n        <!-- /ko -->\n    </fieldset>\n</script>\n<script type=\"text/html\" id=\"survey-imagepicker-item\">\n    <div data-bind=\"css: question.koGetItemClass(item)\">\n        <label data-bind=\"css: question.cssClasses.label\">\n            <input data-bind=\"attr: {type: question.inputType, name: question.questionName, value: item.value, id: question.getItemId(item), 'aria-required': question.ariaRequired, 'aria-label': item.locText.renderedHtml, 'aria-invalid': question.ariaInvalid, 'aria-errormessage': question.ariaErrormessage, readonly: question.isReadOnlyAttr}, checked: question.koValue, enable: question.getItemEnabled(item), css: question.cssClasses.itemControl\"\n            />\n            <div data-bind=\"css: question.cssClasses.itemDecorator\">\n                <div data-bind=\"css: question.cssClasses.imageContainer\">\n                  <!-- ko if: question.cssClasses.checkedItemDecorator -->\n                  <span data-bind=\"css: question.cssClasses.checkedItemDecorator\" aria-hidden=\"true\">\n                    <!-- ko if: question.cssClasses.checkedItemSvgIconId -->\n                    <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.checkedItemSvgIcon, iconName: question.cssClasses.checkedItemSvgIconId, size: 'auto' } } -->\n                    <!-- /ko -->\n                    <!-- /ko -->\n                   </span>\n                  <!-- /ko -->\n                  <!-- ko if: ($data.locImageLink.koRenderedHtml() && !$data.contentNotLoaded && question.contentMode === \"image\") -->\n                  <img data-bind=\"css: question.cssClasses.image, attr: { src: $data.locImageLink.koRenderedHtml, width: question.renderedImageWidth, height: question.renderedImageHeight, alt: item.locText.koRenderedHtml }, style: { objectFit: question.imageFit }, event: { load: question.onContentLoaded, error: $data.onErrorHandler }\"/>\n                  <!-- /ko -->\n                  <!-- ko if: ($data.locImageLink.koRenderedHtml() && !$data.contentNotLoaded && question.contentMode === \"video\") -->\n                  <video controls data-bind=\"css: question.cssClasses.image, attr: { src: $data.locImageLink.koRenderedHtml, width: question.renderedImageWidth, height: question.renderedImageHeight }, style: { objectFit: question.imageFit }, event: { loadedmetadata: question.onContentLoaded, error: $data.onErrorHandler }\"></video>\n                  <!-- /ko -->\n                  <!-- ko if: (!$data.locImageLink.koRenderedHtml() || $data.contentNotLoaded) -->\n                  <div data-bind=\"css: question.cssClasses.itemNoImage, style: { width: question.renderedImageWidth, height: question.renderedImageHeight, objectFit: question.imageFit}\">\n                    <!-- ko component: { name: 'sv-svg-icon', params: { css: question.cssClasses.itemNoImageSvgIcon, iconName: question.cssClasses.itemNoImageSvgIconId, size: 48 } } --><!-- /ko -->\n                  </div>\n                  <!-- /ko -->\n                  \n                </div>\n                <!-- ko if: question.showLabel -->\n                <span data-bind=\"css: question.cssClasses.itemText\">\n                  <!-- ko template: { name: 'survey-string', data: item.locText } -->\n                  <!-- /ko -->\n                </span>\n                <!-- /ko -->\n            </div>\n        </label>\n    </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-matrix.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/question-matrix.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-matrix\">\n  <div data-bind=\"css: question.cssClasses.tableWrapper\">\n    <fieldset>\n      <legend class=\"sv-hidden\"\n        data-bind=\"text: question.locTitle.renderedHtml\"\n      ></legend>\n      <table data-bind=\"css: question.getTableCss()\">\n        <!-- ko if: question.showHeader -->\n        <thead>\n          <tr>\n            <!-- ko if: question.hasRows -->\n            <td data-bind=\"visible: question.hasRows\"></td>\n            <!-- /ko -->\n            <!-- ko foreach: question.koVisibleColumns -->\n            <th data-bind=\"css: question.cssClasses.headerCell, style: { minWidth: question.columnMinWidth, width: question.columnMinWidth }\">\n              <!-- ko component: { name: question.getColumnHeaderWrapperComponentName($data), params: { componentData:  question.getColumnHeaderWrapperComponentData($data), templateData: { data: $data } } } -->\n                <!-- ko template: { name: 'survey-string', data: $data.locText } --><!-- /ko -->\n              <!-- /ko -->\n            </th>\n            <!-- /ko -->\n          </tr>\n        </thead>\n        <!-- /ko -->\n        <tbody>\n          <!-- ko foreach: { data: question.koVisibleRows, as: 'row' } -->\n          <tr data-bind=\"css: row.rowClasses\">\n            <td\n              data-bind=\"visible: question.hasRows, css: row.rowTextClasses, style: {  minWidth: question.rowTitleWidth, width: question.rowTitleWidth }\"\n            >\n              <!-- ko component: { name: question.getRowHeaderWrapperComponentName($data), params: { componentData:  question.getRowHeaderWrapperComponentData($data), templateData: { data: $data } } } -->\n                <!-- ko template: { name: 'survey-string', data: row.locText } -->\n                <!-- /ko -->\n              <!-- /ko -->\n            </td>\n            <!-- ko foreach: question.koVisibleColumns -->\n            <!-- ko if: question.hasCellText -->\n            <td\n              data-bind=\"css: question.getItemClass(row, $data), click: function() { row.cellClick($data); }\"\n            >\n              <!-- ko template: { name: 'survey-string', data: question.getCellDisplayLocText(row.name, $data) } -->\n              <!-- /ko -->\n            </td>\n            <!-- /ko -->\n            <!-- ko if: !question.hasCellText -->\n            <td\n              data-bind=\"attr: { 'data-responsive-title': $data.locText.renderedHtml }, css: question.cssClasses.cell\"\n            >\n            <!-- ko component: { name: \"sv-template-renderer\", params: { templateData: { name: question.cellComponent, data: { question: question, row: $parent, column: $data } } } } -->\n            <!-- /ko -->\n            </td>\n            <!-- /ko -->\n            <!-- /ko -->\n          </tr>\n          <!-- /ko -->\n        </tbody>\n      </table>\n    </fieldset>\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-text\">\n  <span data-bind=\"text:$data.renderedHtml\"></span>\n</script>\n<script type=\"text/html\" id=\"survey-matrix-cell\">\n  <label data-bind=\"css: question.getItemClass(row, column), event: { mousedown: question.koMouseDown }\" >\n    <input\n      type=\"radio\"\n      data-bind=\"css: question.cssClasses.itemValue, attr: { name: row.fullName, readonly: row.isReadOnlyAttr, 'aria-required': question.a11y_input_ariaRequired, 'aria-label': question.getCellAriaLabel(row.locText.renderedHtml, column.locText.renderedHtml), 'aria-invalid': question.a11y_input_ariaInvalid, 'aria-errormessage': question.a11y_input_ariaErrormessage, id: question.inputId + '_' + row.name + '_' + $index() }, enable: !row.isDisabledAttr, checkedValue: column.value, checked: row.value\"\n    />\n    <span data-bind=\"css: question.cssClasses.materialDecorator\">\n        <!-- ko if: question.itemSvgIcon -->\n          <svg data-bind=\"css:question.cssClasses.itemDecorator\">\n            <use data-bind=\"attr:{'xlink:href':question.itemSvgIcon}\" xlink:href=''></use>\n          </svg>  \n        <!-- /ko -->\n    </span>\n    <!-- ko if: question.isMobile -->\n    <span data-bind=\"css: question.cssClasses.cellResponsiveTitle\">\n      <!-- ko template: { name: 'survey-string', data: column.locText } --><!-- /ko -->\n    </span>\n    <!-- /ko -->\n  </label>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-matrixdropdown.html":
/*!*************************************************************!*\
  !*** ./src/knockout/templates/question-matrixdropdown.html ***!
  \*************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-matrixdropdown\">\n  <!-- ko template: { name: 'survey-matrixtable' } --><!--/ko-->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-matrixdynamic.html":
/*!************************************************************!*\
  !*** ./src/knockout/templates/question-matrixdynamic.html ***!
  \************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-matrixdynamic\">\n    <div>\n      <!-- ko if: question.koTable().showAddRowOnTop -->\n      <div\n        data-bind=\"css: question.cssClasses.footer\"\n      >\n        <button\n          type=\"button\"\n          data-bind=\"click: question.isDesignMode ? undefined : question.koAddRowClick, css: question.getAddRowButtonCss(), disable: question.isInputReadOnly\"\n        >\n          <!-- ko template: { name: 'survey-string', data: question.locAddRowText } --><!-- /ko -->\n          <span data-bind=\"css: question.cssClasses.iconAdd\"></span>\n        </button>\n      </div>\n      <!-- /ko -->\n      <!-- ko template: { name: 'survey-matrixtable' } -->\n      <!--/ko-->\n      <!-- ko ifnot: question.koTable().showTable -->\n      <div data-bind=\"css: question.cssClasses.emptyRowsSection\">\n        <div data-bind=\"css: question.cssClasses.emptyRowsText\">\n          <!-- ko template: { name: 'survey-string', data: question.locEmptyRowsText } --><!-- /ko -->\n        </div>\n        <!-- ko if: question.koTable().showAddRow -->  \n        <button\n          type=\"button\"\n          data-bind=\"click:question.koAddRowClick, css: question.getAddRowButtonCss(true), disable: question.isInputReadOnly\"\n        >\n          <!-- ko template: { name: 'survey-string', data: question.locAddRowText } --><!-- /ko -->\n          <span data-bind=\"css: question.cssClasses.iconAdd\"></span>\n        </button>\n        <!-- /ko -->\n      </div>\n      <!-- /ko -->\n      <!-- ko if: question.koTable().showAddRowOnBottom -->\n      <div\n        data-bind=\"css: question.cssClasses.footer\"\n      >\n        <button\n          type=\"button\"\n          data-bind=\"click: question.koAddRowClick, css: question.getAddRowButtonCss(), disable: question.isInputReadOnly\"\n        >\n          <!-- ko template: { name: 'survey-string', data: question.locAddRowText } --><!-- /ko -->\n          <span data-bind=\"css: question.cssClasses.iconAdd\"></span>\n        </button>\n      </div>\n      <!-- /ko -->\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-matrixdropdown-cell\">\n  <!-- ko if: $data.isVisible -->\n  <td\n    data-bind=\"css: $data.className, style: { minWidth: $data.minWidth, width: $data.width }, attr: { title: $data.getTitle(), colspan: $data.colSpans }, event: {focusin: $data.focusIn }\"\n  >\n    <!-- ko if: $data.showResponsiveTitle -->\n    <span data-bind=\"css: $data.responsiveTitleCss\">\n        <!-- ko template: { name: 'survey-string', data: $data.responsiveLocTitle } --><!-- /ko -->\n        <!-- ko if: $data.column && $data.column.isRenderedRequired -->\n        <span>&nbsp</span>\n        <span data-bind=\"css: $data.matrix.cssClasses.cellRequiredText, text: $data.column.requiredText\"></span>\n        <!-- /ko -->\n    </span>\n    <!-- /ko -->\n    <!-- ko if: $data.matrix -->\n    <div data-bind=\"visible: question.isVisible, css: cellQuestionWrapperClassName\">\n      <!-- ko if: $data.isOtherChoice -->\n        <div data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': true } }\"></div>\n      <!-- /ko -->\n      <!-- ko if: $data.isCheckbox -->\n        <!-- ko let: { question: $data.matrix.getCellTemplateData($data) } -->\n          <!-- ko component: { name: $data.matrix.getCellWrapperComponentName($data), params: { componentData:  $data.matrix.getCellWrapperComponentData($data), templateData: { name:  'survey-checkbox-item', data: item } } } -->\n          <!-- /ko -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: $data.isRadio -->\n        <!-- ko let: { question: $data.matrix.getCellTemplateData($data) } -->\n          <!-- ko component: { name: $data.matrix.getCellWrapperComponentName($data), params: { componentData:  $data.matrix.getCellWrapperComponentData($data), templateData: { name:  'survey-radiogroup-item', data: item } } } -->\n          <!-- /ko -->  \n        <!-- /ko -->   \n      <!-- /ko -->\n      <!-- ko ifnot: $data.isChoice -->\n      <!-- ko if: question.isDefaultRendering() -->\n        <!-- ko let: { question: $data.matrix.getCellTemplateData($data) } -->\n        <!-- ko component: { name: $data.matrix.getCellWrapperComponentName($data), params: { componentData:  $data.matrix.getCellWrapperComponentData($data), templateData: { name: question.koTemplateName(), data: question, afterRender: function(el) { $data.matrix.koCellQuestionAfterRender(el, $data); } } } } -->\n        <!-- /ko -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko ifnot: question.isDefaultRendering() -->\n        <!-- ko component: { name: question.getComponentName(), params: { question: question } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko ifnot: $data.matrix -->\n    <!-- ko if: $data.locTitle -->\n    <!-- ko template: { name: 'survey-string', data: $data.locTitle } --><!-- /ko -->\n    <!-- /ko -->\n    <!-- /ko -->\n  </td>\n  <!-- /ko -->\n</script>\n<script type=\"text/html\" id=\"survey-matrixtable\">\n<div\n  data-bind=\"visible: question.koTable().showTable, css: question.cssClasses.tableWrapper, style: { overflowX: question.showHorizontalScroll ? 'scroll': '' }\"\n>\n  <table data-bind=\"css: question.getTableCss()\">\n    <!-- ko if: question.koTable().showHeader -->\n    <thead>\n      <tr>\n        <!-- ko foreach: question.koTable().headerRow.cells -->\n          <!-- ko if: $data.hasTitle -->\n            <th\n              data-bind=\"style: { minWidth: $data.minWidth, width: $data.width }, css: $data.className\"\n            >\n              <!-- ko component: { name: question.getColumnHeaderWrapperComponentName($data), params: { componentData:  question.getColumnHeaderWrapperComponentData($data), templateData: { data: $data } } } -->\n                <!-- ko template: { name: 'survey-string', data: $data.locTitle } --><!-- /ko -->\n                <!-- ko if: $data.column && $data.column.isRenderedRequired -->\n                <span>&nbsp</span>\n                <span data-bind=\"css: question.cssClasses.cellRequiredText, text: $data.column.requiredText\"></span>\n                <!-- /ko -->\n              <!-- /ko -->\n            </th>\n          <!-- /ko -->\n          <!-- ko ifnot: $data.hasTitle -->\n            <td data-bind=\"style: { minWidth: $data.minWidth, width: $data.width }, css: $data.className\"></td>\n          <!-- /ko -->\n        <!-- /ko -->\n      </tr>\n    </thead>\n    <!-- /ko -->\n    <tbody>\n      <!-- ko foreach: { data: question.koTable().renderedRows, afterRender: question.koRowAfterRender } -->\n      <!-- ko ifnot: ($parent.detailPanelMode === \"popup\" && $data.isDetailRow) || !$data.visible-->\n      <tr data-bind=\"css: $data.className, attr: attributes, event: { pointerdown: function (model, event) { question.onPointerDown(event, row); return true;} }\">\n        <!-- ko foreach: $data.cells -->\n        <!-- ko if: $data.isDragHandlerCell -->\n        <td data-bind=\"css:$data.className, attr: {colspan: $data.colSpans}\">\n          <!-- ko component: { name: 'sv-matrix-drag-drop-icon', params: { item: { data: { row: row, question: question } } }} -->\n          <!-- /ko -->\n        </td>\n        <!-- /ko -->\n        <!-- ko if: $data.isActionsCell -->\n        <td data-bind=\"css: $data.className, attr: { colspan: $data.colSpans, title: $data.getTitle() }\">\n          <!-- ko component: { name: 'sv-action-bar', params: { model: $data.item.getData(), handleClick: false } } -->\n          <!-- /ko -->\n        </td>\n        <!-- /ko -->\n        <!-- ko if: $data.isEmpty -->\n        <td data-bind=\"css: $data.className, attr: { colspan: $data.colSpans, title: $data.getTitle() }\"></td>\n        <!-- /ko -->\n        <!-- ko if: $data.hasPanel -->\n        <td data-bind=\"css: $data.className, attr: { colspan: $data.colSpans }\">\n          <!-- ko component: { name: $data.panel.survey.getElementWrapperComponentName($data.panel), \n            params: { componentData:  $data.panel.survey.getElementWrapperComponentData($data.panel), \n            templateData: { name: $data.panel.koElementType, data: $data.panel, afterRender: question.koPanelAfterRender } } } \n          -->\n          <!-- /ko -->\n        </td>\n        <!-- /ko -->\n        <!-- ko if: $data.isErrorsCell && $data.isVisible -->\n        <td data-bind=\"css: $data.className, attr: { colspan: $data.colSpans, title: $data.getTitle() }\">\n            <!-- ko template: { name: 'survey-question-errors', data: $data.question, as: 'question' } -->\n            <!-- /ko -->\n        </td>\n        <!-- /ko -->\n        <!-- ko if: $data.hasQuestion -->\n        <!-- ko template: { name: 'survey-matrixdropdown-cell', afterRender: function(els) { $data.matrix.koCellAfterRender(els, $data); } } --><!-- /ko -->\n        <!-- /ko -->\n        <!-- ko if: $data.hasTitle -->\n        <td\n          data-bind=\"css: $data.className, style: { minWidth: $data.minWidth, width: $data.width }, attr: { colspan: $data.colSpans, title: $data.getTitle() }\"\n        >\n          <!-- ko component: { name: question.getRowHeaderWrapperComponentName($data), params: { componentData:  question.getRowHeaderWrapperComponentData($data), templateData: { data: $data } } } -->\n          <!-- ko template: { name: 'survey-string', data: $data.locTitle } --><!-- /ko -->\n          <!-- ko if: $data.requiredText -->\n          <span data-bind=\"css: question.cssClasses.cellRequiredText, text: $data.requiredText\"></span>\n          <!-- /ko -->\n          <!-- /ko -->\n        </td>\n        <!-- /ko -->\n        <!-- /ko -->\n      </tr>\n\n      <!-- /ko -->\n      <!-- /ko -->\n    </tbody>\n    <!-- ko if:question.koTable().hasFooter -->\n    <tfoot>\n      <tr>\n        <!-- ko foreach: question.koTable().footerRow.cells -->\n            <!-- ko template: { name: 'survey-matrixdropdown-cell', afterRender: function(els) { $data.matrix && $data.matrix.koCellAfterRender(els, $data); } } --><!-- /ko -->\n        <!-- /ko -->\n      </tr>\n    </tfoot>\n    <!-- /ko -->\n  </table>\n</div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-multipletext.html":
/*!***********************************************************!*\
  !*** ./src/knockout/templates/question-multipletext.html ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-multipletext\">\n  <table data-bind=\"css: question.getQuestionRootCss()\">\n    <tbody data-bind=\"foreach: { data:  question.getRows(), as: 'row' }\">\n      <!-- ko if: row.isVisible -->\n      <tr data-bind=\"foreach: { data: row.cells, as: 'cell' }, css: question.cssClasses.row\">\n        <td data-bind=\"css: cell.className\">  \n          <!-- ko ifnot: cell.isErrorsCell -->\n          <label data-bind=\"css: question.getItemLabelCss(item)\">\n              <span data-bind=\"css: question.koItemTitleCss, style: {  minWidth: question.itemTitleWidth, width: question.itemTitleWidth }\">\n                <!-- ko component: { name: 'survey-element-title-content', params: {element: cell.item.editor} } --><!-- /ko -->\n              </span>\n              <div data-bind=\"css: question.koItemCss, event: {focusin: cell.item.focusIn }\">\n                <!-- ko template: { name: item.editor.koTemplateName(), data: cell.item.editor, as: 'question', afterRender: cell.item.editor.koQuestionAfterRender } -->\n                <!-- /ko -->\n              </div>\n          </label>\n          <!-- /ko -->\n          <!-- ko if: cell.isErrorsCell -->\n            <!-- ko template: { name: 'survey-question-errors', data: cell.item.editor, as: 'question' } -->\n            <!-- /ko -->\n          <!-- /ko -->\n        </td>\n      </tr>\n      <!-- /ko -->\n    </tbody>\n  </table>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-paneldynamic-navigator.html":
/*!*********************************************************************!*\
  !*** ./src/knockout/templates/question-paneldynamic-navigator.html ***!
  \*********************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-paneldynamic-navigator\">\n  <div style=\"clear: both;\">\n        <div data-bind=\"css: question.cssClasses.progressContainer\">\n          <!-- ko component: { name: 'sv-paneldynamic-prev-btn', params: { question: question }} --><!-- /ko -->\n          <!-- ko if: question.koIsRange -->\n            <!-- ko template: { name: 'survey-question-paneldynamic-progress', data: question, as: 'question'} --><!-- /ko -->\n          <!-- /ko -->\n          <!-- ko component: { name: 'sv-paneldynamic-next-btn', params: { question: question }} --><!-- /ko -->\n        </div>\n          <!-- ko component: { name: 'sv-paneldynamic-add-btn', params: { question: question }} --><!-- /ko -->\n        <div data-bind=\"text: question.koProgressText, css: question.cssClasses.progressText\"></div>\n      </div>\n</script>\n<script type=\"text/html\" id=\"survey-question-paneldynamic-progress\">\n  <div data-bind=\"css: question.cssClasses.progress\">\n    <div\n      data-bind=\"css: question.cssClasses.progressBar, style: { width: question.koProgress }\"\n      role=\"progressbar\"\n    ></div>\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-paneldynamic.html":
/*!***********************************************************!*\
  !*** ./src/knockout/templates/question-paneldynamic.html ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-paneldynamic\">\n  <div data-bind=\"css: question.cssClasses.root\">\n    <!-- ko if: question.hasTabbedMenu -->\n    <div data-bind=\"css: question.getTabsContainerCss()\">\n        <!-- ko component: { name: \"sv-action-bar\", params: { model: question.tabbedMenu } } -->\n        <!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko if: question.getShowNoEntriesPlaceholder() -->\n      <div data-bind=\"css: question.cssClasses.noEntriesPlaceholder\">\n        <span>\n          <!-- ko template: { name: 'survey-string', data: locNoEntriesText } --><!-- /ko -->\n        </span>\n          <!-- ko component: { name: 'sv-paneldynamic-add-btn', params: { question: question }} -->\n          <!-- /ko -->\n        </div>\n    <!-- /ko -->\n    <!-- ko if: question.koIsList() -->\n    <div data-bind=\"css: question.cssClasses.panelsContainer\">\n      <!-- ko foreach: { data: question.renderedPanels } -->\n        <div data-bind=\"css: question.getPanelWrapperCss($data)\">\n          <!-- ko let: { question: $data } -->\n            <!-- ko component: { name: survey.getElementWrapperComponentName(question), params: { componentData:  survey.getElementWrapperComponentData(question), templateData: { name: question.koElementType, data: question, afterRender: $parent.koPanelAfterRender } } } -->\n            <!-- /ko -->\n          <!-- /ko -->\n          <!-- ko if: question.panelRemoveButtonLocation === 'right' && question.koCanRemovePanel() && $data.state != 'collapsed'-->\n            <!-- ko component: { name: 'sv-paneldynamic-remove-btn', params: { question: question, panel: $data } } -->\n            <!-- /ko -->\n          <!-- /ko -->\n          \n        </div>\n        <!-- ko if: question.showSeparator($index()) -->\n        <hr data-bind=\"css: question.cssClasses.separator\"/>\n        <!-- /ko -->\n      <!-- /ko -->\n      </div>\n      <!-- ko if: question.showLegacyNavigation -->\n        <!-- ko component: { name: 'sv-paneldynamic-add-btn', params: { question: question }} --><!-- /ko -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko ifnot: question.koIsList()  -->\n      <!-- ko if: question.koIsProgressTop-->\n        <!-- ko if: !question.showLegacyNavigation && question.koIsRange -->\n          <!-- ko template: { name: 'survey-question-paneldynamic-progress', data: question, as: 'question'} -->\n          <!-- /ko -->\n        <!-- /ko -->\n        <!-- ko if: question.showLegacyNavigation -->\n        <div data-bind=\"css: question.cssClasses.progressTop\">\n          <!-- ko template: { name: 'survey-question-paneldynamic-navigator', data: question, as: 'question'} -->\n          <!-- /ko -->\n        </div>\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.koPanel() -->\n      <div data-bind=\"css: question.cssClasses.panelsContainer\">\n        <!-- ko foreach: { data: question.renderedPanels } -->\n          <div data-bind=\"css: question.getPanelWrapperCss($data)\">\n          <!-- ko let: { question: $data } -->\n            <!-- ko component: { name: question.survey.getElementWrapperComponentName(question), params: { componentData:  question.survey.getElementWrapperComponentData(question), templateData: { name: question.koElementType, data: question, afterRender: $parent.koPanelAfterRender } } } -->\n            <!-- /ko -->\n          <!-- /ko -->\n          <!-- ko if: question.panelRemoveButtonLocation === 'right'-->\n            <!-- ko template: { name: 'survey-question-paneldynamic-remove-btn', data: { question: question, panel: question.koPanel() }, as: 'question'} -->\n            <!-- /ko -->\n          <!-- /ko-->\n          </div>\n         <!-- /ko -->\n      </div>\n      <!-- /ko -->\n      <!-- ko if: question.showLegacyNavigation && question.koIsProgressBottom--> \n      <div data-bind=\"css: question.cssClasses.progressBottom\">\n        <!-- ko template: { name: 'survey-question-paneldynamic-navigator', data: question, as: 'question'} -->\n        <!-- /ko -->\n      </div>\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: question.showNavigation -->\n    <div data-bind=\"css: question.cssClasses.footer\">\n      <hr data-bind=\"css: question.cssClasses.separator\"/>\n      <!-- ko if: question.koIsRange() && question.koIsProgressBottom -->\n         <!-- ko template: { name: 'survey-question-paneldynamic-progress', data: question, as: 'question'} -->\n         <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.footerToolbar.visibleActions.length -->\n      <div data-bind=\"css: question.cssClasses.footerButtonsContainer\">\n        <!-- ko component: { name: \"sv-action-bar\", params: { model: question.footerToolbar } } -->\n        <!-- /ko -->\n      </div>\n      <!-- /ko -->\n    </div>\n    <!-- /ko -->\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-radiogroup.html":
/*!*********************************************************!*\
  !*** ./src/knockout/templates/question-radiogroup.html ***!
  \*********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-radiogroup\">\n\n  <fieldset data-bind=\"css: question.getSelectBaseRootCss(), attr: { 'role': question.a11y_input_ariaRole, 'aria-required': question.a11y_input_ariaRequired, 'aria-labelledby': question.a11y_input_ariaLabelledBy, 'aria-describedby': question.a11y_input_ariaDescribedBy, 'aria-invalid': question.a11y_input_ariaInvalid, 'aria-errormessage': question.a11y_input_ariaErrormessage, 'aria-label': question.a11y_input_ariaLabel }\">\n    <!-- ko ifnot: question.hasColumns -->\n      <!-- ko if: question.blockedRow -->\n      <div data-bind=\"css: question.cssClasses.rootRow\">\n        <!-- ko foreach: { data: question.dataChoices, as: 'item', afterRender: question.koAfterRender }  -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n        <!-- /ko -->\n        <!-- /ko -->\n      </div>\n      <!-- /ko -->\n      <!-- ko ifnot: question.blockedRow -->\n      <!-- ko foreach: { data: question.bodyItems, as: 'item', afterRender: question.koAfterRender }  -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- /ko -->\n    <!-- /ko -->\n    <!-- ko if: question.hasColumns -->\n      <div data-bind=\"css: question.cssClasses.rootMultiColumn\">\n\n        <!-- ko foreach: question.columns -->\n        <div data-bind=\"css: question.getColumnClass()\" role=\"presentation\">\n          <!-- ko foreach: { data: $data, as: 'item', afterRender: question.koAfterRender } -->\n            <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n            <!-- /ko -->\n          <!-- /ko -->\n        </div>\n        <!-- /ko -->\n      </div>\n    <!-- /ko -->\n    <!-- ko if: question.hasFootItems  -->\n      <!-- ko foreach: { data: question.footItems, as: 'item', afterRender: question.koAfterRender }  -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: question.itemComponent, data: item } } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n    <!-- /ko -->\n\n    <!-- ko if: question.hasOther && question.isOtherSelected -->\n      <div data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': question.isOtherSelected } }\"></div>\n    <!-- /ko -->\n    <!-- ko if: question.showClearButtonInContent -->\n    <div>\n      <input\n        type=\"button\"\n        data-bind=\"click:question.clearValueOnly, css: question.cssClasses.clearButton, value: question.clearButtonCaption\"\n      />\n    </div>\n    <!-- /ko -->\n  </fieldset>\n</script>\n<script type=\"text/html\" id=\"survey-radiogroup-item\">\n  <div role=\"presentation\" data-bind=\"css: question.getItemClass($data)\">\n    <label data-bind=\"css: question.getLabelClass($data), event: { mousedown: question.koMouseDown }\">\n      <input\n        type=\"radio\"\n        data-bind=\"attr: { name: question.questionName, id: question.getItemId($data), 'aria-errormessage': question.ariaErrormessage, readonly: question.isReadOnlyAttr}, checkedValue: $data.value, checked: question.renderedValue, enable: question.getItemEnabled($data), css: question.cssClasses.itemControl\"\n      />\n      <!-- ko if: question.cssClasses.materialDecorator -->\n      <span data-bind=\"css: question.cssClasses.materialDecorator\">\n        <!-- ko if: question.itemSvgIcon -->\n        <svg data-bind=\"css:question.cssClasses.itemDecorator\">\n          <use data-bind=\"attr:{'xlink:href':question.itemSvgIcon}\" xlink:href=''></use>\n        </svg>\n        <!-- /ko -->\n      </span>\n      <!-- /ko -->\n      <!-- ko if: !$data.hideCaption -->\n      <span data-bind=\"css: question.getControlLabelClass($data)\">\n        <!-- ko template: { name: 'survey-string', data: $data.locText } -->\n        <!-- /ko -->\n      </span>\n      <!-- /ko -->\n    </label>\n  </div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-ranking.html":
/*!******************************************************!*\
  !*** ./src/knockout/templates/question-ranking.html ***!
  \******************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-ranking\">\n   <!-- ko ifnot: question.selectToRankEnabled -->\n  <div data-bind=\"css: question.rootClass\">\n    <!-- ko foreach: { data: question.renderedRankingChoices, as: 'item', afterRender: question.koAfterRender } -->\n      <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { number: question.getNumberByIndex($index()), componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: 'survey-ranking-item', data: item } } } -->\n      <!-- /ko -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n\n  <!-- ko if: question.selectToRankEnabled -->\n  <div data-bind=\"css: question.rootClass\">\n    <div data-bind=\"css: question.getContainerClasses('from')\" data-ranking=\"from-container\">\n      <!-- ko foreach: { data: question.renderedUnRankingChoices, as: 'item', afterRender: question.koAfterRender } -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { number: '', componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: 'survey-ranking-item', data: item } } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.renderedUnRankingChoices.length === 0 -->\n        <div data-bind=\"css: cssClasses.containerPlaceholder\">\n            <!-- ko template: { name: 'survey-string', data: question.locSelectToRankEmptyRankedAreaText } -->\n            <!-- /ko -->\n        </div>\n      <!-- /ko -->\n    </div>\n    <div data-bind=\"css: cssClasses.containersDivider\"></div>\n    <div data-bind=\"css: question.getContainerClasses('to')\" data-ranking=\"to-container\">\n      <!-- ko foreach: { data: question.renderedRankingChoices, as: 'item', afterRender: question.koAfterRender } -->\n        <!-- ko component: { name: question.getItemValueWrapperComponentName(item), params: { number: question.getNumberByIndex($index()), componentData:  question.getItemValueWrapperComponentData(item), templateData: { name: 'survey-ranking-item', data: item } } } -->\n        <!-- /ko -->\n      <!-- /ko -->\n      <!-- ko if: question.renderedRankingChoices.length === 0 -->\n      <div data-bind=\"css: cssClasses.containerPlaceholder\">\n          <!-- ko template: { name: 'survey-string', data: question.locSelectToRankEmptyUnrankedAreaText } -->\n          <!-- /ko -->\n      </div>\n      <!-- /ko -->\n    </div>\n  </div>\n\n  <!-- /ko -->\n</script>\n\n<script type=\"text/html\" id=\"survey-ranking-item\">\n  <div\n    data-bind=\"event: { keydown: question.koHandleKeydown, pointerdown: question.koHandlePointerDown, pointerup: question.koHandlePointerUp}, css: question.getItemClass($data), attr: {id: question.getItemId($data), tabindex: question.getItemTabIndex($data), 'data-sv-drop-target-ranking-item': $index() }\"\n  >\n    <div tabindex=\"-1\" style=\"outline: none;\">\n      <div data-bind=\"css: question.cssClasses.itemGhostNode\"></div>\n      <div data-bind=\"css: question.cssClasses.itemContent\">\n        <div data-bind=\"css: question.cssClasses.itemIconContainer\">\n          <svg data-bind=\"css:question.getIconHoverCss()\">\n            <use data-bind=\"attr:{'xlink:href':question.dragDropSvgIcon}\" xlink:href=''></use>\n          </svg>\n          <svg data-bind=\"css:question.getIconFocusCss()\">\n            <use data-bind=\"attr:{'xlink:href':question.arrowsSvgIcon}\" xlink:href=''></use>\n          </svg>\n        </div>\n        <!-- ko if: $parent.number -->\n        <div\n          data-bind=\"css: question.getItemIndexClasses(item), text: $parent.number\"\n        ></div>\n        <!-- /ko -->\n        <!-- ko ifnot: $parent.number -->\n        <div\n          data-bind=\"css: question.getItemIndexClasses(item)\"\n        >\n        <svg>\n          <use data-bind=\"attr:{'xlink:href':question.dashSvgIcon}\" xlink:href=''></use>\n        </svg>\n        </div>\n        <!-- /ko -->\n\n        <!-- ko component: { name: question.itemComponent, params: { cssClasses: question.cssClasses, item: $data } } -->\n        <!-- /ko -->\n      </div>\n    </div>\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-rating.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/question-rating.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-rating\">\n    <div data-bind=\"css: question.ratingRootCss\">\n        <fieldset role=\"radiogroup\">\n            <legend role=\"presentation\" class=\"sv-hidden\"></legend>\n            <!-- ko if: question.hasMinLabel-->\n            <span data-bind=\"css: question.cssClasses.minText\">\n              <!-- ko template: { name: 'survey-string', data: question.locMinRateDescription } -->\n              <!-- /ko -->\n              </span>\n            <!-- /ko -->\n            <!-- ko foreach: question.renderedRateItems -->\n              <!-- ko component: { name: question.itemComponent, params: { question: question, item: $data, index: $index() } } -->\n              <!-- /ko -->\n              \n            <!-- /ko -->\n            <!-- ko if: question.hasMaxLabel-->\n            <span data-bind=\"css: question.cssClasses.maxText\">\n              <!-- ko template: { name: 'survey-string', data: question.locMaxRateDescription } -->\n              <!-- /ko -->\n              </span>\n            <!-- /ko -->\n\n        </fieldset>\n    </div>\n  </fieldset>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/question-signaturepad.html":
/*!***********************************************************!*\
  !*** ./src/knockout/templates/question-signaturepad.html ***!
  \***********************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-signaturepad\">\n    <div data-bind=\"css: question.cssClasses.root, style: { width: question.renderedCanvasWidth }\">\n        <div data-bind=\"css: question.cssClasses.placeholder, visible: $data.needShowPlaceholder()\">\n            <!-- ko template: { name: 'survey-string', data: question.locRenderedPlaceholder } -->\n            <!-- /ko -->\n        </div>\n        <div>\n            <!-- ko if: question.backgroundImage -->\n            <img data-bind=\"attr: { src: question.backgroundImage}, style: { width: question.renderedCanvasWidth }, css: question.cssClasses.backgroundImage\">\n            <!-- /ko -->\n            <canvas tabindex='-1' data-bind=\"css: question.cssClasses.canvas, event: { blur: question.koOnBlur }\" ></canvas>\n        </div>\n        <!-- ko if: question.canShowClearButton -->\n        <div data-bind=\"css: question.cssClasses.controls\">\n            <button type='button'\n                data-bind=\"click: question.clearValueOnly, css: question.cssClasses.clearButton, attr: { title: question.clearButtonCaption }\">\n                    <!-- ko ifnot: question.cssClasses.clearButtonIconId -->\n                        <span>✖</span>\n                    <!-- /ko -->\n                    <!-- ko if: question.cssClasses.clearButtonIconId -->\n                        <sv-svg-icon params=\"iconName: question.cssClasses.clearButtonIconId, size: 'auto'\"></sv-svg-icon>\n                    <!-- /ko -->\n            </button>\n        </div>\n        <!-- /ko -->\n        <!-- ko if: question.showLoadingIndicator -->\n        <div data-bind=\"css: question.cssClasses.loadingIndicator\">\n        <!-- ko component: { name: \"sv-loading-indicator\" } -->\n        <!-- /ko -->\n        </div>\n        <!-- /ko -->\n    </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-tagbox.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/question-tagbox.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-tagbox\">\n  <div data-bind=\"css: question.renderCssRoot\">\n    <!-- ko component: { name: 'sv-tagbox', params: { question: question } } -->\n    <!-- /ko -->\n  <!-- ko if: question.isOtherSelected -->\n  <div\n    data-bind=\"css: question.getCommentAreaCss(true), template: { name: 'survey-other', data: {'question': question, 'visible': question.isOtherSelected } }, style: {display: question.isFlowLayout ? 'inline': ''}\">\n  </div>\n  <!-- /ko -->\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question-text.html":
/*!***************************************************!*\
  !*** ./src/knockout/templates/question-text.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-text\">\n  <!--ko if: !question.dataListId && !question.isReadOnlyRenderDiv()-->\n    <!-- ko template: { name: 'survey-question-text-input' } --><!-- /ko -->\n  <!--/ko-->\n  <!--ko if: question.dataListId && !question.isReadOnlyRenderDiv()-->\n  <div>\n    <!-- ko template: { name: 'survey-question-text-input' } --><!-- /ko -->\n    <datalist data-bind=\"attr: {id: question.dataListId}\">\n    <!-- ko foreach: question.dataList -->\n      <option data-bind=\"value:$data\"></option>\n    <!--/ko-->\n    </datalist>\n  </div>\n  <!--/ko-->\n  <!--ko if: question.isReadOnlyRenderDiv() -->\n  <div data-bind=\"text: question.koReadOnlyValue\"></div>\n  <!--/ko-->\n</script>\n<script type=\"text/html\" id=\"survey-question-text-input\">\n  <input\n  data-bind=\"disable: question.isDisabledAttr, \n    style: question.inputStyle, \n    attr: { type: question.inputType, size: question.renderedInputSize, id: question.inputId, placeholder: question.renderedPlaceholder, maxLength: question.getMaxLength(), min: question.renderedMin, max: question.renderedMax, step: question.renderedStep, 'aria-required': question.a11y_input_ariaRequired, 'aria-invalid': question.ariaInvalid, 'aria-label': question.a11y_input_ariaLabel, 'aria-labelledby': question.a11y_input_ariaLabelledBy, 'aria-describedby': question.a11y_input_ariaDescribedBy, 'aria-invalid': question.a11y_input_ariaInvalid, 'aria-errormessage': question.a11y_input_ariaErrormessage, autocomplete: question.autocomplete, list:question.dataListId, readonly:question.isReadOnlyAttr }, \n    event: { keydown: koOnKeyDown, keyup: koOnKeyUp, change: koOnChange, compositionupdate: koOnCompositeUpdate, blur: koOnBlur, focus: koOnFocus },\n    value: question.koReadOnlyValue,\n    css: question.getControlClass()\"/>\n  <!--ko if: question.getMaxLength() -->\n  <!-- ko component: { name: 'sv-character-counter', params: { counter: question.characterCounter, remainingCharacterCounter: question.cssClasses.remainingCharacterCounter } } -->\n  <!-- /ko -->\n  <!--/ko-->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/question.html":
/*!**********************************************!*\
  !*** ./src/knockout/templates/question.html ***!
  \**********************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question\">\n<div data-bind=\"css: question.getRootCss(), style: question.getRootStyle(), attr: { id: question.id, 'data-name': question.name, role: question.ariaRole, 'aria-required': question.ariaRequired, 'aria-invalid': question.ariaInvalid, 'aria-labelledby': question.ariaLabelledBy, 'aria-describedby':question.ariaDescribedBy, 'aria-expanded': question.ariaExpanded}\">\n  <!-- ko if: question.showErrorsAboveQuestion -->\n    <!-- ko template: { name: 'survey-question-errors', data: question } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.hasTitleOnLeftTop -->\n    <!--ko template: { name: 'survey-question-title', data: question  } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko component: { name: question.survey.getQuestionContentWrapperComponentName(question), params: { componentData:  question.survey.getElementWrapperComponentData(question), templateData: { name: 'survey-question-content', data: question } } } -->\n  <!-- /ko -->\n  <!-- ko if: question.hasTitleOnBottom -->\n    <!--ko template: { name: 'survey-question-title', data: question  } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.showErrorsBelowQuestion -->\n    <!-- ko template: { name: 'survey-question-errors', data: question } -->\n    <!-- /ko -->\n  <!-- /ko -->\n</div>\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/questioncontent.html":
/*!*****************************************************!*\
  !*** ./src/knockout/templates/questioncontent.html ***!
  \*****************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-content\">\n<div data-bind=\"visible: question.renderedIsExpanded, css: question.cssContent, event: {focusin: question.focusIn }\" role=\"presentation\">\n  <!-- ko if: question.showErrorOnTop -->\n    <!-- ko template: { name: 'survey-question-errors', data: question } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.isDefaultRendering() -->\n    <!-- ko template: { name: question.koTemplateName(), data: question, afterRender: question.koQuestionAfterRender } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko ifnot: question.isDefaultRendering() -->\n    <!-- ko component: { name: getComponentName(), params: { question: question } } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.hasComment -->\n  <div data-bind=\"css: question.getCommentAreaCss()\">\n    <div>\n      <!-- ko template: { name: 'survey-string', data: question.locCommentText } -->\n      <!-- /ko -->\n    </div>\n    <!-- ko template: { name: 'survey-comment',  data: {'question': question, 'visible': true } } -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n  <!-- ko if: question.showErrorOnBottom -->\n    <!-- ko template: { name: 'survey-question-errors', data: question } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: question.hasDescriptionUnderInput -->\n  <div data-bind=\"css: question.cssDescription, attr: {'id': question.ariaDescriptionId}\">\n    <!-- ko template: { name: 'survey-string', data: locDescription } -->\n    <!-- /ko -->\n  </div>\n  <!-- /ko -->\n</div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/questiontitle.html":
/*!***************************************************!*\
  !*** ./src/knockout/templates/questiontitle.html ***!
  \***************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-question-title\">\n  <div data-bind=\"css: question.cssHeader, style: { width: $data.titleWidth }, click: function(m, e) { if(question.clickTitleFunction) return question.clickTitleFunction(e); }\">\n    <!-- ko component: { name: 'survey-element-title', params: { element: $data } } --><!-- /ko -->\n    <!-- ko if: $data.hasDescriptionUnderTitle -->\n    <div data-bind=\"css: $data.cssDescription, visible: $data.hasDescription, attr: {'id': $data.ariaDescriptionId}\">\n      <!-- ko template: { name: 'survey-string', data: $data.locDescription } --><!-- /ko -->\n    </div>\n    <!-- /ko -->\n    <!-- ko if: $data.hasAdditionalTitleToolbar -->\n    <!-- ko component: { name: 'sv-action-bar', params: { model: $data.additionalTitleToolbar } } --><!-- /ko -->\n    <!-- /ko -->\n  </div>\n</script>";

/***/ }),

/***/ "./src/knockout/templates/row.html":
/*!*****************************************!*\
  !*** ./src/knockout/templates/row.html ***!
  \*****************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-row\">\n  <div data-bind=\"css: row.getRowCss()\">\n    <!-- ko template: { name: \"survey-row-content\", afterRender: row.rowAfterRender } -->\n    <!-- /ko -->\n  </div>\n</script>\n<script type=\"text/html\" id=\"survey-row-content\">\n<!-- ko foreach: { data: row.visibleElements, as: 'question', afterRender: row.koAfterRender } -->\n  <div data-bind=\"css: question.cssClasses.questionWrapper, style: $data.rootStyle\">\n  <!-- ko if: row.isNeedRender -->\n    <!-- ko component: { name: row.panel.survey.getElementWrapperComponentName(question), params: { componentData:  row.panel.survey.getElementWrapperComponentData(question), templateData: { name: question.koElementType, data: question, afterRender: $parent.koElementAfterRender } } } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  <!-- ko if: !row.isNeedRender && question.skeletonComponentName -->\n    <!-- ko component: { name: question.skeletonComponentName, params: { element: question } } -->\n    <!-- /ko -->\n  <!-- /ko -->\n  </div>\n<!-- /ko -->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/rows.html":
/*!******************************************!*\
  !*** ./src/knockout/templates/rows.html ***!
  \******************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-rows\">\n  <!-- ko foreach: { data: visibleRows, as: 'row' } -->\n      <!-- ko component: { name: $parent.survey.getRowWrapperComponentName(row), params: { componentData:  $parent.survey.getRowWrapperComponentData(row), templateData: { name: 'survey-row', data: row } } } -->\n      <!-- /ko -->\n  <!-- /ko -->\n</script>";

/***/ }),

/***/ "./src/knockout/templates/string.html":
/*!********************************************!*\
  !*** ./src/knockout/templates/string.html ***!
  \********************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-string\">\n    <!-- ko component: { name: renderAs, params: { locString: renderAsData } } -->\n    <!-- /ko -->\n</script>\n";

/***/ }),

/***/ "./src/knockout/templates/timerpanel.html":
/*!************************************************!*\
  !*** ./src/knockout/templates/timerpanel.html ***!
  \************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = "<script type=\"text/html\" id=\"survey-timerpanel\">\n    <!-- ko if: isRunning && showTimerAsClock -->\n    <div data-bind=\"css: rootCss\">\n        <!-- ko if: showProgress -->\n        <svg data-bind=\"css: getProgressCss(), style: { strokeDasharray: 440, strokeDashoffset: -440 * progress }\">\n            <use data-bind=\"attr:{'xlink:href': '#icon-timercircle'}\" xlink:href=''></use>\n        </svg>\n        <!-- /ko -->\n        <div data-bind=\"css: textContainerCss\">\n            <span data-bind=\"css: majorTextCss, text: clockMajorText\"></span>\n            <!-- ko if: !!minorTextCss -->\n            <span data-bind=\"css: minorTextCss, text: clockMinorText\"></span>\n            <!-- /ko -->\n        </div>\n    </div>\n    <!-- /ko -->\n    <!-- ko if: isRunning && !showTimerAsClock -->\n    <div data-bind=\"css: survey.getCss().timerRoot, text: text\"></div>\n    <!--/ko -->\n</script>\n";

/***/ }),

/***/ "knockout":
/*!********************************************************************************************!*\
  !*** external {"root":"ko","commonjs2":"knockout","commonjs":"knockout","amd":"knockout"} ***!
  \********************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_knockout__;

/***/ }),

/***/ "survey-core":
/*!*********************************************************************************************************!*\
  !*** external {"root":"Survey","commonjs2":"survey-core","commonjs":"survey-core","amd":"survey-core"} ***!
  \*********************************************************************************************************/
/*! no static exports found */
/*! ModuleConcatenation bailout: Module is not an ECMAScript module */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_survey_core__;

/***/ })

/******/ });
});
//# sourceMappingURL=survey-knockout-ui.js.map