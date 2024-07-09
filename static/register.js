function validateForm() {
    // Get form fields
    var email = document.getElementById("email").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
  
    // Simple email validation (you can add more complex validation)
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!email.match(emailPattern)) {
      alert("Please enter a valid email address.");
      return false;
    }
  
    // Simple username validation (you can add more rules)
    if (username.length < 6) {
      alert("Username must be at least 6 characters long.");
      return false;
    }
  
    // Simple password validation (you can add more rules)
    if (password.length < 6) {
      alert("Password must be at least 8 characters long.");
      return false;
    }
    alert("Successfully Registered!");
    return true; // Form is valid, allow submission
  }
  