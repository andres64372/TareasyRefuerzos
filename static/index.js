var regresar = document.getElementById("regresar");
var files = document.getElementById("file-input");
var envia = document.getElementById("envia");
var subfile = document.getElementById("subfile");
var table = document.getElementById("tbody");
var cargar = document.getElementById("cargar");
var loader = document.getElementById("loader");
files.style.visibility = "hidden";
subfile.style.visibility = "hidden";
loader.style.visibility = "hidden";
//envia.disabled = true;
document.getElementById("table").style.visibility = "hidden";
var filenum = 0;
var label = [];
var ext = /(\.rar|\.pdf|\.doc|\.docx|\.xls|\.xlsx|\.jpeg|\.jpg|\.png|\.gif)$/i;
files.addEventListener("change", function(){
    const xhr = new XMLHttpRequest();
    const form = new FormData();
    for (const file of files.files){
        if(file.size < 20*1024*1024){
            if(ext.exec(file.name)){
                form.append("file",file);
                filenum++;
            }else{
                alert("La extension del archivo "+ file.name +" no es valida");
            }
        }else{
            alert("El archivo "+ file.name +" es demasiado pesado");
        };      
    }
    if(filenum > 0){
        xhr.open("post","file");
        xhr.addEventListener("loadstart", function(data){
            envia.disabled = true;
            loader.style.visibility = "visible";
        })
        xhr.addEventListener("load", function(data){
            var resp = JSON.parse(data.target.response);
            document.getElementById("table").style.visibility = "visible";
            for(const index of resp){
                var row = table.insertRow(0);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                cell1.innerHTML = index.name;
                cell2.innerHTML = "<a onclick='borrar(this)'> &#128308 </a>";
                label.push(index)
            }
            strconv();
            envia.disabled = false;
            loader.style.visibility = "hidden";
        })
        xhr.send(form);
    }
});
function borrar(e){
    const xhr = new XMLHttpRequest();
    const form = new FormData();
    var i = e.parentNode.parentNode.rowIndex;
    var val = -1;
    var element = document.getElementById("table").rows[i].cells[0].innerHTML;
    xhr.open("post","borrar");
    xhr.addEventListener("loadstart", function(data){
        envia.disabled = true;
    })
    xhr.addEventListener("load", function(data){
        envia.disabled = false;
    })
    for(const index of label){
        if(index.name === element){
            form.append("file",index.file);
            xhr.send(form);
            label.splice(label.indexOf(index),1);
        }
    }
    strconv();
    document.getElementById("table").deleteRow(i);
    filenum--;
    if(filenum<1){
        document.getElementById("table").style.visibility = "hidden";
    }
};
function strconv(){
    var arr = [];
    for(const index of label){
        arr.push(index.file);
    }
    subfile.value = arr.toString();
}
cargar.addEventListener("click", function(evt) {
    evt.preventDefault();
    files.click();
});
regresar.addEventListener("click", function(){
    window.history.back();
});