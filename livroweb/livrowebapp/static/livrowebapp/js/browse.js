document.addEventListener('DOMContentLoaded', function () {
    function openPopup(url) {
        fetch(url)
        .then(response => response.text())
        .then(data => {
            var popupContainer = document.getElementById('popup-container');
            popupContainer.innerHTML = data;
            popupContainer.style.display = 'flex';
            popupContainer.classList.add('overlay');  // Add the overlay class

            if(url == '/signup/'){
                let password = document.getElementById ("password");
                let confirmpassword = document.getElementById ("confirmpassword");
                let showpassword = document.getElementById ("showpassword");
            
                showpassword.onclick = function (){
                    if(password.type == "password") {
                        password.type = "text";
                        confirmpassword.type = "text"
                    }else{
                        password.type = "password";
                        confirmpassword.type = "password"
                    }
                
                    password.classList.toggle("show-password");
                    confirmpassword.classList.toggle("show-password");
            };}
                
        })
        .catch(error => console.error('Error fetching content:', error));
    }



    document.getElementById('login-button').addEventListener('click', function () {
        openPopup('/signin/');
    });

    document.getElementById('signup-button').addEventListener('click', function () {
        openPopup('/signup/');
    });

    window.addEventListener('popstate', function (event) {
        closePopup();
    });

});

function closeSignIn() {
    document.querySelector('.wrap').style.display = 'none';
    removeOverlay();
}

document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.closebutton');
    if (closeButton) {
        closeButton.addEventListener('click', closeSignIn);
    }
});

function closeSignUp() {
    document.querySelector('.popup').style.display = 'none';
    removeOverlay();
}

document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeSignUp);
    }
});

function removeOverlay() {
    var popupContainer = document.getElementById('popup-container');
    popupContainer.innerHTML = '';  // Clear the content when closing
    popupContainer.style.display = 'none';
    popupContainer.classList.remove('overlay');  // Remove the overlay class
}

document.addEventListener('DOMContentLoaded', function () {
    function openPopup(url) {
        fetch(url)
        .then(response => response.text())
        .then(data => {
            var popupContainer = document.getElementById('popup-container');
            popupContainer.innerHTML = data;
            popupContainer.style.display = 'flex';
            popupContainer.classList.add('overlay');  // Add the overlay class

            if(url == '/signup/'){
                let password = document.getElementById ("password");
                let confirmpassword = document.getElementById ("confirmpassword");
                let showpassword = document.getElementById ("showpassword");

                showpassword.onclick = function (){
                    if(password.type == "password") {
                        password.type = "text";
                        confirmpassword.type = "text"
                    }else{
                        password.type = "password";
                        confirmpassword.type = "password"
                    }

                    password.classList.toggle("show-password");
                    confirmpassword.classList.toggle("show-password");
            };}
        })
        .catch(error => console.error('Error fetching content:', error));
}


    document.getElementById('login-button').addEventListener('click', function () {
        openPopup('/signin/');
    });
    
    document.getElementById('signup-button').addEventListener('click', function () {
        openPopup('/signup/');
    });

    window.addEventListener('popstate', function (event) {
        closePopup();
    });

});

function closeSignIn() {
    document.querySelector('.wrap').style.display = 'none';
    removeOverlay();
}

document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.closebutton');
    if (closeButton) {
        closeButton.addEventListener('click', closeSignIn);
    }
});

function closeSignUp() {
    document.querySelector('.popup').style.display = 'none';
    removeOverlay();
}

document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeSignUp);
    }
});

function removeOverlay() {
    var popupContainer = document.getElementById('popup-container');
    popupContainer.innerHTML = '';  // Clear the content when closing
    popupContainer.style.display = 'none';
    popupContainer.classList.remove('overlay');  // Remove the overlay class
}

const genreButtons = document.querySelectorAll('.genre-button');
const genreBoxes = document.querySelectorAll('.genrebox');
const hiddenBoxes = document.querySelectorAll('#h2, #h3, #h4, #h5, #h6,#h7,#h8, #h9');

hiddenBoxes.forEach(box => {
    box.style.display = 'none';
  });

genreButtons.forEach((button, index) => {
  button.addEventListener('click', () => {
    display = index + 1;
    updateGenreDisplay();
    updateHiddenDisplay(); 
  });
});

function updateHiddenDisplay() {
    hiddenBoxes.forEach((box, index) => {
      if (index === display - 1) {
        box.style.display = 'block';
      } else {
        box.style.display = 'none';
      }
    });
  }

function updateGenreDisplay() {
  genreBoxes.forEach((box, index) => {
    if (index === display - 0) {
      box.style.display = 'block';
    } else {
      box.style.display = 'none';
    }
  });
}