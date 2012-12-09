%include header_template

%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Current Events:</p>
<table class="striped" style='width: 1300px;'>

<tr style='font-weight: bold;'>
<td>ID</td>
<td>Name</td>
<td>Description</td>
<td>Category</td>
<td>Website URL</td>
<td>Image URL</td>
<td>Start Date</td>
<td>End Date</td>
<td>Location</td>
<td>Up Votes</td>
<td>Down Votes</td>
<td>Ticket Price</td>
<td>Edit</td>
</tr>

ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets

%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  <td>
	<a href='/edit/{{row[0]}}'>Edit</a>
  </td>
<!--  <td>
	<a href='/edit/{{row[0]}}?delete=delete'>Delete</a>
  </td> //-->
  </tr>
%end
</table>

%for row in rows:
  %for col in row:
    <!-- {{col}}<br> //-->
  %end
%end 


<br />

<a href='/new'>Create New</a>


%include footer_template