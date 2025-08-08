/*!
 * surveyjs - Survey JavaScript library v1.12.47
 * Copyright (c) 2015-2025 Devsoft Baltic OÜ  - http://surveyjs.io/
 * License: MIT (http://www.opensource.org/licenses/mit-license.php)
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define("english", [], factory);
	else if(typeof exports === 'object')
		exports["english"] = factory();
	else
		root["SurveyLocales"] = factory();
})(this, function() {
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./packages/survey-core/src/localization/english.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./packages/survey-core/src/localization/english.ts":
/*!**********************************************************!*\
  !*** ./packages/survey-core/src/localization/english.ts ***!
  \**********************************************************/
/*! exports provided: englishStrings */
/*! ModuleConcatenation bailout: Module is an entry point */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "englishStrings", function() { return englishStrings; });
// Uncomment the line below if you create a custom dictionary
// import { setupLocale } from "survey-core";
var englishStrings = {
    pagePrevText: "Previous",
    pageNextText: "Next",
    completeText: "Complete",
    previewText: "Preview",
    editText: "Edit",
    startSurveyText: "Start",
    otherItemText: "Other (describe)",
    noneItemText: "None",
    refuseItemText: "Refuse to answer",
    dontKnowItemText: "Don't know",
    selectAllItemText: "Select All",
    deselectAllItemText: "Deselect all",
    progressText: "Page {0} of {1}",
    indexText: "{0} of {1}",
    panelDynamicProgressText: "{0} of {1}",
    panelDynamicTabTextFormat: "Panel {panelIndex}",
    questionsProgressText: "Answered {0}/{1} questions",
    emptySurvey: "The survey doesn't contain any visible elements.",
    completingSurvey: "Thank you for completing the survey",
    completingSurveyBefore: "You have already completed this survey.",
    loadingSurvey: "Loading Survey...",
    placeholder: "Select...",
    ratingOptionsCaption: "Select...",
    value: "value",
    requiredError: "Response required.",
    requiredErrorInPanel: "Response required: answer at least one question.",
    requiredInAllRowsError: "Response required: answer questions in all rows.",
    eachRowUniqueError: "Each row must have a unique value.",
    numericError: "The value should be numeric.",
    minError: "The value should not be less than {0}",
    maxError: "The value should not be greater than {0}",
    textNoDigitsAllow: "Numbers are not allowed.",
    textMinLength: "Please enter at least {0} character(s).",
    textMaxLength: "Please enter no more than {0} character(s).",
    textMinMaxLength: "Please enter at least {0} and no more than {1} characters.",
    minRowCountError: "Please fill in at least {0} row(s).",
    minSelectError: "Please select at least {0} option(s).",
    maxSelectError: "Please select no more than {0} option(s).",
    numericMinMax: "The '{0}' should be at least {1} and at most {2}",
    numericMin: "The '{0}' should be at least {1}",
    numericMax: "The '{0}' should be at most {1}",
    invalidEmail: "Please enter a valid e-mail address.",
    invalidExpression: "The expression: {0} should return 'true'.",
    urlRequestError: "The request returned error '{0}'. {1}",
    urlGetChoicesError: "The request returned empty data or the 'path' property is incorrect",
    exceedMaxSize: "The file size should not exceed {0}.",
    noUploadFilesHandler: "Files cannot be uploaded. Please add a handler for the 'onUploadFiles' event.",
    otherRequiredError: "Response required: enter another value.",
    uploadingFile: "Your file is uploading. Please wait several seconds and try again.",
    loadingFile: "Loading...",
    chooseFile: "Choose file(s)...",
    noFileChosen: "No file selected",
    filePlaceholder: "Drag and drop a file here or click the button below to select a file to upload.",
    confirmDelete: "Are you sure you want to delete this record?",
    keyDuplicationError: "This value should be unique.",
    addColumn: "Add Column",
    addRow: "Add Row",
    removeRow: "Remove",
    emptyRowsText: "There are no rows.",
    addPanel: "Add new",
    removePanel: "Remove",
    showDetails: "Show Details",
    hideDetails: "Hide Details",
    choices_Item: "item",
    matrix_column: "Column",
    matrix_row: "Row",
    multipletext_itemname: "text",
    savingData: "The results are being saved on the server...",
    savingDataError: "An error occurred and we could not save the results.",
    savingDataSuccess: "The results were saved successfully!",
    savingExceedSize: "Your response exceeds 64KB. Please reduce the size of your file(s) and try again or contact the survey owner.",
    saveAgainButton: "Try again",
    timerMin: "min",
    timerSec: "sec",
    timerSpentAll: "You have spent {0} on this page and {1} in total.",
    timerSpentPage: "You have spent {0} on this page.",
    timerSpentSurvey: "You have spent {0} in total.",
    timerLimitAll: "You have spent {0} of {1} on this page and {2} of {3} in total.",
    timerLimitPage: "You have spent {0} of {1} on this page.",
    timerLimitSurvey: "You have spent {0} of {1} in total.",
    clearCaption: "Clear",
    signaturePlaceHolder: "Sign here",
    signaturePlaceHolderReadOnly: "No signature",
    chooseFileCaption: "Select File",
    takePhotoCaption: "Take Photo",
    photoPlaceholder: "Click the button below to take a photo using the camera.",
    fileOrPhotoPlaceholder: "Drag and drop or select a file to upload or take a photo using the camera.",
    replaceFileCaption: "Replace file",
    removeFileCaption: "Remove this file",
    booleanCheckedLabel: "Yes",
    booleanUncheckedLabel: "No",
    confirmRemoveFile: "Are you sure that you want to remove this file: {0}?",
    confirmRemoveAllFiles: "Are you sure that you want to remove all files?",
    questionTitlePatternText: "Question Title",
    modalCancelButtonText: "Cancel",
    modalApplyButtonText: "Apply",
    filterStringPlaceholder: "Type to search...",
    emptyMessage: "No data to display",
    noEntriesText: "No entries yet.\nClick the button below to add a new entry.",
    noEntriesReadonlyText: "No entries",
    tabTitlePlaceholder: "New Panel",
    more: "More",
    tagboxDoneButtonCaption: "OK",
    selectToRankEmptyRankedAreaText: "All choices are selected for ranking",
    selectToRankEmptyUnrankedAreaText: "Drag choices here to rank them",
    ok: "OK",
    cancel: "Cancel",
};
// Uncomment the lines below if you create a custom dictionary.
// Replace "en" with a custom locale code (for example, "fr" or "de"),
// Replace `englishStrings` with the name of the variable that contains the custom dictionary.
//setupLocale({ localeCode: "en", strings: englishStrings, nativeName: "English", englishName: "English" });


/***/ })

/******/ });
});
//# sourceMappingURL=english.js.map