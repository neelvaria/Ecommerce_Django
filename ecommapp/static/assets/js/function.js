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