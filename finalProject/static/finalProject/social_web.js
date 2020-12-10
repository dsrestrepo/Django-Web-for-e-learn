document.addEventListener('DOMContentLoaded', function() {
    initial();

    // Use buttons that display course items and final test
    document.querySelectorAll('.item').forEach(button => {
        button.onclick = () => {
            let item = button.dataset.id;
            console.log(`the item selected is ${item}`)
            if (button.classList.contains('btn-outline-info')){                 
                document.querySelector(`#${item}`).style.display = 'none';
                button.className='btn btn-outline-success item';
            }
            else{
                
                document.querySelector(`#${item}`).style.display = 'flex';
                button.className='btn btn-outline-info item';
            }
        }
    });


    
        
    // Search movie
    document.querySelector('#movie_search').onsubmit = ()=>{
        let movie = document.querySelector('#seach_bar').value;
        movie = movie.trim()
        document.querySelector('#movie_list').innerHTML = ''
        document.querySelector('#recommendation_list').innerHTML = ''

        fetch('/load_csv_file', {
            method: 'PUT',
            body: JSON.stringify({
                movie: movie
            })
            })        
        .then(response => response.json())
        .then(result => {
        if ("movies" in result) {  
            //if is success send to sent view
            console.log(result['movies'])
            document.querySelector('#seach_bar').value="";
            document.querySelector('.course_content_div_recommender').style.paddingBottom = '20px';
            
            movies = result['movies']
            posters = result['posters']
            ids = result['ids']
            //console.log(movies.length)
            if(movies.length >= 10 ){
                movies = movies.slice(0, 9);
                posters = posters.slice(0, 9)
                ids = ids.slice(0, 9)
            }
            //console.log(movies)
            for (i=0; i<movies.length; i++){
                document.querySelector('#movie_list').innerHTML += `
                <div style="margin-top: 20px; margin-bottom=20px">
                    <div class="card" style="width: 18rem; background: white;">
                    <!-- <img class="card-img-top" src="https://image.tmdb.org/t/p/w185${posters[i]}" alt="Card image cap">
                        -->
                        <div class="card-body">
                        <h5 class="card-title">${movies[i]}</h5>
                        <a data-id="${ids[i]}" data-name="${movies[i]}" class="btn btn-primary movie_btn" onclick="get_recommendation(this.dataset.id, this.dataset.name)">See recommendations of ${movies[i]}</a>
                        </div>
                    </div>
                </div>
                `;
            }
        }
        if ("error" in result) {
            console.log(result['error'])
            //if is not success show the error
            
            document.querySelector('#seach_bar_message').innerHTML = result['error']
            document.querySelector('#seach_bar_message').style.color = 'red'
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

function get_recommendation(id, name){
    
    console.log(`the item selected is ${id}`)
    fetch('/get_recommendation', {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
        })        
    .then(response => response.json())
    .then(result => {
    if ("recommendation" in result) {  
        //if is success send to sent view
        
        document.querySelector('#movie_list').innerHTML = ''

        console.log(result['recommendation'])
        document.querySelector('.course_content_div_recommender').style.paddingBottom = '20px';
        document.querySelector('#recommendation_list').innerHTML = `<h2>Your recommendation for ${name} </h2>`
        
        let movies = result['recommendation']
        
        if(movies.length >= 10 ){
            movies = movies.slice(0, 9);
        }
        //console.log(movies)
        for (i=0; i<movies.length; i++){
        
            document.querySelector('#recommendation_list').innerHTML += `<div class="alert alert-success" ><h4> ${i+1}. ${movies[i][1]} </h4></div>`;
        }
    }
    if ("error" in result) {
        console.log(result['error'])
        //if is not success show the error
        
        document.querySelector('#recommendation_list').innerHTML = result['error']
        document.querySelector('#recommendation_list').style.color = 'red'
    }
    console.log(result);
    })
    .catch(error => {
    console.log(error);
    
    });
    return false;

}


/* 
function getMovieInfo(id){
    let baseURL = 'https://api.themoviedb.org/3/movie/';

    let baseImageURL = null;
    
    let getConfig = function () {
        let url = "".concat(baseURL, id,'?api_key=', '{19a95550df4fedce88dbdc6f0472b3e9}','&callback=test'); 
        fetch(url)
        .then((result)=>{
            return result.json();
        })
        .then((data)=>{
            console.log('data')
            //baseImageURL = data.images.secure_base_url;
            //configData = data.images;
            //console.log('config:', data);
            //console.log('config fetched');
            
        })
        .catch(function(err){
            console.log(err);
        });
    return false;

    }
}
*/