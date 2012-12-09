<link rel="stylesheet" media="all" type="text/css" href="http://code.jquery.com/ui/1.9.1/themes/smoothness/jquery-ui.css" />
<link rel="stylesheet" media="all" type="text/css" href="static/jquery-ui-timepicker-addon.css" />

<script type="text/javascript" src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
<script type="text/javascript" src="http://code.jquery.com/ui/1.9.1/jquery-ui.min.js"></script>
<script type="text/javascript" src="static/jquery-ui-timepicker-addon.js"></script>
<script type="text/javascript" src="static/jquery-ui-sliderAccess.js"></script>

		<script type="text/javascript">
			
			$(function(){

				$('#start').datetimepicker();
				$('#end').datetimepicker();
			
			});
			
		</script>

%#template for the form for a new website
<p>Add a new event to EventFinder:</p>
<form action="/new" method="GET">

ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets

<table>
<tr><td valign='top'>Event Name:<br> <input type="text" size="100" maxlength="500" name="Name"></td></tr>
<tr><td valign='top'>Description:<br> <textarea rows='10' cols='60' name="Description"></textarea></td></tr>
<tr><td valign='top'>Category:<br> <input type="text" size="100" maxlength="500" name="Category"></td></tr>
<tr><td valign='top'>URL:<br> <input type="text" size="100" maxlength="500" name="Website_URL"></td></tr>
<tr><td valign='top'>Image URL:<br> <input type="text" size="100" maxlength="500" name="Image_URL"></td></tr>

<tr><td valign='top'>Start Date:<br> <input type="text" size="100" maxlength="500" id='start' name="Start_Date"></td></tr>
<tr><td valign='top'>End Date:<br> <input type="text" size="100" maxlength="500" id='end' name="End_Date"></td></tr>

<tr><td valign='top'>Location:<br> <input type="text" size="100" maxlength="500" name="Location"></td></tr>
<!-- <tr><td valign='top'>Up Votes:<br> <input type="text" size="100" maxlength="500" name="Up_Votes"></td></tr>
<tr><td valign='top'>Down Votes:<br> <input type="text" size="100" maxlength="500" name="Down_Votes"></td></tr> //-->
<tr><td valign='top'>Tickets:<br> <input type="text" size="100" maxlength="500" name="Tickets"></td></tr>

<tr><td valign='top'><input type="submit" name="save" value="save"></td></tr>
</table>

</form>