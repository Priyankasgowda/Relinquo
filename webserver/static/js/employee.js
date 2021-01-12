$(document).ready(function(){
	if (!window.localStorage["token"]){
		alert("You're not authenticated! Please login.");
		window.location = "/login/"
	}




$("#submit").on('click', function(){

		var date =  $("#date").val();
		var duration =  $("#duration").val();
		var reason =  $("#reason").val();
		

		var data={};
		
		data["date"]=date;
		data["duration"]=duration;
		data["reason"]=reason;
		
		$.ajax({
			method: "POST",
			url: "/api/leave/",
			data:data,
			type:'application/json',
			 beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                console.log(response);
                alert("successful!");

            },
        });
    });

});