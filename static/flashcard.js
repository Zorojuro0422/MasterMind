
const titleform =document.querySelector('.titleform');

function createflashcard(){
  const createflashcardbtn = document.querySelector('#createbtn');

  createflashcardbtn.addEventListener('click', () =>{
    const logoholder = document.querySelector('#mastermindlogo');

    logoholder.style.height = "30%";
    logoholder.style.width = "25%";
    logoholder.style.position = "absolute";
    logoholder.style.right = "5%";
    logoholder.style.top = "10%";

    titleform.style.display = "block";
    titleform.style.display = "flex";
    titleform.style.justifyContent = "center";
    titleform.style.alignItems = "center";
    titleform.style.flexDirection = "column";
  });
}

createflashcard();