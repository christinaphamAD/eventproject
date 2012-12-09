%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>Edit EventFinder Event with ID = {{no}}</p>

<form action="/edit/{{no}}" method="get">

Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets

<table>
<tr><td>User Name*:<br><input type="text" name="Name" value="{{old[0]}}" size="100" maxlength="100"></td></tr>
<tr><td>Description*:<br><textarea name="Description" rows='10' cols='60'>{{old[1]}}</textarea></td></tr>
<tr><td>Category*:<br><input type="text" name="Category" value="{{old[2]}}" size="100" maxlength="100"></td></tr>
<tr><td>Website_URL*:<br><input type="text" name="Website_URL" value="{{old[3]}}" size="100" maxlength="100"></td></tr><tr><td>Image_URL*:<br><input type="text" name="Image_URL" value="{{old[4]}}" size="100" maxlength="100"></td></tr><tr><td>Start_Date*:<br><input type="text" name="Start_Date" value="{{old[5]}}" size="100" maxlength="100"></td></tr><tr><td>End_Date*:<br><input type="text" name="End_Date" value="{{old[6]}}" size="100" maxlength="100"></td></tr><tr><td>Location* ({{old[11]}},{{old[12]}}):<br><input type="text" name="Location" value="{{old[7]}}" size="100" maxlength="100"></td></tr><tr><td>Up_Votes*:<br><input type="text" name="Up_Votes" value="{{old[8]}}" size="100" maxlength="100"></td></tr><tr><td>Down_Votes*:<br><input type="text" name="Down_Votes" value="{{old[9]}}" size="100" maxlength="100"></td></tr><tr><td>Tickets*:<br><input type="text" name="Tickets" value="{{old[10]}}" size="100" maxlength="100"></td></tr>
</table>


<br/>
<input type="submit" name="save" value="save">
<input type="submit" value="cancel" onclick="location.replace('../'); return false;">
<!-- &nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" name="delete" value="delete"> //-->
</form>