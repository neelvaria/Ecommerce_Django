const monthNames = ["January", "February", "March", "April", "May", 
    "June","July", "August", "September", "October", "November", "December"];


$("#commentForm").submit(function (event) {
    event.preventDefault();

    let dt = new Date();
    let time = dt.getDay()+" "+monthNames[dt.getUTCMonth()]+" "+dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url:$(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Saved to DB!!",response);

            if (response.bool == true){
                $("#review-resp").html("Review saved successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                        _html += '<div class="thumb text-center">'
                            _html += '<img src="/static/assets/imgs/blog/author-2.png" alt="" />';
                            _html += '<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                       _html += ' </div>'
                        _html += '<div class="desc">'
                            _html += '<div class="d-flex justify-content-between mb-10">'
                                _html += '<div class="d-flex align-items-center">'
                                    _html += '<span class="font-xs text-muted">'+ time +'</span>'
                                _html += '</div>'

                                for (let i=1;i<=response.context.rating;i++){
                                    _html += '<i class="fas fa-star text-warning"></i>'
                                }

                            _html += '</div>'
                            _html += '<p class="mb-10">'+response.context.review+'</p>'
                        _html += '</div>'
                    _html += '</div>'
                _html += '</div>'
                $("#comment-list").prepend(_html)

                $("#commentForm")[0].reset();

            }
        }
    })

})

$(document).ready(function () {
    $(".filter-checkbox, #price_filter-btn").on("click", function () {
        console.log("clicked")
        
        let filter_object = {}
        let min_price = $("#min_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $(".filter-checkbox").each(function () { 
            let filter_value = $(this).val() 
            let filter_key = $(this).data("filter")

            // console.log("Filter value will be: ",filter_value)
            // console.log("Filter key will be: ",filter_key)

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter Object will be: ",filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType:"json",
            beforeSend: function () {
                console.log("Trying to Filter a PRoduct....");
            },
            success:function(response){
                console.log("Response: ",response)
                console.log("Data Sucessfully Filtered!!");
                $("#filtered-product").html(response.context)
            }
        })
    })
    $("#range").on("input", function() {
        let current_value = $(this).val();
        $("#max_price").val(current_value);  // Sync number input
    });

    // Sync number input with range input
    $("#max_price").on("keyup", function() {
        let current_value = $(this).val();
        $("#range").val(current_value);  // Sync range input
    });

     // Handle when number input loses focus (blur event)
    $("#max_price").on("blur", function() {
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();

        // console.log("Current Value:", current_price);
        // console.log("Min value:", min_price);
        // console.log("Max value:", max_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            console.log("Value is out of range");

            min_price = Math.round(min_price * 100)/100
            max_price = Math.round(max_price * 100)/100

            // console.log("##################################")
            // console.log("##################################")
            // console.log("Min value:", min_price);
            // console.log("Max value:", max_price);
            // console.log("##################################")
            // console.log("##################################")

            alert("Price must be between: ₹"+min_price+" and ₹"+max_price);
            $(this).val(min_price);
            $('#range').val(min_price);

            $(this).focus();
            return false

        }
    });

    $(".add-to-cart-btn").on("click", function () {

        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text().trim()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
    
    
        console.log("Quantity: ",quantity)
        console.log("Product Title: ",product_title)
        console.log("Product ID: ",product_id)
        console.log("Product Price: ",product_price)
        console.log("Product PID: ",product_pid)
        console.log("Product Image: ",product_image)
        console.log("Index: ",index)
        console.log("This: ",this_val)
    
    
        $.ajax({
            url: '/add-to-cart',
            data: {
                'pid':product_pid,
                'id':product_id,
                'qty':quantity,
                'title':product_title,
                'price':product_price,
                'image':product_image,
    
            },
            dataType:"json",
            beforeSend: function () {
                console.log("Added to cart....");
            },
            success:function(response){
                this_val.html("✔")
                console.log("Added to cart Sucessfully!!");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    
    })

    $(".delete-product").on("click", function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product ID: ",product_id);

        $.ajax({
            url:'/delete-from-cart',
            data:{
                "id":product_id
            },
            dataType:"json",
            beforeSend: function () {
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })
    
    $(".update-product").on("click", function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_qty = $(".product-qty-" + product_id).val()
    
        console.log("Product ID: ",product_id);
        console.log("Product QTY: ",product_qty);

        $.ajax({
            url:'/update-cart',
            data:{
                "id":product_id,
                "qty":product_qty
            },
            dataType:"json",
            beforeSend: function () {
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    //Make default address
    $(document).on("click", ".make-default-address", function () {
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("Address ID: ",id);
        console.log("This: ",this_val)

        $.ajax({
            url:'/make-default-address',
            data:{
                "id":id
            },
            dataType:"json",
            success:function(response){
                console.log("Address made Default!!!");
                if (response.bool == true) {
                    $(".check").hide()
                    $(".action-btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                }
            }
        })
        
    })
    
})

//Add to cart



//Add to cart
// $("#add-to-cart-btn").on("click", function () {


//     let quantity = $(".product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)


//     console.log("Quantity: ",quantity)
//     console.log("Product Title: ",product_title)
//     console.log("Product ID: ",product_id)
//     console.log("Product Price: ",product_price)
//     console.log("This: ",this_val)

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id':product_id,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price

//         },
//         dataType:"json",
//         beforeSend: function () {
//             console.log("Added to cart....");
//         },
//         success:function(response){
//             this_val.html("Item added to cart!!!")
//             console.log("Added to cart Sucessfully!!");
//             $(".cart-items-count").text(response.totalcartitems)
//         }
//     })
// })