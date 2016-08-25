"use strict";



function replaceNewsQuote(results) {
    $("#news-quote-text").html(results);
}

function showNewsQuote(evt) {
    $.get('/news_quote', replaceNewsQuote);
}

$('#get-news-quote-button').on('click', showNewsQuote)

