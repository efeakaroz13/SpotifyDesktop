document.getElementById("results").style.display = "none";
async function search(){
    document.getElementById("results").style.display = "";
    document.getElementById("results").innerHTML = "<h3>Loading...</h3>";
    
    query = document.getElementById("search").value
    response = await fetch("/api/search?q="+query)
    json_ = await response.json();
    document.getElementById("results").innerHTML =""
    //Playlists
    items = json_.playlists.items;
    items = items.slice(0, 2);
    for (let i = 0; i < items.length; i++) {

        const element = items[i];
        
        owner = element.owner
        artistText = "<a href='/user/"+owner.id+"' class='artist_search' >"+owner.display_name+"</a>"
        name_item = element.name;
        small_image = element.images[0].url

        type = element.type
        document.getElementById("results").innerHTML =document.getElementById("results").innerHTML+"<li>"+"<img src='"+small_image+"' class='cover'  width='60'>"+"<div class='detailGroup'><a class='result_title' href='/playlist/"+element.id+"'>"+name_item+"</a>"+"<br>"+artistText+"</div>  <a style='position:absolute;right:10px;'>"+type+"</a></li><hr>" 
        
    }
    //Artists

    items = json_.artists.items;
    items = items.slice(0, 3);
    for (let i = 0; i < items.length; i++) {

        const element = items[i];


        
        name_item = element.name;
        try{
            small_image = element["images"][2].url
        }catch{
            small_image = ""
        }
        

        type = element.type
        document.getElementById("results").innerHTML =document.getElementById("results").innerHTML+"<li>"+"<img src='"+small_image+"' class='artist-cover' width='50'>"+"<div class='detailGroup'><a class='result_title' href='/artist/"+element.id+"'>"+name_item+"</a>"+"<br><a class='artist_search'>Artist</a></div>  <a style='position:absolute;right:10px;'>"+type+"</a></li><hr>" 
        
    }

    //Tracks

    items = json_.tracks.items;
    for (let i = 0; i < items.length; i++) {

        const element = items[i];
        artistText = ""
        artists = element.artists
        for(a in artists){
            current = artists[a];
            name_ = current.name;
            id_ = current.id;
            artistText += "<a href='/artist/"+id_+"' class='artist_search' >"+name_+"</a>"
            if (artists.length-1 != a) {
                artistText += ", "
                
            }
        }
        name_item = element.name;
        small_image = element.album["images"][2].url

        type = element.type
        document.getElementById("results").innerHTML =document.getElementById("results").innerHTML+"<li>"+"<img src='"+small_image+"' class='cover' width='50'>"+"<div class='detailGroup'><a class='result_title' href='/track/"+element.id+"'>"+name_item+"</a>"+"<br>"+artistText+"</div>  <a style='position:absolute;right:10px;'>"+type+"</a></li><hr>" 
        
    }

}


function loadPL(data_string){

    data= JSON.parse(data_string);
    console.log(data)
    items = data.tracks.items;
    document.getElementById("pl").innerHTML = ""
    for (let i = 0; i < items.length; i++) {

        const element = items[i]["track"];
        artistText = ""
        artists = element.artists
        for(a in artists){
            current = artists[a];
            name_ = current.name;
            id_ = current.id;
            artistText += "<a href='/artist/"+id_+"' class='artist_search' >"+name_+"</a>"
            if (artists.length-1 != a) {
                artistText += ", "

            }
        }
        name_item = element.name;
        small_image = element.album["images"][2].url

        type = element.type
        time_min = Math.floor(element.duration_ms/60000)
        time_sec = Math.floor((element.duration_ms/60000 - time_min)*60)
        if(time_sec<10){
        time_sec = "0"+time_sec
        }
        document.getElementById("pl").innerHTML =document.getElementById("pl").innerHTML+"<li>"+"<img src='"+small_image+"' class='cover' width='50'>"+"<div class='detailGroup'><a class='result_title' id='"+element.id+"'>"+name_item+"</a>"+"<br>"+artistText+"</div>  <a style='position:absolute;right:10px;'>"+time_min+":"+time_sec+"</a></li><hr>"

    }
}
if (window.location.href.includes("/playlist")){
    loadPL(document.getElementById("pl").innerHTML);
}