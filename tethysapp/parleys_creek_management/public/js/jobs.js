function updateLink(id, status, link) {
	var link_selector;
	
	link_selector = $('tr#' + id + ' td.results');
	
	if (status === 'success') {
		// Create a link to browse the results
		var results_link = '<a href="' + link + '">View Results</a>';
		
		$(link_selector).html(results_link);
	} else {
		$(link_selector).html('');
	}
}

function updateStatus(id, status, percentage) {
	var status_selector;
	
	status_selector = $('tr#' + id + ' td.status');
	
	if (status !== 'error') {
		if ($('tr#' + id + ' td.status .job-percentage .bar').length === 0) {
			// Replace pending with progress bar
			var progress_bar;
			progress_bar = '<div class="job-percentage progress progress-striped active">'
					 	 +   '<div class="bar" style="width: 0%;"></div>'
					 	 + '</div>';
			
			$(status_selector).html(progress_bar);	 	 
		} else {
			// Update progress bar percentage
			$('tr#' + id + ' td.status .job-percentage .bar').css('width', percentage + '%');
		}
		
		if (status === 'success') {
			setTimeout(function(){
				// Set status to success
				$(status_selector).html(status);
			}, 1000);
		}
	
	} else {
		// Set status to error
		$(status_selector).html(status);
	}
}

function updateRunButton(id, status) {
	var run_button_selector;
	
	run_button_selector = $('tr#' + id + ' .run-btn');
	
	if (status !== 'error') {
		$(run_button_selector).css('display', 'none');
	} else {
		$(run_button_selector).html('ReRun');
		$(run_button_selector).css('display', 'inline-block');
	}
	
}

function checkStatus(id) {
	$.ajax({
		method: "get",
		url: id +"/status"
	}).done(function(data){
		// Make sure data has status in it
		if ('status' in data) {
			// Update the status field and run button
			updateStatus(id, data['status'], data['percentage']);
			updateRunButton(id, data['status']);
			
			// If not successful set time to check again
			if (data['status'] !== 'success') {
				// Set timeout to check again
				setTimeout(function() { checkStatus(id); }, 3000);
				
			} else {
				updateLink(id, data['status'], data['link']);
			}
		}
		
	});
	
}

function submitRunRequest(id) {	
	$.ajax({
		method: "get",
		url: id + "/run"
	});
	
	checkStatus(id);
}


$(function(){

});
