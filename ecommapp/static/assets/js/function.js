$("#commentForm").submit(function (event) {
    event.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url:$(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Saved to DB!!");

            if (response.bool == true){
                $("#review-resp").html("Review saved successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = `
                <div class="single-comment justify-content-between d-flex mb-30">
                    <div class="user justify-content-between d-flex">
                        <div class="thumb text-center">
                            <img src="{% static 'assets/imgs/blog/author-2.png' %}" alt="" />
                            <a href="#" class="font-heading text-brand">{{r.user.username|title}}</a>
                        </div>
                        <div class="desc">
                            <div class="d-flex justify-content-between mb-10">
                                <div class="d-flex align-items-center">
                                    <span class="font-xs text-muted">{{r.date|date:"d M Y"}} </span>
                                </div>
                                <div class="product-rate d-inline-block">
                                    <div class="product-rating" style="width: 100%">{{r.rating}}</div>
                                </div>
                            </div>
                            <p class="mb-10">{{r.review}}<a href="#" class="reply">Reply</a></p>
                        </div>
                    </div>
                </div>
                `
            }
        }
    })

})