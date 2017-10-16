/*
   Sushi, huh? offline package downloader for GNU/Linux systems
   Copyright (C) 2008  Gonzalo Exequiel Pedone

   jquery.sidebar.js is part of Sushi, huh?.

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

// Show a nice sidebar in your web page.

jQuery.fn.sideBar = function(options)
{
 sidebar_id = "#" + this.attr("id");

 this.html("<DIV id=\"sidebarcontainer\" class=\"ui-widget-content\"><DIV id=\"sidebarcontent\">" + this.html() + "</DIV></DIV><DIV id=\"sidebarsh\" class=\"ui-state-default ui-corner-left\">&gt;</DIV>")>

 $("#sidebarsh").click(function()
 {
  if($("#sidebarsh").text() == ">")
  {
   sidebarcontainerwidth = $("#sidebarcontainer").width();
   sidebarshwidth = $("#sidebarsh").width() + 14;

   $("#sidebarcontainer").attr("alt", sidebarcontainerwidth + "px")
   $("#sidebarcontainer").animate({width: "0px", padding: 0, opacity: 0}, "normal");
   $(sidebar_id).attr("alt", (sidebarcontainerwidth + sidebarshwidth))
   $(sidebar_id).animate({width: sidebarshwidth}, "fast");
   $("#sidebarsh").html("&lt;");
  }
  else
  {
   $(sidebar_id).animate({width: parseInt($(sidebar_id).attr("alt")) + 10}, "fast");
   $("#sidebarcontainer").animate({width: $("#sidebarcontainer").attr("alt"), padding: "5px", opacity: 1}, "normal");
   $("#sidebarsh").html("&gt;");
  }
 });

 $("#sidebarsh").hover(function()
 {
  $("#sidebarsh").animate({opacity: 1}, "normal");
  $("#sidebarsh").addClass("ui-state-hover");
 },
 function()
 {
  $("#sidebarsh").removeClass("ui-state-hover");
  $("#sidebarsh").animate({opacity: 0.75}, "normal");
 });

 return this;
}
