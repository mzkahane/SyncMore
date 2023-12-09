// const btn = document.getElementById('modify-form-btn');
//var names = '';

// select all 'button' elements with the class name="modify-form-btn"
const buttons = document.querySelectorAll('button.modify-form-btn');

// function for toggling the modify form of each phone and email on User Home Page (index.html)
// loop through each button and add a click event listener
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    // get button value (phone.id or email.id)
    const id = button.dataset.id;
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


// function for filtering documents by document type on User Personal Drive (index.html)
function filterDocuments() {
  console.log("Filter function called");
  // var documentType = document.getElementById('documentTypeSelector').value;
  // fetchDocuments(documentType);
  const documents_list = document.querySelectorAll(".document-item"); // select all document-items
  // grab the value in the event target's data-filter attribute

  var filter = document.getElementById('documentTypeSelector').value;
  console.log(filter);

  if (filter === 'All') {
    console.log("inside all filter");
    documents_list.forEach(doc => {
      console.log(doc.dataset.id);
      doc.classList.remove('hidden')
      doc.classList.add('active-document');
    });
  }  else {
    console.log("inside other filter");
    documents_list.forEach(doc => {
          const typ = doc.dataset.id; // get the document type from its data-id
          console.log(typ);
          if (typ === filter) {
              doc.classList.remove('hidden');
              doc.classList.add('active-document');
          } else {
              doc.classList.add('hidden');
              doc.classList.remove('active-document');
          }
      });
  };
  
}


// select all elements with class name="expiration-date"
// const expirationDates = document.querySelectorAll('expiration-date');
// console.log("outside expiration dates forEach");
// // loop through each expiration date element and check if expiration-date is today or older than today
// expirationDates.forEach((date) => {
//   console.log("inside expiration dates forEach");
//   const expires = date.innerHTML;

//   var varDate = new Date(expires); //dd-mm-YYYY
//   var today = new Date();
//   today.setHours(0,0,0,0);

//   if(varDate >= today) {
//     //Do something..
//     alert("Working!");
//     expires.classList.add('expired');
//     }
// });

