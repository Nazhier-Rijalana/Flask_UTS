function encrypt() {
    var plaintext = document.getElementById("plaintext");
    var keyPadding = document.getElementById("keyPadding");
    var key2 = document.getElementById("Key2");

    $.ajax({
       type: "POST",
       url: "/encrypt/proc",
       data:{
         "plaintext":plaintext,
         "keyPadding":keyPadding,
         "key":key2,
       },
        success : function (response) {
            var text1 = document.createElement("span");
            text1.innerHTML = response;
            $("body").append(text1);
        }
    });
}
// function decrypt() {
//     var chipertext = document.getElementById("chipertext");
//     var keyPadding = document.getElementById("keyPadding");
//     var key2 = document.getElementById("key2");
//
//     $.ajax({
//        type: "POST",
//        url: "/decrypt/proc",
//        data:{
//            "chipertext":chipertext,
//            "keyPadding": keyPadding,
//            "key2":key2
//        } ,
//         success : function (response) {
//             // var text1 = "<span></span>";
//             var text1 = document.createElement("span");
//             text1.innerHTML = response;
//             $("body").append(text1);
//         }
//     });
// }