    //Attempt to get the element using document.getElementById
    var successEl = document.getElementById("msg-success");
    var warningEl = document.getElementById("msg-warning");
    var infoEl = document.getElementById("msg-info");
    var errorEl = document.getElementById("msg-error");

    //If it isn't "undefined" and it isn't "null", then it exists.
    if(typeof(successEl) != 'undefined' && successEl != null){
        toastr.success(successEl.innerText);
    }

     if(typeof(warningEl) != 'undefined' && warningEl != null){
        toastr.warning(warningEl.innerText);
    }

      if(typeof(infoEl) != 'undefined' && infoEl != null){
        toastr.info(infoEl.innerText);
    }
      if(typeof(errorEl) != 'undefined' && errorEl != null){
        toastr.error(errorEl.innerText);
    }
console.log("dsds")