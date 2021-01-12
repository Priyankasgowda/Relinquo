$("#submit").on('click', function(){

		var first_name =  $("#first_name").val();
		var last_name =  $("#last_name").val();
		var email =  $("#email").val();
		var username =  $("#username").val();
		var password =  $("#password").val();
		var org_id =  $("#org_id").val();

		var data={};
		data["first_name"]=first_name;
		data["last_name"]=last_name;
		data["email"]=email;
		data["username"]=username;
		data["password"]=password;
		data["org_id"]=org_id;

		$.ajax({
			method: "POST",
			url: "http://127.0.0.1:8000/api/getstarted/",
			type:'application/json',
			data:data,
			success:function(response){
				if (response.error) {
					alert(response.error);
				} else {
				alert(response.success);
				window.location.href="/login/";

				}

			}

		});
});
