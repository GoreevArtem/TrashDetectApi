import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";

@Injectable()
export class UserService {
    constructor(private http: HttpClient){}
    private path1='user/me';
    private path2='user/me_delete';
    private path3='user/update_password';
    private path4='user/update_email';

    getUser()
    {
        return this.http.get<any>(`${environment.api}${this.path1}`,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    deleteUser()
    {
        return this.http.delete<any>(`${environment.api}${this.path2}`,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    updatePassword(data:any)
    {
        return this.http.patch(`${environment.api}${this.path3}`,data,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t})});
    }

    updateLogin(data:any)
    {
        return this.http.patch(`${environment.api}${this.path4}`,data,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t})});
    }
}