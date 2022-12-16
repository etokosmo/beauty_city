
var firstvalue = null;
var secondvalue = null;
var thirdvalue = null;
var fourthvalue = null;
function firstvalue_eventForm(value) {
  firstvalue = value;
};
function secondvalue_eventForm(value) {
  secondvalue = value;
};
function thirdvalue_eventForm(value) {
  thirdvalue = value;
};
function fourthvalue_eventForm(value) {
  fourthvalue = value;

};


function check() {
    if ((!!firstvalue) & (!!secondvalue) & (!!thirdvalue) & (!!fourthvalue)) {
        var code = firstvalue + secondvalue + thirdvalue + fourthvalue
        console.log(code)
        let response = fetch('/verify_user/', {
          method: 'POST',
          body: JSON.stringify({"passcode": code}),
          headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': '{{csrf_token}}',
            }
        })
        .then(r =>  r.json().then(data => ({result: data['result'], jwt: data['user_phone_number']})))
        .then(obj => setCookie('user_phone_number',obj['jwt']));
    } return true
    return false
};

var myBtn = document.getElementById('myButton');

myBtn.addEventListener('click', function(event) {
    a = check();
    if (a === false) {
        alert('Заполните все поля!');
    } else {
        jwt = getCookie('user_phone_number');
        if (jwt === null) {
            setTimeout(() => {  location.reload(true); }, 100);
        } else {
        alert('Неправильный код');
        setTimeout(() => {  location.reload(true); }, 100);
         }
    }


});

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
};
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
};

maskPhone('.contacts__form_iunput');
function maskPhone(selector, masked = '7-___-___-__-__') {
	const elems = document.querySelectorAll(selector);

	function mask(event) {
		const keyCode = event.keyCode;
		const template = masked,
			def = template.replace(/\D/g, ""),
			val = this.value.replace(/\D/g, "");
		console.log(template);
		let i = 0,
			newValue = template.replace(/[_\d]/g, function (a) {
				return i < val.length ? val.charAt(i++) || def.charAt(i) : a;
			});
		i = newValue.indexOf("_");
		if (i !== -1) {
			newValue = newValue.slice(0, i);
		}
		let reg = template.substr(0, this.value.length).replace(/_+/g,
			function (a) {
				return "\\d{1," + a.length + "}";
			}).replace(/[+()]/g, "\\$&");
		reg = new RegExp("^" + reg + "$");
		if (!reg.test(this.value) || this.value.length < 5 || keyCode > 47 && keyCode < 58) {
			this.value = newValue;
		}
		if (event.type === "blur" && this.value.length < 5) {
			this.value = "";
		}

	}

	for (const elem of elems) {
		elem.addEventListener("input", mask);
		elem.addEventListener("focus", mask);
		elem.addEventListener("blur", mask);
	}

}

