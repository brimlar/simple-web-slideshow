/* Javascript
 * The transition *effect* lives entirely in CSS (see template.css).
 * This script only toggles the .active class on each frame on a timer,
 * and CSS animates the rest. Effect selection is done by adding the
 * matching CSS class to each frame in the generated HTML.
 *
 * Frame 1 is the title slide and is baked with the .active class in the
 * generated HTML, so it is visible on first paint with no JS-timing trick.
 */

var NUMSLIDES = {numslides};
var SLIDE_INTERVAL = {interval};

var current = 1;

setInterval(function() {{
    var outgoing = document.getElementById("frame" + current);
    if (outgoing) outgoing.classList.remove("active");

    current++;
    if (current > NUMSLIDES) current = 1;

    var incoming = document.getElementById("frame" + current);
    if (incoming) incoming.classList.add("active");
}}, SLIDE_INTERVAL);
