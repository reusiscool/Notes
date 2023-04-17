function f(){
  alert('ashbdak');
};
let ls = document.getElementsByClassName('created');
for (const i of ls) {
    let date = new Date(i.innerHTML);
    i.innerHTMl = date.toLocaleString();
//    i.innerHTML = 'none';
}