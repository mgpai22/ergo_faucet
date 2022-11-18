function getInput(){
    let myData = document.getElementById('text').value
    console.log(myData)
    console.log(window._env_.API_URL)
    $.post("http://{your-ip}:5000/faucet_api", {"address": myData})
      .done(function( data ) {
        if (data === 'Error'){
            alert("Error, please try again!")
        }
        else {
        alert("Submitted, please wait for the transaction!")
        $body = $("body")
        $body.addClass("loading")
        getHash(data.task_id)
        console.log(data.task_id)
    }
      })
      
}

function getHash(taskID) {
  var checker = setInterval(function(){
    $.ajax({
        type: 'GET',
        url: 'http://{your-ip}:5000/api_hash/' + taskID,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
          try{
          if (data.tx_hash !="None"){
          $body.removeClass("loading")
          console.log(`https://testnet.ergoplatform.com/en/transactions/${data.tx_hash}`)
          stopChecker()
        if (window.confirm('Sent!')){
        window.location.href=`https://testnet.ergoplatform.com/en/transactions/${data.tx_hash}`
        };
        }
        
      } catch (error){}
      }
    });
  }, 3000);

  function stopChecker() {
    clearInterval(checker)
  }
}