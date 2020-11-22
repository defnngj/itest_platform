function getCaseInfo() {
    var url = window.location.href;
    var caseId = url.split("/")[5];

    $.post("/api/get_case_info/", {
        cid: caseId
    }, function (resp) {
        if (resp.code == 10200) {
            //URL
            document.querySelector("#req_url").value = resp.data.url;

            // 请求方法
            if(resp.data.method == 1){
                document.querySelector("#get").setAttribute("checked", "");
            }else if(resp.data.method == 2){
                document.querySelector("#post").setAttribute("checked", "");
            }

            // header
            var header_json = JSON.parse(resp.data.header);
            headerEditor.set(header_json);

            //参数类型
             if(resp.data.method == 1){
                document.querySelector("#form").setAttribute("checked", "");
            }else if(resp.data.method == 2){
                document.querySelector("#json").setAttribute("checked", "");
            }

            // 参数
            var par_json = JSON.parse(resp.data.parameter_body);
            parameterEditor.set(par_json);

            // 结果
            document.querySelector("#result").value = resp.data.result;

            // 断言类型
             if(resp.data.method == 1){
                document.querySelector("#include").setAttribute("checked", "");
            }else if(resp.data.method == 2){
                document.querySelector("#equal").setAttribute("checked", "");
            }

            // 断言内容
            document.querySelector("#assert").value = resp.data.assert_text;

             // 名称
            document.querySelector("#case_name").value = resp.data.name;

            // 初始化菜单
            SelectInit(resp.data.project, resp.data.module);
        }
    });

}