/* Javascript */
/* Double brackets are used to escape Python
 * Different JS classes are used for the desired effects
 * Substitution of bracketed keywords done by Python at the top */

var NUMSLIDES = {numslides};
var SLIDE_INTERVAL = {interval};
var EFFECT = {effect};
// maybe a future version could change the following constants
var SLIDESPEED = 0.86;
var EDGERESIST = 0.2;


var tmr = setInterval(function(){{tmrAction()}}, SLIDE_INTERVAL);
var current = 1;

function tmrAction() {{
    var effect = new EFFECT();
    if (current < NUMSLIDES) {{
        var nextslide = document.getElementById("frame" + (current + 1));
        current++;
        effect.fill_in(nextslide);
    }}
    else {{
        var lastslide = document.getElementById("frame" + current);
        current = 1;
        // Vanish all but first slide
        reset_prev_opac();
        // With only the first slide visible, now vanish last slide
        effect.vanish(lastslide);
    }}
}}


function Blur() {{
    this.fill_in = function(slide) {{
        // Create timer to slowly fill in opacity       
        var opac = 10;
        var new_tmr = setInterval(function() {{
            if (opac < 100) {{
                slide.style.opacity = ("0." + opac);
                opac += 10;
            }}
            else {{
                slide.style.opacity = 1;
                clearInterval(new_tmr);
            }}
        }}, 80);
    }}

    this.vanish = function(slide) {{
        // Create timer to slowly vanish last slide
        var opac = 90;
        var new_tmr = setInterval(function() {{
            if (opac > 0) {{
                slide.style.opacity = ("0." + opac);
                opac -= 10;
            }}
            else {{
                slide.style.opacity = 0;
                clearInterval(new_tmr);
            }}
        }}, 80);
    }}
}}


function Abrupt() {{
    this.fill_in = function(slide) {{
        slide.style.opacity = 1;    
    }}

    this.vanish = function(slide) {{
        slide.style.opacity = 0;
    }}
}}


function HorizontalSlide() {{
    this.fill_in = function(slide) {{
        // Create timer to slowly fill in opacity       
        // was 0 in greater than
        var hleft = 100;
        var new_tmr = setInterval(function() {{
            if (hleft > EDGERESIST) {{
                slide.style.opacity = 1;
                slide.style.left = hleft + "%";
                hleft = hleft * SLIDESPEED;
            }}
            else {{
                slide.style.left = "0px";
                clearInterval(new_tmr);
            }}
        }}, 40);
    }}

    this.vanish = function(slide) {{
        // Find first slide, raise its zIndex and move it left with marginLeft
        // When it arrives, blank the last slide and lower the zIndex of the
        // first slide to normal
        var mleft = 100; // was 90
        var slide1 = document.getElementById("frame" + 1);
        var new_tmr = setInterval(function() {{
            if (mleft > EDGERESIST) {{
                slide1.style.marginLeft = mleft + "%";
                slide1.style.zIndex = NUMSLIDES + 1;
                mleft = mleft * SLIDESPEED;
            }}
            else {{
                slide1.style.marginLeft = "0px";
                slide.style.opacity = 0;
                slide1.style.zIndex = 1;
                clearInterval(new_tmr);
            }}
        }}, 40);
    }}
}}


function VerticalSlide() {{
    this.fill_in = function(slide) {{
        // Create timer to slowly fill in opacity       
        // was 0 in greater than
        var sltop = 100;
        var new_tmr = setInterval(function() {{
            if (sltop > EDGERESIST) {{
                slide.style.opacity = 1;
                slide.style.top = sltop + "%";
                sltop = sltop * SLIDESPEED;
            }}
            else {{
                slide.style.top = "0px";
                clearInterval(new_tmr);
            }}
        }}, 40);
    }}

    this.vanish = function(slide) {{
        // Find first slide, raise its zIndex and move it left with marginLeft
        // When it arrives, blank the last slide and lower the zIndex of the
        // first slide to normal
        var mtop = 100; // was 90
        var slide1 = document.getElementById("frame" + 1);
        var new_tmr = setInterval(function() {{
            if (mtop > EDGERESIST) {{
                slide1.style.marginTop = mtop + "%";
                slide1.style.zIndex = NUMSLIDES + 1;
                mtop = mtop * SLIDESPEED;
            }}
            else {{
                slide1.style.marginTop = "0px";
                slide.style.opacity = 0;
                slide1.style.zIndex = 1;
                clearInterval(new_tmr);
            }}
        }}, 40);
    }}
}}


function reset_prev_opac() {{
    for (i = 2; i < NUMSLIDES; i++) {{
        var slide = document.getElementById("frame" + i);
        slide.style.opacity = 0;
    }}
}}
