// Sets the rotation input box to a random rotation number from 0 to 25
function fill_in_form_with_rotation() {

  // Gets random number between 0 and 25
  const rand_rotation = Math.floor(Math.random() * 26)

  // Sets textbox to that random number
  rotation_textbox = document.getElementById('input_rot');
  rotation_textbox.value = rand_rotation;
}
