/*
   Sushi, huh? offline package downloader for GNU/Linux systems
   Copyright (C) 2008  Gonzalo Exequiel Pedone

   custom.js is part of Sushi, huh?.

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

// A nice scrambled set of funtions :P.

/*
main()

The first funtion to excute.
*/
function main()
{
 $("#packages").resizable({containment: "DIV.mainboard", amimate: true, amimateDuration: "slow", handles: "all"});
 $("#packages").draggable({containment: "DIV.mainboard", handle: "DIV.drag", snap: true, opacity: 0.5});

 $("#downloads").resizable({containment: "DIV.mainboard", amimate: true, amimateDuration: "slow", handles: "all"});
 $("#downloads").draggable({containment: "DIV.mainboard", handle: "DIV.drag", snap: true, opacity: 0.5});

 $("#dialog").dialog({bgiframe: true, width: 640, height: 480, modal: true, autoOpen: first_time_run});
 $("#descriptiondialog").dialog({bgiframe: true, width: 640, height: 480, modal: true, autoOpen: false});
 $("#downloadslistdialog").dialog({buttons: {"Download": download_packages, "Clear all": clear_downloadslist}, bgiframe: true, width: 640, height: 480, modal: true, autoOpen: false});
 $("#SearchPackages").dialog({bgiframe: true, minWidth: 0, minHeight: 0, modal: true, autoOpen: false});
 $("#downloadinfodialog").dialog({buttons: {"Ok": confirm_download_packages, "Cancel": function(){ $("#downloadinfodialog").dialog("close");}}, bgiframe: true, width: 640, height: 480, modal: true, autoOpen: false});
 $("#toolsdialog").dialog({bgiframe: true, width: 640, height: 480, modal: true, autoOpen: false});
 $("#syncdialog").dialog({bgiframe: true, width: 320, height: 240, modal: true, autoOpen: false});

 $("#downloadslisttable").droppable({accept: "TR.draggablepackage", activeClass: "ui-state-default", hoverClass: "ui-state-hover", drop: on_package_drop});
 $("#iconbar").Fisheye({maxWidth: 128, items: "a", itemsText: "span", container: "DIV.dock-container", itemWidth: 32, proximity: 32, alignment : "left", valign: "bottom", halign : "center"});

 $("#SearchPackagesInput").keypress(function(event)
 {
  if(event.keyCode == 13)
  {
   keyword = $("#SearchPackagesInput").val();

   if(keyword != "")
   {
    open_page("il_cuore/html/search.html?keyword=" + encodeURIComponent(keyword), "DIV.packagesarea");
    $("#SearchPackages").dialog("close");
   }
  }
 });

 if(ini_file_closed)
  open_page("il_cuore/html/loading_tables.html", "DIV.packagesarea");
 else
  open_page("il_cuore/html/wizard.html", "DIV.packagesarea");

 // The download info is updated every 1 second.
 $.timer(1000, update_download);
}

/*
open_page(url, where)

Open a page in a new window, tab or div.

url = URL to open.
where =
*/
function open_page(url, where)
{
 proto = "http://";

 if(url.substring(0, proto.length) == proto)
  window.open(url, "new_window");
 else
  $(where).load(url);
}

/*
get_form(form_name) -> str

Get form fields.

form_name = The form name.
*/
function get_form(form_name)
{
  try
  {
   form_fields = "?";
   fst = true;

   for(element = 0; element < window.document.forms[form_name].elements.length; element++)
   {
    element_type = String(document.forms[form_name].elements[element].type);

    if(element_type != "undefined")
    {
     if(element_type == "checkbox")
     {
      if(window.document.forms[form_name].elements[element].checked)
      {
       if(fst)
        fst = false;
       else
        form_fields += "&";

       form_fields += encodeURIComponent(window.document.forms[form_name].elements[element].name) + "=" + encodeURIComponent(self.document.forms[form_name].elements[element].value);
      }
     }
     else
     {
      if(fst)
       fst = false;
      else
       form_fields += "&";

      form_fields += encodeURIComponent(window.document.forms[form_name].elements[element].name) + "=" + encodeURIComponent(self.document.forms[form_name].elements[element].value);
     }
    }
   }
  }
  catch(e)
  {
   form_fields = "";
  }

  if(form_fields == "?")
   form_fields = "";

  return form_fields;
}

