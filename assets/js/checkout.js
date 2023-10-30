$(document).on('click','.applybtn',function(e){
    e.preventDefault();
    var $button = $(this);
    var oldValue = $button.parent().find("input").val();
    console.log(oldValue)
    $.ajax({
        url:'/checkout/apply_coupon',
        type:'GET',
        data:{
            'code':oldValue,
        },
        success:function(data){
            console.log('success')
            var old_table_data = document.getElementById('cart-total-table'); // old table 
            var htmlObject = $(data); 
            var new_table_data = htmlObject.find("#cart-total-table").html(); // new table
            if(old_table_data != null){
                old_table_data.innerHTML=new_table_data;
            }
        },
        error:function(){
            console.log('error')
        },
    });
});