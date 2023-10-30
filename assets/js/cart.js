console.log(auth);

function getCookie(name) {
    var cookieArr = document.cookie.split(";");
    for(var i = 0; i<cookieArr.length; i++){
        var cookiePair = cookieArr[i].split("=");
        if(name == cookiePair[0].trim()){
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}
var cart = JSON.parse(getCookie('cart'));
if (cart==undefined){
    cart = {}
    document.cookie = 'cart='+JSON.stringify(cart) + ";domain;path=/;SameSite=Lax;Secure"
}

function bindButtonClick(){
    $(".cart-plus-minus").prepend('<div class="dec qtybutton">-</div>');
    $(".cart-plus-minus").append('<div class="inc qtybutton">+</div>');
    $(".qtybutton").on("click", function() {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
        if ($button.text() == "+") {
            var newVal = parseFloat(oldValue) + 1;
        } 
        else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } 
            else {
                newVal = 0;
            }
        }
        $button.parent().find("input").val(newVal);
    });
}    

    // $(".cart-plus-minus-only").prepend('<div class="dec qtybutton-only">-</div>');
    // $(".cart-plus-minus-only").append('<div class="inc qtybutton-only">+</div>');
    // $(".qtybutton-only").on("click", function() {
    //     var $button = $(this);
    //     var oldValue = $button.parent().find("input").val();
    //     if ($button.text() == "+") {
    //         var newVal = parseFloat(oldValue) + 1;
    //     } 
    //     else {
    //         if (oldValue > 0) {
    //             var newVal = parseFloat(oldValue) - 1;
    //         } 
    //         else {
    //             newVal = 0;
    //         }
    //     }
    //     $button.parent().find("input").val(newVal);
    // });

function updateCartEvent(){
    var $body = $('body');
    var $ltn__utilizeToggle = $('.ltn__utilize-toggle'),
        $ltn__utilize = $('.ltn__utilize'),
        $ltn__utilizeOverlay = $('.ltn__utilize-overlay'),
        $mobileMenuToggle = $('.mobile-menu-toggle');
    $ltn__utilizeToggle.on('click', function (e) {
        e.preventDefault();
        var $this = $(this),
            $target = $this.attr('href');
        $body.addClass('ltn__utilize-open');
        $($target).addClass('ltn__utilize-open');
        $ltn__utilizeOverlay.fadeIn();
        if ($this.parent().hasClass('mobile-menu-toggle')) {
            $this.addClass('close');
        }
    });
    $('.ltn__utilize-close, .ltn__utilize-overlay').on('click', function (e) {
        e.preventDefault();
        $body.removeClass('ltn__utilize-open');
        $ltn__utilize.removeClass('ltn__utilize-open');
        $ltn__utilizeOverlay.fadeOut();
        $mobileMenuToggle.find('a').removeClass('close');
    });
}

function mobileltn__utilizeMenu() {
    var $ltn__utilizeNav = $('.ltn__utilize-menu, .overlay-menu'),
        $ltn__utilizeNavSubMenu = $ltn__utilizeNav.find('.sub-menu');

    /*Add Toggle Button With Off Canvas Sub Menu*/
    $ltn__utilizeNavSubMenu.parent().prepend('<span class="menu-expand"></span>');

    /*Category Sub Menu Toggle*/
    $ltn__utilizeNav.on('click', 'li a, .menu-expand', function (e) {
        var $this = $(this);
        if ($this.attr('href') === '#' || $this.hasClass('menu-expand')) {
            e.preventDefault();
            if ($this.siblings('ul:visible').length) {
                $this.parent('li').removeClass('active');
                $this.siblings('ul').slideUp();
                $this.parent('li').find('li').removeClass('active');
                $this.parent('li').find('ul:visible').slideUp();
            } else {
                $this.parent('li').addClass('active');
                $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                $this.closest('li').siblings('li').find('ul:visible').slideUp();
                $this.siblings('ul').slideDown();
            }
        }
    });
}

$(document).on('click','.nice-select .option',function(e){
    var selectedVal = $(this).data('value');
    var url = '/product?filter='+filter+'&orderby='+selectedVal;
    window.location.href = url;
});

