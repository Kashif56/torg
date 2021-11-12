burger = document.querySelector('.burger')
navbar = document.querySelector('.navbar')
navlinks = document.querySelector('.nav-links')

burger.addEventListener('click', () => {
    navbar.classList.toggle('h-nav-resp');
    navlinks.classList.toggle('v-nav-resp');
})