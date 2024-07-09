const startBtn = document.querySelector('.startbtn');
const landingpage = document.querySelector('#landingpage');
const loginandsignupcontainer = document.querySelector('#loginandsignupcontainer');

function getStarted() {
  startBtn.addEventListener('click', () => {
    landingpage.style.display = 'none';
    loginandsignupcontainer.style.zIndex = 2;
  });
}

getStarted();
