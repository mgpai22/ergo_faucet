function getInput(){
    $body = $("body")
    $body.addClass("loading")
    let myData = document.getElementById('text').value
    console.log(myData)
    $.post("http://localhost:5000", {"address": myData})
      .done(function( data ) {
        $body.removeClass("loading")
        // alert( "Data Loaded: " + data );
        if (data === 'Error'){
            alert("Error, please try again!")
        }
        else {
        if (window.confirm('Sent!')) 
        {
        window.location.href=data
        };
    }
      })
      
}

async function test(){
    await ergoConnector.nautilus.connect()
    console.log(await ergo.get_unused_addresses())
}
