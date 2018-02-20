(function($) {
    /*===========================
    1. function declearetion
    ===========================*/
	var themeApp = {
        setNavbar: function() {
            if(typeof fixed_navbar != "undefined" && fixed_navbar == true) {
                $('body').addClass('has-fixed-navbar');
                $('#main-navbar').addClass('fixed');
            }
        },
        highlighter: function() {
            $('pre').each(function(i, block) {
                hljs.highlightBlock(block);
            });
        },
        mobileMenu:function() {
            $('#mobile-menu').html($('#main-menu').html());
            $('#nav-toggle-button').on('click', function(e){
                e.preventDefault();
                $('body').toggleClass('mobile-menu-opened');
            });
            $('#backdrop').on('click', function(){
                $('body').toggleClass('mobile-menu-opened');
            });
            var li = $(".mobile-menu").find('li');
            $(li).has('ul').addClass('menu-item-has-children').prepend('<span class="submenu-toggle-button"><i class="fa fa-angle-down"></i></span>');
            $('.menu-item-has-children').find('.submenu-toggle-button').on('click', function(){
                $(this).toggleClass('opened');
                $(this).siblings('ul').slideToggle();
            });
        },
        searchPopup: function() {
            var toggle_btn = $('#search-button');
            toggle_btn.on('click', function(e) {
                e.preventDefault();
                $('#search-wrap').toggleClass('visible');
                toggle_btn.toggleClass('opened');
                if ($('#search-wrap').hasClass('visible')) {
                    setTimeout(function() {
                        $('#search-wrap').find('#search').focus();
                    }, 100);
                    
                    toggle_btn.find('i').removeClass('fa-search');
                    toggle_btn.find('i').addClass('fa-close');
                } else {
                    toggle_btn.find('i').removeClass('fa-close');
                    toggle_btn.find('i').addClass('fa-search');
                };
            });
        },
        backToTop: function() {
            $(window).scroll(function(){
                if ($(this).scrollTop() > 100) {
                    $('#back-to-top').fadeIn();
                } else {
                    $('#back-to-top').fadeOut();
                }
            });
            $('#back-to-top').on('click', function(e){
                e.preventDefault();
                $('html, body').animate({scrollTop : 0},1000);
                return false;
            });
        },
        
		init:function(){
            themeApp.setNavbar();
    		themeApp.highlighter();
    		themeApp.mobileMenu();
            themeApp.searchPopup();
            themeApp.backToTop();
    	}
	}
    /*===========================
    2. Initialization
    ===========================*/
    $(document).ready(function(){
    	themeApp.init();
    });

    /*===========================
    3. menu hover effect
    ===========================*/
    $( window ).on( 'load', function(){
        var indicator = $('.line');
        var menu = $('.main-menu > ul');
        var activeItem = menu.children( '.current-menu-item' );
        var defaultWidth = 0;
        var position = menu.children('li:first-child').position();
        var defaultPosition = position.left + 16;
        if ( ! activeItem.length ) {
            activeItemWidth = 0;
        }
        if ( activeItem.length ) {
            activeItemWidth = activeItem.outerWidth() - 32;
            defaultPosition = activeItem.position().left + 16;
            defaultWidth = activeItemWidth;
            indicator.css( 'width', defaultWidth + 'px' );
            indicator.css( 'left', defaultPosition );
        }
        menu.children( 'li' ).on('mouseenter', function() {
            activeItem =$(this);
            activeItemWidth = activeItem.outerWidth() - 32;
            indicator.css( 'width', activeItemWidth + 'px' );
            indicator.css( 'left', activeItem.position().left + 16 );
        }).on( 'mouseleave', function() {
            indicator.css( 'width', defaultWidth + 'px' );
            indicator.css( 'left', defaultPosition );
        });
    });
}(jQuery));