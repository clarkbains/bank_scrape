import {HttpClient, json} from 'aurelia-fetch-client';
let client = new HttpClient();
export class Gateway{
    a = "r"
    
    constructor(opts){
        console.log("Const")
        console.log(this)
        this.session = opts.session || "";
        this.host = opts.host
    }
    login (username,password) {
        return 
        console.log ("Logging in with opts ", opts)
    }
    apiQuery (path,method,data){
        var headers  = new Headers();
        headers.append('content-type','application/json')
        headers.append('x-auth',this.session)
        console.log("Request", this.host+'/'+path)
        return client.fetch(this.host+'/'+path,{
            method: method,
            headers: headers,
            body: JSON.stringify(data)
        })
    }
}