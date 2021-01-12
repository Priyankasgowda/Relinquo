$("#submit").on('click', function(){

	var username =  $("#username").val();
	var password =  $("#password").val();

	var data={};
	data["username"]=username;
	data["password"]=password;
	
	console.log(data);
	$.ajax({
		method:"POST",
		url:"/api-token-auth/",
		type:'application/json',
		data:data,
		success: function(response){
			console.log(response);
			window.localStorage["token"] = response['token'];
			window.location = '/dashboard/';
		},
		


	});
});
