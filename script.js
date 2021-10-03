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

const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.list-links');

hamburger.addEventListener('click', mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
}

const navLink = document.querySelectorAll(".nav-link");

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}
