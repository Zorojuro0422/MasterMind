
const signupBtn = document.querySelector('.signup');
const loginBtn = document.querySelector('.login');
const displaylogin = document.querySelector('#displaylogin');
const displaysignup = document.querySelector('#displaysignup');
  signupcontainer.classList.add('active');
function toggleSignupAndLogin(){
  signupBtn.addEventListener('click', () =>{
    displaysignup.style.display="block";
    displaylogin.style.display="none";
    signupBtn.classList.add('active');
    loginBtn.classList.remove('active');
  });
  loginBtn.addEventListener('click', () =>{
    displaylogin.style.display="block";
    displaysignup.style.display="none";
    loginBtn.classList.add('active');
    signupBtn.classList.remove('active');
  });
}

toggleSignupAndLogin();