$(document).ready(function() {

    if (!window.localStorage["token"]){
        alert("You're not authenticated! Please login.");
        window.location = "/login/"
    }


    $(document).on("click", ".accept-leave", function(){
        let lid = $(this).attr('id').slice(3,);
        let data = {"state" : "Accept"}
        $.ajax({
        method:"PATCH",
        url:"/api/leave/" + lid + "/",
        data: data,
        type: 'application/json',
        beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
        success: function(response) {
            alert(response);
            window.location = "/dashboard/";

                   
           },

        });
    });

     $(document).on("click", ".reject-leave", function(){
        var lid = $(this).attr('id').slice(3,);
        let data = {"state" : "Reject"}
        $.ajax({
        method:"PATCH",
        url:"/api/leave/" + lid + "/",
        data: data,
        type: 'application/json',
        beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
        success: function(response) {
            alert(response);
            window.location = "/dashboard/";

           },

        });
    });

    var orgdiv = $("#allorgs");
    var blankmsg = $("#blankmsg");

    getOrganisation();

    var leave_requests=$("#leave_requests");
	$.ajax({
		method:"GET",
		url:"/api/leave/",
		beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
        success: function(response) {
        	console.log(response);
        	for (let leave_req of response) {
        		leave_requests.append(`<div class="card">
        			<div class="card-body">
        			<p class="card-title">${leave_req.name.first_name} has requested for leave on ${leave_req.date} </p>
        			${Button_leave(leave_req.id)}
        			</div>
        			</div><br>`);
        	}          
           },

	});

    $("#createneworg").on("click", function() {

        var json = {};
        json["name"] = $("#name").val();
        json["about"] = $("#about").val();
        json["founded"] = $("#founded").val();
        json["org_size"] = $("#org_size").val();


        $.ajax({
            method: "POST",
            url: "/api/organisation/",
            data: json,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                console.log(response);
                $('#createnewOrganisation').modal('hide');
                getOrganisation();

            },
        });



    });


    function getOrganisation() {
        $.ajax({
            method: "GET",
            url: "/api/organisation/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                console.log(response);
                if (response.length == 0 || response.error) {
                    $("#blankmsg").append(BlankTeamScreen());
                     $("#leave_requests").hide();
                } else {
                    blankmsg.html('');
                    orgdiv.html('');
                    orgdiv.append(OrganisationCard(response));


                }
            },
        });

    };

});


function OrganisationCard(org) {
    let component = `
			<div class="card" style="width: 18rem; margin-right:10px">
			  <div class="card-body">
			<h5 class="card-title">${org.name} (<span style="font-size:16px"><b>ID:</b> ${org.org_id}<span>)</h5>
			    <p class="card-text">${org.about}</p>
			    <span><b>Founded On:</b> ${org.founded}</span><br>
			    <span><b>Size:</b> ${org.org_size}</span>
			    <br>
				<a href="/team/" type="button" class="btn btn-primary" style="margin-top:20px;margin-left:30px;">Add Team</a>
			  </div>

			</div>

			`

    return component;
}


function BlankTeamScreen() {



    let component = `
			<div style="text-align:center;">
			<h5>You currently aren't part of any organisation. Please create your own organisation! </h5><br>
			<button class="btn btn-lg btn-warning" data-toggle="modal" data-target="#createnewOrganisation">Create New Organisation</button>
			</div>`;


    return component;
}

function Button_leave(id) {
    let component = `
            <div class="alert alert-info" role="alert" id="lmsg-${id}" style="display:none">
            </div>
			<button type="button" class="btn btn-sm btn-success accept-leave" id="la-${id}">Accept</button>
			<button type="button" class="btn btn-sm btn-outline-danger reject-leave" id="lr-${id}">Decline</button>
			`
    return component;
}