/*
hove_item()

Action when a item is hovered.
*/
function hove_item()
{
 $(this).addClass("ui-state-hover");
}

/*
unhove_item()

Action when a item is unhovered.
*/
function unhove_item()
{
 $(this).removeClass("ui-state-hover");
}

/*
update_download()

Update download info.
*/
function update_download()
{
 open_page("il_cuore/html/downloads.html", "DIV.downloadsarea");
}

/*
select_all()

Add all the viewed to the download packages list.
*/
function select_all()
{
 packages =  $("TABLE.PackagesTable>tbody>tr[title]");
 packs = "";

 for(package = 0; package < packages.length; package++)
  packs += "<LI>" + $(packages[package]).attr("title") + "</LI>";

 $("#packagesdownloadlist").append(packs);
 $("#packagesdownloadlist").makeSortedSet();
}

/*
get_next_page()

Show the next page in the wizard page.
*/
function get_next_page()
{
 open_page("il_cuore/html/wizard.html" + get_form("FormParcer"), "DIV.packagesarea");
}

/*
get_description(package_id)

Show the description of a package.

package_id = The package ID.
*/
function get_description(package_id)
{
 $("#descriptiondialog").dialog("open");
 open_page("il_cuore/html/description.html?package_id=" + encodeURIComponent(package_id), "DIV.descriptionarea");
}

/*
helper_drag_icon(event) -> object

Show a symbolic icon when a package is dragged to the download list.
*/
function helper_drag_icon(event)
{
 $("#helperdragicon").show();
 return $("#helperdragicon");
}

/*
drag_start()

This function is called when a package drag start.
*/
function drag_start()
{
 $("#downloadslistdialog").dialog("open");
}


/*
drag_stop()

This function is called when a package drag stop.
*/
function drag_stop()
{
 $("#packagesdownloadlist").makeSortedSet();
 $("#downloadslistdialog").dialog("close");
 $("BODY").append("<div id=\"helperdragicon\"><img src=\"il_cuore/images/oxygen/128x128/actions/add-files-to-archive.png\" style=\"width: 64px; height: 64px;\"></div>");
}

/*
on_package_drop(event, ui)

When a package is droped in the download list.
*/
function on_package_drop(event, ui)
{
 $("#packagesdownloadlist").append("<li style=\"padding-left:16px;cursor:pointer;background:url(il_cuore/images/oxygen/16x16/actions/dialog-close.png) bottom left no-repeat;List-style:none;\">" + ui.draggable.attr("title") + "</li>");
}

/*
clear_downloadslist()

Remove all packages in ther download list.
*/
function clear_downloadslist()
{
 $("#packagesdownloadlist>li").remove();
}

/*
download_packages()

Send all packages in the download list to the download server.
*/
function download_packages()
{
 packages =  $("#packagesdownloadlist>li");
 packs = "";

 for(package = 0; package < packages.length; package++)
 {
  if(package != 0)
   packs += "&"

  packs += "pkg" + package + "=" + encodeURIComponent($(packages[package]).text());
 }

 open_page("il_cuore/html/get_dependencies.html?" + packs, "#downloadinfodialog");
 $("#downloadinfodialog").dialog("open");
 $("#downloadslistdialog").dialog("close");
}

/*
confirm_download_packages()

Show information about packages and size before download.
*/
function confirm_download_packages()
{
 packages =  $("#fulldependencieslist>li");
 packs = "";

 for(package = 0; package < packages.length; package++)
 {
  if(package != 0)
   packs += "&"

  packs += "pkg" + package + "=" + encodeURIComponent($(packages[package]).text());
 }

 open_page("il_cuore/html/downloads.html?" + packs, "DIV.downloadsarea");
 $("#downloadinfodialog").dialog("close");
 clear_downloadslist();
}

/*
make_sync()

Sinchronize Sushi, huh? with your PC.
*/
function make_sync()
{
 $("#syncdialog").dialog("open");
 open_page("il_cuore/html/sync.html", "#syncdialog");
}

/*
show_tools()

Show the tools window.
*/
function show_tools()
{
 open_page("il_cuore/html/tools.html", "#toolsdialog");
 $("#toolsdialog").dialog("open");
}
