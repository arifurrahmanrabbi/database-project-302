var prevScrollPos = window.pageYOffset;


window.onscroll = function() {
	var currentScrollPos = window.pageYOffset;
	if (prevScrollPos > currentScrollPos || currentScrollPos < 250) {
		document.querySelector("nav").style.top = "0";
		document.querySelector(".filter_form").style.top = "8rem";
	} else {
		document.querySelector("nav").style.top = "-10rem";
		document.querySelector(".filter_form").style.top = "-20rem";
	}
	prevScrollPos = currentScrollPos;
};
