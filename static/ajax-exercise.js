"use strict";




function replaceHomePage(results) {
    $(#registerform).html(results);
}

function showRegistratonForm(evt) {
    $.get('#saying', replaceHomePage);
}

$('#register').on('click', showRegistrationForm)

