$(document).ready(function() {
    if (!window.localStorage["token"]){
        alert("You're not authenticated! Please login.");
        window.location = "/login/"
    }




    var teamdiv = $("#allteams");
    var blankmsg = $("#blankmsg");
    var teamid;
    var target;
    getTeams();



    $.ajax({
        method: "GET",
        url: "/api/profile/",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
        },
        success: function(response) {
            console.log(response);
            for (var emp of response) {
                $("#employee-name-list").append(`
						<option value=${emp.user.id}>${emp.user.first_name} ${emp.user.last_name}</option>
					`);
                $("#team-leads-list").append(`
                        <option value=${emp.user.id}>${emp.user.first_name} ${emp.user.last_name}</option>
                    `);


            }
        },
    });





    $("#createteam").on("click", function() {

        var json = {};
        json["name"] = $("#teamname").val();
        json["about"] = $("#teamabout").val();
        json["size"] = $("#teamsize").val();
        json["lead"] = $('#team-leads-list').find(":selected").attr('value');

        $.ajax({
            method: "POST",
            url: "/api/team/",
            data: json,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                $('#createnewteam').modal('hide');
                getTeams();

            },
        });



    });


    function getTeams() {
        $.ajax({
            method: "GET",
            url: "/api/team/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                if (response.teams.length == 0) {
                    blankmsg.append(BlankTeamScreen());

                } else {
                    blankmsg.html('');
                    blankmsg.append(`<button class="btn btn-sm btn-warning" data-toggle="modal" 
                    	data-target="#createnewteam">Create New Team</button><br><br>`)
                    teamdiv.html('');
                    for (let teamobj of response.teams) {
                        teamdiv.append(TeamCard(teamobj));
                    
                    }
                }
            },
        });

    };

    $(document).on('click', '.add-employee', function() {
        teamid = $(this).data("team-id");
        target = $(this).data('target');
        $(target).modal("show");

    });

    $("#save-employee").on('click', function() {
        let team = teamid;
        let user = $("#employee-name-list").find(":selected").attr('value');

        let data = {}
        data['user'] = user;
        data['team'] = team;

        $.ajax({
            method: "POST",
            url: "/api/teammember/",
            data: data,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
            },
            success: function(response) {
                $(target).modal("hide");
                console.log(response);

            },
        });
    });


});


function TeamCard(team) {
    let header = `
			<div class="card" style="width: 18rem; margin-right:10px">
			  <div class="card-body">
			    <h5 class="card-title">${team.name}</h5>
			    <p class="card-text">${team.about}</p>
			    <span><b>Lead:</b> ${team.lead.email}</span><br>
			    <span><b>Size:</b> ${team.size}</span>
                
			  <br><hr><br><h4>Team Members</h4>`

    var footer = `<button type="button"  class="btn btn-primary add-employee" 
              data-team-id=${team.id} data-target="#employeeModal">
             Add New Team Members
            </button><br><br></div>
			</div>`
    var teammembers = ``;
    var component;

    let data = {};
    data['team'] = team.id;
    $.ajax({
        method: 'GET',
        url: '/api/teammember/',
        data: data,
        type: 'application/json',
        async: false,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Token " + window.localStorage["token"]);
        },
        success: function(response) {
            for (let teammember of response) {
                teammembers += "<p>" + teammember.user.first_name + " " + teammember.user.last_name + "</p>";
            }
            component = header + teammembers + footer;

        },
    });
    
        return component;

}


function BlankTeamScreen() {
    let component = `
			<div style="text-align:center;">
			<h5>You currently aren't part of any team. Please create your own team! </h5><br>
			<button class="btn btn-lg btn-warning" data-toggle="modal" 
			data-target="#createnewteam">Create New Team</button>
			</div>
			`

    return component;
}