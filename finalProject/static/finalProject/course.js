document.addEventListener('DOMContentLoaded', function() {
    initial();

    // Use buttons that display course items and final test
    document.querySelectorAll('.item').forEach(button => {
        button.onclick = () => {
            let item = button.dataset.id;
            console.log(`the item selected is ${item}`)
            if (button.classList.contains('btn-danger')){                 
                document.querySelector('#items_list').style.display = 'flex' ;
                document.querySelector(`#${item}`).style.display = 'none';
                document.querySelector(`#${final_button}`).className='btn btn-outline-success item';
            }
            if (button.classList.contains('btn-outline-info')){                 
                document.querySelector(`#${item}`).style.display = 'none';
                button.className='btn btn-outline-success item';
            }
            else{
                
                if (item == 'section5'){
                    document.querySelector('#items_list').style.display = 'none' ;
                    document.querySelector(`#${item}`).style.display = 'flex';
                }
                else{
                document.querySelector(`#${item}`).style.display = 'flex';
                button.className='btn btn-outline-info item';
                }
            }
        }
    });


    //send final test
    document.querySelector('#test_3').onsubmit = ()=>{
        let course = document.getElementsByName("course")[0].value;
        let version = document.getElementsByName("version")[0].value;
        options=[0,1,2,3,4]
        let question1 = 1;
        let question2 = 2;
        let question3 = 3;
        let question4 = 4;
        let question5 = 5;
        let question6 = 5;
        
        for (i in options){
            if (document.getElementsByName("question1")[i].checked === true){
                question1 = document.getElementsByName("question1")[i].value;
            }
            if (document.getElementsByName("question2")[i].checked === true){
                question2 = document.getElementsByName("question2")[i].value;
            }
            if (document.getElementsByName("question3")[i].checked === true){
                question3 = document.getElementsByName("question3")[i].value;
            }
            if (document.getElementsByName("question4")[i].checked === true){
                question4 = document.getElementsByName("question4")[i].value;
            }
            if (document.getElementsByName("question5")[i].checked === true){
                question5 = document.getElementsByName("question5")[i].value;
            }
            if (document.getElementsByName("question6")[i].checked === true){
                question6 = document.getElementsByName("question6")[i].value;
            }
        }
        fetch('/test', {
            method: 'POST',
            body: JSON.stringify({
                course: course,
                version:version,
                question1:question1,
                question2:question2,
                question3:question3,
                question4:question4,
                question5:question5,
                question6:question6,
            })
        })        
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if ("message" in result) {  
                console.log(result['message'])
                document.querySelector('#final_button').style.display = 'none';
                document.querySelector('#items_list').style.display = 'flex';
                document.querySelector('#section5').style.display = 'none';
                document.querySelector('#message_final_test').innerHTML = `You've sent you final exam, your result was ${result['result']}`;    
            }
            if ("error" in result) {
                console.log(result['error'])
                //if is not success show the error
                document.querySelector('#result').innerHTML = result['error']
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
        return false;
    }
  
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

//initial configuration
function initial(){
    document.querySelector('#section1').style.display="none";
    document.querySelector('#section2').style.display="none";
    document.querySelector('#section3').style.display="none";
    document.querySelector('#section4').style.display="none";
    document.querySelector('#section5').style.display="none";
}
