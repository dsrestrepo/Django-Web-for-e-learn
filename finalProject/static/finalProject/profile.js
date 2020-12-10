document.addEventListener('DOMContentLoaded', function() {
    initial();

    // Use buttons that display th different profile options
    document.querySelectorAll('.btn-secondary').forEach(button => {
        button.onclick = () => {
            let active = document.querySelector('.active');
            active.className = 'btn btn-secondary profile_buttons';
            let div = active.dataset.id;
            document.querySelector(`#${div}`).style.display="none";

            let item = button.dataset.id;
            if (!button.classList.contains('active')){ 
            document.querySelector(`#${item}`).style.display="block";
            button.className='btn btn-secondary profile_buttons active';
            }
        }
    });

    // edit Profile
    document.querySelector('#edit_profile_form').onsubmit = ()=>{
        let first_name = document.querySelector("#first_name").value;
        let last_name = document.querySelector("#last_name").value;
        let country = document.querySelector('#country').value;
        let career = document.querySelector('#career').value;
        let profession = document.querySelector('#profession').value;
        let username = document.querySelector('#username').value;    
        let email = document.querySelector('#email').value;    
        fetch('/editUser', {
            method: 'PUT',
            body: JSON.stringify({
                first_name:first_name,
                last_name:last_name,
                country:country,
                career:career,
                profession:profession,
                username,username,
                email:email
            })
        })        
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if ("message" in result) {  
                console.log(result['message'])
                document.querySelector('#edit_profile_message').style.color="green";
                document.querySelector('#edit_profile_message').innerHTML="the profile has been updated successfully";
                document.querySelector("#user_full_name").innerHTML=`${first_name} ${last_name}`;  
                document.querySelector("#user_country").innerHTML=`${country}`;
                document.querySelector("#user_career").innerHTML=`${career}`;
                document.querySelector("#user_profession").innerHTML=`${profession}`;
                document.querySelector("#user_email").innerHTML=`${email}`;
                //if is success show the result
            }
            if ("error" in result) {
                console.log(result['error'])
                //if is not success show the error
                document.querySelector('#edit_profile_message').style.color="red";
                document.querySelector('#edit_profile_message').innerHTML = result['error']
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
        return false;
    }

    //Send New Message
    document.querySelector('#message-form').onsubmit = ()=>{
        let message = document.querySelector('#message-content').value;
        let target_user = document.querySelector("#target_user").value;
        fetch('/newMessage', {
            method: 'POST',
            body: JSON.stringify({
                message: message,
                user:target_user,
            })
        })        
        .then(response => response.json())
        .then(result => {
        if ("message" in result) {  
            console.log(result['message'])
            document.querySelector('#send_message_message').style.color="green";
            document.querySelector('#send_message_message').innerHTML = "The message has been sent successfully"
            document.querySelector('#message-content').value = ""
            //if is success send to sent view
        }
        if ("error" in result) {
            console.log(result['error'])
            //if is not success show the error
            document.querySelector('#edit_profile_message').style.color="red";
            document.querySelector('#send_message_message').innerHTML = result['error']
        }
        console.log(result);
        })
        .catch(error => {
        console.log(error);
        });
        return false;
    };

    //read message
    document.querySelectorAll('.card').forEach(card=>{
        card.onclick = () =>{
            let id = card.dataset.id;
            fetch('/read', {
                method: 'PUT',
                body: JSON.stringify({
                    id: id
                })
            })        
            .then(response => response.json())
            .then(result => {
            if ("message" in result) {  
                console.log(result['message'])
                card.style.background = 'whitesmoke'     
                //if is success send to sent view
            }
            if ("error" in result) {
                console.log(result['error'])
                //if is not success show the error
            }
            console.log(result);
            })
            .catch(error => {
            console.log(error);
            });
            return false;
        }
    });

}) 

function initial(){
    document.querySelector('#see_results_div').style.display="none";
    document.querySelector('#see_comments_div').style.display="none";
    document.querySelector('#see_courses_div').style.display="block";
    document.querySelector('#edit_profile_div').style.display="none";
    document.querySelector('#send_message_div').style.display="none";
    document.querySelector('#see_message_div').style.display="none";
}
