// Smooth scroll for dashboard anchor links
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.sidebar-nav a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});