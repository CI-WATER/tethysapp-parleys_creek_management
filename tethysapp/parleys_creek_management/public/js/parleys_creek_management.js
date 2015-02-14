/*****************************************************************************
 * FILE:    gssha_explorer.js
 * DATE:    6 September 2013
 * AUTHOR: Nathan R. Swain
 * COPYRIGHT: (c) 2013 Brigham Young University
 * LICENSE: BSD 2-Clause
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/

var GOLDSIM = (function packModel() {
	// Wrap the library in a package function
	"use strict"; // And enable strict mode for this library
	
	/************************************************************************
 	*                      MODULE LEVEL / GLOBAL VARIABLES
 	*************************************************************************/
 	var map,						// GoogleEarth map object
		libraryObject;				// Object returned by the module
		
		
	
	/************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
	/* These functions will be private functions, not accessible outside of the
	 * library. Declare function first, then define.
	 *  
	 * For Example:
	 * // Cookie Management function declarations
	 * var checkCookie;
	 * checkCookie = function(name) {
	 * 	  return docCookies.hasItem(name);
	 * };
	 */
	var initStages;
	
	initStages = function() {
	   var height, margin, stage_height;
	   
	   height = parseInt($('.wrapper').css('height'));
	   
	   $('.stage').each(function(){
           $(this).css('height', height);
        });
	};
	
	/************************************************************************
 	*                            TOP LEVEL CODE
 	*************************************************************************/
	/*
	 * Library object that contains public facing functions of the package.
	 */
	libraryObject = {
		
		// Click Submit from Remote Button
		remoteSubmit:  function(formID) {
			// Code here
			$(formID).submit();
		},
		
		// Initialize the OpenLayers Map
		initGoogleMap: function() {
			// Map constructor
	 	},
	};
	
	
	// Initialization: jQuery function that gets called when 
	// the DOM tree finishes loading
	$(function() {
		
		// Handle delete checkboxes
		$(".tabular-delete-box").change(function(){
			var isChecked, group;
			
			isChecked = $(this).attr("checked");
			group = $(this).attr("for");
			
			// If the checkbox is checked, disable fields.
			if (isChecked)
				{
					$("input[group=" + group + "]").prop("disabled", true);
				}
			else
				{
					$("input[group=" + group + "]").prop("disabled", false);
				}
		});
		
		// nitialize stages
		initStages();
	});
	
	

	return libraryObject;

}()); // End of package wrapper

/*****************************************************************************
 *                      Public Functions
 *****************************************************************************/
function remoteSubmit(formID) {
	"use strict";
	
	// Pass through the library object
	GOLDSIM.remoteSubmit(formID)
}