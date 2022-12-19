$(document).ready(function() {
	$('.salonsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  infinite: true,
	  prevArrow: $('.salons .leftArrow'),
	  nextArrow: $('.salons .rightArrow'),
	  responsive: [
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});
	$('.servicesSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.services .leftArrow'),
	  nextArrow: $('.services .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.mastersSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.masters .leftArrow'),
	  nextArrow: $('.masters .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.reviewsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.reviews .leftArrow'),
	  nextArrow: $('.reviews .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	// menu
	$('.header__mobMenu').click(function() {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function() {
		$('#mobMenu').hide()
	})

	let selectedDate;

	let datePicker = new AirDatepicker('#datepickerHere', {
		selectedDates: [Date],
		onSelect({date}) {
			selectedDate = date.toLocaleDateString('ru');
		},
		range: false,
    })

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function(e) {
	  	e.preventDefault()
	    this.classList.toggle("active");
	    var panel = $(this).next()
	    panel.hasClass('active') ?  
	    	 panel.removeClass('active')
	    	: 
	    	 panel.addClass('active')
	  });
	}


	$(document).on('click', '.accordion__block', function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()

		console.log(thisName)

		$.get( "/choose_categories/?salon=" + thisName, function( data ) {
			$('.service__services > .panel').text("")
			console.log(data)
			data.forEach(function (item, i, data) {
				let button = document.createElement('button');

				button.addEventListener("click", function(e) {
					e.preventDefault()
					this.classList.toggle("active");
					var panel = $(this).next()
					panel.hasClass('active') ?
						 panel.removeClass('active')
						:
						 panel.addClass('active')
				  });

				button.className = "accordion";
				button.innerHTML = item.title
				let main_div = document.createElement('div');
				main_div.className = "panel";
				let block_items_div = document.createElement('div');
				block_items_div.className = "accordion__block_items";
				main_div.append(block_items_div)
				$('.service__services > .panel').append(button).append(main_div)
				item.services.forEach(function(item, i, services) {
					let div = document.createElement('div');
					div.className = "accordion__block_item fic";
					div.innerHTML = '<div class="accordion__block_item_intro">' + item.title + '</div><div class="accordion__block_item_address">' + item.price + '₽</div>'
					block_items_div.append(div)
					div.addEventListener("click", function(e) {
						console.log(11111222)
						let thisName,thisAddress;
						thisName = $(this).find('> .accordion__block_item_intro').text()
						thisAddress = $(this).find('> .accordion__block_item_address').text()
						$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
						// $(this).parent().parent().parent().parent().find('> button.active').click()
						// $(this).parent().parent().parent().addClass('hide')
						setTimeout(() => {
							$(this).parent().parent().parent().parent().find('> button.active').click()
						}, 200)
					});
				})
			})
		});

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)
		
		// $(this).parent().addClass('hide')

		// console.log($(this).parent().parent().find('.panel').hasClass('selected'))
		
		// $(this).parent().parent().find('.panel').addClass('selected')
	})

	$(document).on('click', '.service__services', function (e) {
		$.get("/choose_masters/?salon=" + $('.service__salons > .selected').text().split('  ')[0] + '&service=' + $('.service__services > .selected').text().split('  ')[0], function (data) {
			$('.service__masters > .panel').text("")
			data.forEach(function (item, i, data) {
				let div = document.createElement('div');
				div.className = "accordion__block fic";
				div.innerHTML = '<div class="accordion__block_elems fic"><img src="img/masters/avatar/lenina/1.svg" alt="avatar" class="accordion__block_img"><div class="accordion__block_master">' + item.fields.first_name + ' ' + item.fields.second_name + '</div></div></div>'
				$('.service__masters > .panel').append(div)
			})
		});
	});

	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		// $(this).parent().parent().parent().parent().find('> button.active').click()
		// $(this).parent().parent().parent().addClass('hide')
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})



	// 	console.log($('.service__masters > .panel').attr('data-masters'))
	// if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
	// }


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function(e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function(e) {

        var service_price = $(this).attr('value');
        fetch('/get_order/', {
          method: 'POST',
          body: JSON.stringify({"service_price": service_price}),
          headers: {
            'Content-type': 'application/json; charset=UTF-8',
            }
        })
        .then(r =>  r.json().then(data => ({price: data['price'], order_id: data['order_id']})))
                .then(obj => $('#payment-form').append(`<input type="hidden" name="price" value=${obj["price"]}>`) &&
                $('#payment-form').append(`<input type="hidden" name="order_id" value=${obj["order_id"]}>`))

		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.payPopupOpenFull').click(function(e) {
	console.log($("body").data("order_sum"))
	var order_sum = $("body").data("order_sum")
	var orders_for_pay = $("body").data("orders_for_pay")
	    $('#payment-form').append(`<input type="hidden" name="price" value=${order_sum}>`);
        $('#payment-form').append(`<input type="hidden" name="order_id" value=${orders_for_pay}>`);
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function(e) {
//	    console.log($(this).attr('value'))
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})
	
	$('.authPopup__form').submit(function() {
	    var form_data = $('.authPopup__form').serialize().split('&');
	    var csrf = form_data[0].split('=')[1]
	    var tel = decodeURIComponent(form_data[1].split('=')[1])
	    document.getElementById('tel1').innerHTML = tel;
        fetch('/set_passcode/', {
          method: 'POST',
          body: JSON.stringify({"tel": tel}),
          headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrf,
            }
        });
		$('#confirmModal').arcticmodal();
//		console.log(document.cookie.match(/user_id=(.+?)(;|$)/)[1]);
		return false
	})

	//service
	$('.time__items .time__elems_elem .time__elems_btn').click(function(e) {
		e.preventDefault()
		$('.time__elems_btn').removeClass('active')
		$(this).addClass('active')
		// $(this).hasClass('active') ? $(this).removeClass('active') : $(this).addClass('active')
	})

	$(document).on('click', '.servicePage', function() {
		if($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').hasClass('selected')) {
			$('.time__btns_next').addClass('active')
		}
	})

	$(document).on('click', '.time__btns_next', function() {
		let master = $('.service__masters > .selected').text().split('  ')[0]
		let service = $('.service__services > .selected').text().split('  ')[0]
		let salon = $('.service__salons > .selected').text().split('  ')[0]
		let time = $('.time__elems_elem > .active').text()
		let timeslot = {
			'master': master,
			'service': service,
			'salon': salon,
			'day': selectedDate,
			'time': time
		}
		$.post("/servicefinally/", timeslot, function (timeslot) {
		})

})
})