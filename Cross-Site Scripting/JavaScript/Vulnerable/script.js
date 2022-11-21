// To store our input data
users = []

// On input data submit, check for input validation
document.querySelector('form.form').addEventListener('submit', function (e) {
  e.preventDefault();
  let x = document.querySelector('form.form').elements;
  // Make JSON object of data
  user = { "userid": x['userid'].value, "password": x['pwd'].value };
  // Add to users list
  users.push(user)
  console.log(users);
  document.getElementById("users").innerHTML = ""
});


// Called when View Users is pressed to display data
function appendData(data) {
  document.getElementById("users").innerHTML = ""
  var mainContainer = document.getElementById("users");
  for (var i = 0; i < users.length; i++) {
    var div = document.createElement("div");
    div.innerHTML = 'Name: ' + users[i].userid + '\tPassword: ' + users[i].password;
    mainContainer.appendChild(div);
  }
}

