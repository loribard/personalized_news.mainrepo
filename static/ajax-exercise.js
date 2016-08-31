"use strict";

function replaceNews(results) {
    $('#changing').html(results);
}


function showRedditnews(evt)  {
    $.get('/see-news',['.container'],replaceNews);
}


$('#see-news').on('click',showRedditnews);



$(document).ready(function() {
    $(#register_form).ajaxForm(function() {
        alert("Thank you for registering!");
    });
});

