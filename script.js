function scrollHome() {
    var ele = document.getElementById('header');

    ele.scrollIntoView({behavior: 'smooth'});
}

function scrollAboutMe() {
    var ele = document.getElementById('about-me');
    
    ele.scrollIntoView({behavior: 'smooth'});
}

function scrollProjects() {
    var ele = document.getElementById('projects');

    ele.scrollIntoView({behavior: 'smooth'});
}

function scrollContact() {
    var ele = document.getElementById('contact');

    ele.scrollIntoView({behavior: 'smooth'});
}

var viewHeight = document.documentElement.clientHeight;
var nav = document.getElementById('navbar');


// function showNav() {
//     if (window.pageYOffset >= viewHeight) {
//         nav.style.visibility = 'visible';
//     } else {
//         nav.style.visibility = 'hidden';
//     }
// }