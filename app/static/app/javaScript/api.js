$(document).ready(function () {
    let manga = $("manga").text();
    function manga(elemento){
        let manga = `
        <div class="container Mangas" id="Mangas">
            <div class="productoM">
                <img src=${elemento.imagen} alt="" class="imgManga">
                <h1 class=${elemento.titulo}></h1>
                <h1 class=${elemento.editorial}></h1>
                <p class=${elemento.precio}><p>CLP</p></p>
                <h1 class=${elemento.descripcion}></h1>
                <h1 class=${elemento.cantidad}></h1>
            </div>
        </div>`
        $('#Mangas').append(manga)
    }
    $.get("https://mangas-4edfa-default-rtdb.firebaseio.com/mangas.json", function(data, status){
        console.log(status)
        $.each(data, function (vistasMangas, elemento) {
            manga(elemento)
            console.log(elemento.titulo)
        });
    });
});