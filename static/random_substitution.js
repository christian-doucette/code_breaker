// Returns a random permutation of the alphabet, using Fisher-Yates Shuffle Algorithm
function get_random_alphabet_permutation () {
  let nonchosen_letters = Array.from("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
  let chosen_letters    = [];


  for (i = 0; i < 26; i++) {
    const chosen_index = Math.floor(Math.random() * (26 - i));
    chosen_letters.push(nonchosen_letters[chosen_index]);
    nonchosen_letters.splice(chosen_index, 1);
  }

  return chosen_letters.join('');
}


// Sets the substitution input box to a random alphabet permutation from get_random_alphabet_permutation()
function fill_in_form_with_alphabet_permutation() {
  alphabet_permutation_textbox = document.getElementById('input_substitution');
  alphabet_permutation_textbox.value = get_random_alphabet_permutation();
}
