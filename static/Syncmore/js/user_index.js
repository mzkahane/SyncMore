// const btn = document.getElementById('modify-form-btn');
//var names = '';

// select all 'button' elements with the class name="modify-form-btn"
const buttons = document.querySelectorAll('button.modify-form-btn');

// loop through each button and add a click event listener
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    // get button value (phone.id or email.id)
    const id = button.value;
    // get the id's respective form
    const form = document.getElementById(id);
    
    if (form.style.display === 'none') {
      // 👇️ this SHOWS the form
      form.style.display = 'block';
    } else {
      // 👇️ this HIDES the form
      form.style.display = 'none';
    }
    });
});
