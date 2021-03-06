$( document ).ready(function() {

	//++++++++++ From scripts_inputs.js in ubertool_eco ++++++++++++
	//BlockUI on Form Submit
	$("input[value='Submit']").click(function (e) {

		e.preventDefault();

		$.blockUI({
		  css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
		  message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static/images/loader.gif" style="margin-top:-16px">',
		  fadeIn:  500
		});
		setTimeout(function() {$('form').submit();}, 500);
	});

	$('#clearbutton').click(function(){
		// $("table[class^='tab']:visible").find(':input').each(function() {

		//Needs to only clear the selected tab
		//tab classes: [Chemical, Speciation] and [tabSel, tabUnsel]
		//divs have classes: tab_Chemical or tab_Speciation

		$('input:visible, textarea:visible').each(function() {
			switch(this.type) {
				case 'text':
					$(this).val('');
					break;
				case 'textarea':
					$(this).val('');
					break;
				case 'radio':
					this.checked = false;
					break;
				case 'number':
					$(this).val('');
					break;
				case 'checkbox':
					//need .change() to trigger chkbox change event...
					$(this).prop('checked', false).change(); 
					break;
			}
		});

		// Handles Chemical Editor tab defaults:
		if ($('li.Chemical').hasClass('tabSel')) {
			marvinSketcherInstance.clear(); //clear marvinjs sketch
		}

	});


	//Highlight errors on form 
	$('.errorlist').each(function() {
		var parentCell = $(this).parent();
		var input = $(parentCell).find('textarea, input');
		if (input.length == 0) {
			//if .errorList element is a sibling of element with error:
			input = $(parentCell).siblings('textarea, input:not([type=checkbox])');
		}
		$(input).addClass('formError');
	});

	//Remove formError class when focused on textbox:



});

// Tabbed Nav
function uberNavTabs( modelTabs, subTabs ) {
	var tab_pool = [], liTabArray = [], noOfTabs = modelTabs.length
	// Create 'tab_' & 'li.' arrays
	for (var i=0;i<noOfTabs;i++) {
		var addTabText = ".tab_"+modelTabs[i];
		tab_pool.push(addTabText);
		var addTabText_li = 'li.'+modelTabs[i];
		liTabArray.push(addTabText_li);
	}

	// Setup tab defaults
	var uptab_pool = modelTabs;
	var curr_ind = 0;
	$(".back, .submit, #metaDataToggle, #metaDataText, #resetbutton").hide();
	
	// $('.tabUnsel').hide();

	// Click handler
	$('.input_nav ul li').click(function() {
		// Check if "li" element has class (ignores the input buttons)
		if ($(this).attr('class')) {
			var testClass = $(this).attr("class").split(' ')[0];

			curr_ind = $.inArray(testClass, modelTabs);

			// Remove current tab from array;
			var liTabArrayMinusCurr = liTabArray.slice(0);
			liTabArrayMinusCurr.splice(curr_ind,1);

			if (curr_ind == 0) {

				// chemical editor tab doesn't need defaults button:
				$('#resetbutton').hide();
				
				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .next").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}

			if ( curr_ind > 0 && curr_ind < (modelTabs.length-1) ) {

				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .back, .next, #resetbutton").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}

			if ( curr_ind == (modelTabs.length-1) ) {

				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .next, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .back, .submit, #resetbutton").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}
		}
	});

	$('.next').click(function () {

		window.scroll(0,0); //scroll to top

		var tab = $(".tab:visible");
		if (curr_ind < (modelTabs.length-1)) {

			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind + 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".back, #resetbutton").show();
			// Check if this tab has subTabs
			if ( subTabs.isSubTabs && curr_ind > 1 ) {
				var subTabsText = tab_pool[curr_ind].replace(".tab_","");

				if ( subTabs.hasOwnProperty(subTabsText) ) {
					$(subTabs[subTabsText].toString()).show();
				}
			}
		}
		if (curr_ind == (modelTabs.length-1)) {
			
			$('.submit, #metaDataToggle, #metaDataText').show();
			$(".next").hide();
			
		}
	});

	$('.back').click(function () {

		window.scroll(0, 0); //scroll to top

		if (curr_ind > 0) {
			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind - 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".next, #resetbutton").show();
			// Check if this tab has subTabs
			if ( subTabs.isSubTabs ) {
				var subTabsText = tab_pool[curr_ind].replace(".tab_","");

				if ( subTabs.hasOwnProperty(subTabsText) ) {
					$(subTabs[subTabsText].toString()).show();
				}
			}
		}
		if (curr_ind == 0) {
			$(".back, #metaDataToggle, #metaDataText, #resetbutton").hide();
		}
	});
}