var timeoutID;
var timeout = 10000;

function setup() {
	document.getElementById("submitButton").addEventListener("click", makePost, true);

  console.log("setup done");
}

function makePost() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var text = document.getElementById("message").value;
  console.log(text);
	httpRequest.open("POST", "/makePost");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data;
	data = "text=" + text + "&sender=" + {{ username|safe }};
  console.log("sending");
	httpRequest.send(data);
}

window.addEventListener("load", setup, true);
