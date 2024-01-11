$(document).ready(function () {
    $('.min_slider').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 3,
                nav: true,
                autoplay: true,
            },
            1000: {
                items: 5,
                nav: true,
                loop: true,
                autoplay: true,
            }
        }
    })

    $('.slider').owlCarousel({
        loop: true,
        margin: 10,
        dots: true,
        autoplay: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
            },
        }
    })

    $('.plus-cart').click(function () {
        let id = $(this).attr('pid').toString();
        let e = this.parentNode.children[2]
        $.ajax({
            type: 'GET',
            url: '/pluscart',
            data: {
                prod_id:id,
            },
            success: function (data) {
                console.log(data)
                e.innerText = data.quantity;
                document.getElementById('amount').innerText = data.amount;
                document.getElementById('total_amount').innerText = data.total_amount;

            }
        })
    })

    $('.minus-cart').click(function () {
        let id = $(this).attr('pid').toString();
        let e = this.parentNode.children[2]
        $.ajax({
            type: 'GET',
            url: '/minuscart',
            data: {
                prod_id:id,
            },
            success: function (data) {
                console.log(data)
                e.innerText = data.quantity;
                document.getElementById('amount').innerText = data.amount;
                document.getElementById('total_amount').innerText = data.total_amount;

            }
        })
    })

    $('.remove-cart').click(function () {
        let id = $(this).attr('pid').toString();
        let e = this
        $.ajax({
            type: 'GET',
            url: '/removecart',
            data: {
                prod_id:id,
            },
            success: function (data) {
                console.log(data)
                document.getElementById('amount').innerText = data.amount;
                document.getElementById('total_amount').innerText = data.total_amount;
                e.parentNode.parentNode.parentNode.parentNode.remove()
            }
        })
    })
});