$(document).on('click','.add-item',function(){
    var id = $(this).data('id');
    var q = document.getElementById("cart-plus-minus-box");
    if (q!=null){
        q = q.value;
    }
    else{
        q = 1;
    }
    console.log(q);
    if( auth === "False" ){
        console.log('Not logged in')
        addCookieItem(id,q)
    }
    else{
        $.ajax({
            url:'',
            type:'GET',
            data:{
                'id':id,
                'cart':'cart',
                'quantity':q
            },
            success:function(data){
                $('#add_to_cart_modal .modal-dialog').html($('#add_to_cart_modal .modal-dialog',data));
                $('#add_to_cart_modal').modal('show');
                $('#update-cart .update').html($('#update-cart .update',data));
                $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
                updateCartEvent();
                //bindButtonClick();
            },
            error:function(){
                console.log('error')
            },
        });
    }
});
function addCookieItem(id, quantity){
    if(cart[id] == undefined){
        cart[id] = {'quantity': quantity}
    }
    else{
        cart[id]['quantity'] = quantity
    }
    console.log(cart)
    document.cookie = 'cart='+JSON.stringify(cart) + ";domain;path=/;SameSite=Lax;Secure"
    $.ajax({
        url:'',
        type:'GET',
        data:{
            'id':id,
        },
        success:function(data){
            $('#add_to_cart_modal .modal-dialog').html($('#add_to_cart_modal .modal-dialog',data));
            $('#add_to_cart_modal').modal('show');
            $('#update-cart .update').html($('#update-cart .update',data));
            $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
            updateCartEvent();
            //bindButtonClick();
        },
        error:function(){
            console.log('error')
        },
    });
}


$(document).on('click','.add-product',function(){
    var id = $(this).data('id');
    console.log(auth)
    if(auth=='False'){
        $('#liton_wishlist_modal').modal('show');
    }
    else {
    $.ajax({
        url:'',
        type:'GET',
        data:{
            'id':id,
            'wishlist': 'wishlist'
        },
        success:function(data){
            $('#liton_wishlist_modal .modal-dialog').html($('#liton_wishlist_modal .modal-dialog',data));
            $('#liton_wishlist_modal').modal('show');
            $('#update-cart .update').html($('#update-cart .update',data));
            $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
            updateCartEvent();
            //bindButtonClick();
        },
        error:function(){
            console.log('error')
        },
    });
    }
});

$(document).on('click','.view-product',function(){
    var id = $(this).data('id');
    console.log(id)
    $.ajax({
        url:'',
        type:'GET',
        data:{
            'id':id,
        },
        success:function(data){
            $('#quick_view_modal .modal-dialog').html($('#quick_view_modal .modal-dialog',data));
            $('#quick_view_modal').modal('show');
            $('#update-cart .update').html($('#update-cart .update',data));
            $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
            updateCartEvent();
            //bindButtonClick();
        },
        error:function(){
            console.log('error')
        },
    });
});

function updateCookieItem(id, action){
    if(action == "remove"){
        delete cart[id]
    }
    console.log(cart)
    document.cookie = 'cart='+JSON.stringify(cart) + ";domain;path=/;SameSite=Lax;Secure"
}

$(document).on('click','.remove-cart',function(){
    var id = $(this).data('id');
    var action = $(this).data('action');
    console.log(id, action)
    if( auth === "False" ){
        updateCookieItem(id,action);
    }
    $.ajax({
        url:'/cart/',
        type:'GET',
        data:{
            'id':id,
            'action': action
        },
        success:function(data){
            var old_table_data = document.getElementById('tableid'); // old table 
            var htmlObject = $(data); 
            var new_table_data = htmlObject.find("#tableid").html(); // new table
            if(old_table_data != null){
                old_table_data.innerHTML=new_table_data;
            }
            $('#update-cart .update').html($('#update-cart .update',data));
            $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
            updateCartEvent();
            //bindButtonClick();
        },
        error:function(){
            console.log('error')
        },
    });
});

function cartCookieItem(id, quantity){
    if (quantity <= '0'){
        delete cart[id]
    }
    else{
        cart[id]['quantity'] = quantity
    }
    document.cookie = 'cart='+JSON.stringify(cart) + ";domain;path=/;SameSite=Lax;Secure"
};

$(document).on('click','.qtybutton-only',function(){
    var id = $(this).data('id');
    var quantity = $(this).data('quantity');
    if( auth === "False" ){
        cartCookieItem(id,quantity);
    }
    $.ajax({
        url:'/cart/update/',
        type:'GET',
        data:{
            'id':id,
            'quantity': quantity
        },
        success:function(data){
            var old_table_data = document.getElementById('tableid'); // old table 
            var htmlObject = $(data); 
            var new_table_data = htmlObject.find("#tableid").html(); // new table
            if(old_table_data != null){
                old_table_data.innerHTML=new_table_data;
            }
            $('#update .shoping-cart-total').html($('#update .shoping-cart-total',data));
            $('#update-cart .update').html($('#update-cart .update',data));
            $('#ltn__utilize-cart-menu .ltn__utilize-menu-inner').html($('#ltn__utilize-cart-menu .ltn__utilize-menu-inner',data));
            updateCartEvent();
        },
        error:function(){
            console.log('error')
        },
    });
});