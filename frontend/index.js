// API gateway SDK
var apigClient = apigClientFactory.newClient();
// var apigClient = apigClientFactory.newClient({
//   accessKey: 'ACCESS_KEY',
//   secretKey: 'SECRET_KEY',
// });
//


$("#search-form").on("submit", () => {
    var params = {"q": $("#q").val()}
    var additionalParams = {}
    var body = ""
    apigClient.searchGet(params, body, additionalParams)
        .then((result) => {
            var html = ""
            for (let [key, item] of Object.entries(result['data']['results'])){
                var new_url = ""
                var urlArray = item['url'].split('/')
                urlArray[urlArray.length-1] = encodeURIComponent(urlArray[urlArray.length-1])
                console.log(urlArray)
                for (i=0; i<urlArray.length; i++){
                    if (i != urlArray.length - 1){
                        new_url = new_url + urlArray[i] + '/'
                    }else {
                        new_url = new_url + urlArray[i]
                    }
                }
                console.log(new_url)
                html = html + "<li><img alt=\"Not found\" src=" + new_url + " style=\"max-width: auto; height: 100px; \"> </br>"
                html = html + "<text> Labels: " + item['labels'] + "</text></li> </br> "
            }
            $("#result-list").html(html)
        })
        .catch((error) => console.log(error))
    return false
})

$("#photo").on("click", () => $("#uploadTitle").text('Upload photo'))

$("#upload-form").on("submit", function() {
    var item = $("#photo").val().split('\\').pop()
    let ContentType = 'image/' + $("#photo").val().split(".").pop()
    var params = {"item": item, "folder": "prj3photostore", "Content-Type": ContentType}
    var additionalParams = {}

    var reader = new FileReader();
    reader.onload = function (event) {
        var base64String = reader.result.replace(/^data:image\/\w+;base64,/, "")
        apigClient.uploadPut(params, base64String, additionalParams)
            .then(() => $("#uploadTitle").text('Done'))
            .catch((error) => console.log(error))
    }
    reader.readAsDataURL($("#photo")[0].files[0])
    return false
});



