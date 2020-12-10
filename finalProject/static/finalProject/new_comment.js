document.addEventListener('DOMContentLoaded', function() {


    // New Post
    document.querySelector('#post-form').onsubmit = ()=>{
        let post = document.querySelector('#post-content').value;
        let cname = document.querySelector("#post-course").value;
        fetch('/newPost', {
            method: 'POST',
            body: JSON.stringify({
                content: post,
                course_name:cname
            })
            })        
        .then(response => response.json())
        .then(result => {
        if ("message" in result) {  
            console.log(result['message'])
            document.querySelector('#post-content').value="";
            location.reload();
            //if is success send to sent view
        }
        if ("error" in result) {
            console.log(result['error'])
            //if is not success show the error
            document.querySelector('#result').innerHTML = result['error']
        }
        console.log(result);
        })
        .catch(error => {
        console.log(error);
        });
        return false;
    };

    
        
}) 
