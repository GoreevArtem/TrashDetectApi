import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";

@Injectable()
export class ExpertService {
    constructor(private http: HttpClient){}
    private path1='expert/me';
    private path2='expert/me_update';

    getExpert()
    {
        return this.http.get<any>(`${environment.api}${this.path1}`,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    updatePassword(data:any)
    {
        return this.http.patch(`${environment.api}${this.path2}`,data,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t})});
    }
}