async function search(){
    query = document.getElementById("search").value
    response = await fetch("/api/search?q="+query)
    json_ = await response.json();
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
        }
        name_item = element.name;

        document.getElementById("results").innerHTML =document.getElementById("results").innerHTML+"<li>"+"<a class='result_title'>"+name_item+"</a>"+"<br>"+artistText+"</li><hr>" 
        
    }

}