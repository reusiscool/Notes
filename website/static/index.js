function f(){
  alert('ashbdak');
};
let ls = document.getElementsByClassName('created');
for (const i of ls) {
    let date = new Date(i.innerHTML);
    i.innerHTML = 'created on ' + date.toLocaleString();
}
ls = document.getElementsByClassName('notify');
for (const i of ls) {
    let date = new Date(i.innerHTML);
    date = date.toLocaleString();
    if (date != 'Invalid Date'){
        i.innerHTML = 'notification on ' + date;
    }
}
