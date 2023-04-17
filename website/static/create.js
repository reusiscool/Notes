function post () {
    let data = new FormData();
    data.append("title", document.getElementById("title").value);
    data.append("body", document.getElementById("body").value);
    let date_info = document.getElementById("datetime").value;
    if (date_info){
        let date = new Date(date_info);
        data.append("datetime", `${date.getUTCFullYear()}-${date.getUTCMonth() + 1}-${date.getUTCDate()}T${date.getUTCHours()}:${date.getUTCMinutes()}`);
    }
    else{
        data.append("datetime", "")
    }
    fetch("/create", {
      "method": "POST",
      "body": data,
    }).then(response => response.json()).then(info => {
        if (info['status'] == 'successful'){
            window.location = '/';
        }
        else{
            alert(info['error']);
        }
    });
}