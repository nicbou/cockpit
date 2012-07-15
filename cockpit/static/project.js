$(document).ready(function(){
	//Inline project editing
	$('.edit_form .submit').hide();
	$('.edit_form table input,.edit_form textarea,.edit_form select').focus(
		function(){$('.edit_form .submit').fadeIn(300);}
	);
	$('.edit_form table input,.edit_form textarea, .edit_form select').change(
		function(){$(this).addClass('changed');}
	);
	
	//Datepickers in the page
	$('#id_deadline,#id_task-deadline,#id_project-deadline').datepicker({dateFormat: "yy-mm-dd"});
	
	//Tabs and hashtag support
	$('#tabs').tabs({
		select: function(event, ui) { window.location.hash = ui.tab.hash }
	});
	
	//Hidden passwords
	$('.reveal').hide();
	$('.placeholder').click(
		function(){$(this).hide();$(this).siblings().fadeIn();}
	);
	
	//Task status changes
	$('.status a').click(function(e){
		e.preventDefault();
		$.get($(this).attr('href'));
		$(this).siblings().removeClass('current');
		$(this).addClass('current');
	});
	
	//Comment delete
	$('.comment-delete').click(function(e){
		e.preventDefault();
		$.ajax({
			context: this,
			type: "GET",
			url: $(this).attr('href'),
			success: function(data){
				$(this).parents('li').fadeOut(300);
			}
		});
	});
	

	//Contact info delete
	$('.phonenumber .delete,.emailaddress .delete,.website .delete').click(function(e){
		e.preventDefault();
		$.ajax({
			context: this,
			type: "GET",
			url: $(this).attr('href'),
			success: function(data){
				$(this).parents('.formsetfieldwrap').slideUp({duration:300,queue:false}).fadeOut({duration:300,queue:false});
			}
		});
	});
	
});