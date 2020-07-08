$(document).ready(function() {
    getMoviesData()
        .then(function(data){
            // console.log(data.count)
            let $li =  $('#movie-items > li').clone();
            $('#movie-items').empty()
            let $ul = $('#movie-items')
            for(let i = 0; i < data.count; i++){
                let $newLi = $li.clone()
                // img
                $newLi.children('a').children('img').attr('src', data.subjects[i].img)
                
                let $spans = $('.movie-info', $newLi).children()
                // name                
                $spans.children('.name').text(data.subjects[i].movieName)
                // url
                $spans.children('.name').attr('href', 'https://movie.douban.com/subject/' + data.subjects[i].movieId)
                // rating
                $spans[1].innerText = '电影评分：' + data.subjects[i].rating
                // genres
                $spans[2].innerText = '电影类型：' + data.subjects[i].genres
                // summary
                $('.movie-summary', $newLi).text(data.subjects[i].summary)
                $ul.append($newLi)
            }
        })
    $li =  $('#movie-items > li').clone();
    console.log($li);
});



function getMoviesData() {
    let url = './js/test.json'

    return $.get(url).promise()
        .catch(function(err){
            if (err) {
                console.log(err)
            }
        })
};



