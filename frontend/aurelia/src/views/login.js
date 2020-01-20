export class Login{
    constructor(){

    }
    activate(view,route,router){
        this.root = route.settings.root
        console.log(this.root)
        this.root.gateway.apiQuery('api/login','POST',{username:'clark.bains',password:'databaseTester101'})
    }

    
}

