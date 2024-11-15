import axios from "axios";

// Set CSRF token in Axios headers globally (ensure this is executed before your requests)
axios.defaults.headers.common["X-CSRFToken"] = getCookie("csrftoken");

// Function to get the CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export default axios;
