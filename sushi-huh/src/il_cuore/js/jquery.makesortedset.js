/*
   Sushi, huh? offline package downloader for GNU/Linux systems
   Copyright (C) 2008  Gonzalo Exequiel Pedone

   jquery.makesortedset.js is part of Sushi, huh?.

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

// Sort a list and delete repetitions.

jQuery.fn.makeSortedSet = function(options)
{
 li = this.find("li").get();
 set = []

 for(i = 0; i < li.length; i++)
 {
  in_set = false;

  for(j = 0; j < set.length; j++)
   if($(set[j]).text() == $(li[i]).text())
    in_set = true;

  if(!in_set)
   set[set.length] = li[i];
 }

 li = set;

 li.sort(function(a, b)
 {
  ka = $(a).text();
  kb = $(b).text();

  if(ka < kb)
   return -1;

  if(ka > kb)
   return 1;

  return 0;
 });

 this.html(li);

 return this;
}
