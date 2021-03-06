function showMobileMenu() {
    $("#mobile").addClass("openMobileMenu", 1000);
    event.preventDefault();
};

function hideMobileMenu() {
    $("#mobile").removeClass("openMobileMenu", 1000);
    event.preventDefault();
};

$('#homeCarousel').owlCarousel({
    loop: false,
    margin: 10,
    dots: false,
    dotsEach: false,
    responsiveClass: true,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1,
            nav: true,
            loop: true
        },
        600: {
            items: 1,
            nav: true,
            loop: true
        },
        1000: {
            items: 1,
            nav: true,
            loop: true
        }
    }
})
$('#sugestions').owlCarousel({
    loop: false,
    margin: 10,
    dots: false,
    dotsEach: false,
    responsiveClass: true,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 2,
            nav: true,
            loop: true
        },
        600: {
            items: 2,
            nav: true,
            loop: true
        },
        1000: {
            items: 4,
            nav: true,
            loop: true
        }
    }
})
$('#paperCarousel').owlCarousel({
    loop: false,
    margin: 10,
    dots: false,
    dotsEach: false,
    responsiveClass: true,
    autoplay: false,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 2,
            nav: true,
            loop: false
        },
        600: {
            items: 3,
            nav: true,
            loop: false
        },
        1000: {
            items: 3,
            nav: true,
            loop: false
        }
    }
})
$('#woodenFrameCarousel').owlCarousel({
    loop: false,
    margin: 10,
    dots: false,
    dotsEach: false,
    responsiveClass: true,
    autoplay: false,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 2,
            nav: true,
            loop: false
        },
        600: {
            items: 3,
            nav: true,
            loop: false
        },
        1000: {
            items: 3,
            nav: true,
            loop: false
        }
    }
})
$('#marginCarousel').owlCarousel({
    loop: false,
    margin: 10,
    dots: false,
    dotsEach: false,
    responsiveClass: true,
    autoplay: false,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 2,
            nav: true,
            loop: false
        },
        600: {
            items: 3,
            nav: true,
            loop: false
        },
        1000: {
            items: 3,
            nav: true,
            loop: false
        }
    }
})

var slide = function (item) {
    if ($('#' + item).is(':visible')) {
        $('#' + item).css({
            'display': 'block'
        });
        $('#' + item).slideToggle('slow');
        $(".mobileNav li a i").removeClass('fa-sort-up');
        $(".mobileNav li a i").addClass('fa-sort-down');
    } else {
        $('#' + item).css({
            'display': 'none'
        });
        $('#' + item).slideToggle('slow');
        $(".mobileNav li a i").removeClass('fa-sort-down');
        $(".mobileNav li a i").addClass('fa-sort-up');
    }
};

function toggle_visibility(id) {
    var e = document.getElementById(id);
    if (e.style.display == 'block')
        e.style.display = 'none';
    else
        e.style.display = 'block';
};

function userProfileToggle(item1, item2, item3, item4, item5, item6) {
    $('#' + item1).fadeIn(500);
    $('#' + item2).hide();
    $('#' + item3).hide();
    $('#' + item4).hide();
    $('#' + item5).hide();
    $('#' + item6).hide();
};
