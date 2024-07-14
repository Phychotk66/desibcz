document.addEventListener("DOMContentLoaded", function() {
    var showMenuBtn = document.getElementById("showMenuBtn");
    var closeMenuBtn = document.getElementById("closeMenuBtn");
    var sideMenu = document.getElementById("sideMenu");
    var categoryLinks = document.querySelectorAll('.category-link');

    showMenuBtn.addEventListener("click", function() {
        sideMenu.style.left = "0px";
    });

    closeMenuBtn.addEventListener("click", function() {
        sideMenu.style.left = "-250px";
    });

    categoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the link from navigating
            var submenu = this.parentElement.nextElementSibling;
            submenu.classList.toggle('show');
            var dropdownIcon = this.nextElementSibling;
            dropdownIcon.innerHTML = submenu.classList.contains('show') ? '&#9650;' : '&#9660;';
        });
    });
});
