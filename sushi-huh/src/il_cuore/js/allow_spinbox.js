/*
   Sushi, huh? offline package downloader for GNU/Linux systems
   Copyright (C) 2008  Gonzalo Exequiel Pedone

   allow_spinbox.js is part of Sushi, huh?.

   Sushi, huh? is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Sushi, huh? is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Sushi, huh?.  If not, see <http://www.gnu.org/licenses/>.

   Email   : hipersayan_x@users.sourceforge.net
   Web-Site: http://sushi-huh.sourceforge.net/
*/

// Manage the spinboxes events.

/*
on_spinbox_keyup(formname, element_name, def_value)

Event when a key is released.

formname = Formulary that receives the event.
element_name = Element that receives the event.
def_value = Default value of the spinbox.
*/
function on_spinbox_keyup(formname, element_name, def_value)
{
 // Only numbers are allowed.
 allow_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
 cur_value = window.document.forms[formname].elements[element_name].value;
 new_value = "";

 for(c in cur_value)
  if(cur_value[c] in allow_values)
   new_value += cur_value[c];

 if(new_value == "")
  new_value = String(def_value);

 window.document.forms[formname].elements[element_name].value = new_value;
}


/*
on_spinbox_change(formname, element_name, min_value, max_value)

Event when the value of the spinbox changes.

formname = Formulary that receives the event.
element_name = Element that receives the event.
min_value = Minimum value of the spinbox.
max_value = Maximum value of the spinbox.
*/
function on_spinbox_change(formname, element_name, min_value, max_value)
{
 cur_value = parseInt(window.document.forms[formname].elements[element_name].value);

 if(cur_value > max_value)
  cur_value = max_value;

 if(cur_value < min_value)
  cur_value = min_value;

 window.document.forms[formname].elements[element_name].value = String(cur_value)
}

/*
on_spinbox_up_click(formname, element_name, max_value)

Event when the up button is pressed.

formname = Formulary that receives the event.
element_name = Element that receives the event.
max_value = Maximum value of the spinbox.
*/
function on_spinbox_up_click(formname, element_name, max_value)
{
 on_spinbox_change(formname, element_name);
 new_value = parseInt(window.document.forms[formname].elements[element_name].value) + 1;

 if(new_value <= max_value)
  window.document.forms[formname].elements[element_name].value = String(new_value)
}

/*
on_spinbox_down_click(formname, element_name, min_value)

Event when the down button is pressed.

formname = Formulary that receives the event.
element_name = Element that receives the event.
min_value = Minimum value of the spinbox.
*/
function on_spinbox_down_click(formname, element_name, min_value)
{
 on_spinbox_change(formname, element_name);
 new_value = parseInt(window.document.forms[formname].elements[element_name].value) - 1;

 if(new_value >= min_value)
  window.document.forms[formname].elements[element_name].value = String(new_value)
}
